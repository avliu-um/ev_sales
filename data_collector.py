from util import (append_to_json, get_selenium_driver, get_soup, find_in_dict, get_soup_text, remove_symbols_str,
                  read_from_sqs, get_today)
import json, re
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin


class DataCollector:

    def __init__(self, sqs_queue_id=None, platform=None, url=None):
        if sqs_queue_id:
            message = read_from_sqs(sqs_queue_id=sqs_queue_id)
            platform = message['platform']
            url = message['url']

        # Make sure we got these params, either from sqs queue or otherwise
        assert(platform and url)

        self.url = url
        self.platform = platform

        self.file_name = f'data_{get_today()}_{self.platform}'

    def get_data(self):
        print(f'getting data for platform {self.platform} and url {self.url}')
        data = None
        if self.platform == 'kbb':
            data = self.kbb_get_data()
        elif self.platform == 'craigslist':
            data = self.craigslist_get_data()
        elif self.platform == 'ebay':
            data = self.ebay_get_data()
        else:
            print('crying')

        # Write the data
        append_to_json(f'data/{self.file_name}.json', data)

    def kbb_get_data(self):
        driver = get_selenium_driver(undetected=True)
        driver.get(self.url)

        # wait for, then scroll from, the "make a deal" container
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[id="nativeDealContainer"]'))
        )
        above_container = driver.find_element(By.CSS_SELECTOR, 'div[id="nativeDealContainer"]')
        scroll_origin = ScrollOrigin.from_element(above_container)
        ActionChains(driver) \
            .scroll_from_origin(scroll_origin, 0, 500) \
            .perform()

        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[id="sellerComments"] div[data-cmp="heading"]'))
        )
        comment = driver.find_element(By.CSS_SELECTOR, 'div[id="sellerComments"] div[data-cmp="heading"]').text.lower()
        vin_idx = comment.lower().find('vin: ') + len('vin: ')
        # https://www.lithia.com/research/how-to/how-to-decode-your-cars-vin-number.htm
        vin_length = 17
        vin = comment[vin_idx:vin_idx + vin_length]

        price = driver.find_element(By.CSS_SELECTOR, 'div[data-cmp="pricing"]').text.lower()
        title = driver.find_element(By.CSS_SELECTOR, 'h1[data-cmp="heading"]').text.lower()

        url = driver.current_url
        state_idx = url.find('&state=') + len('&state=')
        state = url[state_idx:state_idx + 2]

        # fuel type and mileage are in a table and the only sensible labels don't actually contain the text we want;
        # hence, the workaround by searching the table text itself
        list_elem = driver.find_element(By.CSS_SELECTOR, 'div[data-cmp="section"]').text.lower()
        words = re.split('[\n ]', list_elem)

        engine_idx = words.index('engine') - 1
        engine = words[engine_idx].strip()

        miles_idx = words.index('miles') - 1
        mileage = words[miles_idx].strip()

        # Sale date
        soup = get_soup(driver)

        # Find the element containing the target string
        target_str = "window.__BONNET_DATA__="
        target_element = soup.find(string=lambda text: text and target_str in text)

        if target_element:
            # Extract the parent element's text
            parent_text = target_element.parent.get_text()
            parent_dict = json.loads(parent_text[len(target_str):])
            pricing_history = find_in_dict(parent_dict, 'pricingHistory')
            list_date = pricing_history[0]['dateUpdated']
        else:
            list_date = None

        info = {
            'vin': vin,
            'price': price,
            'title': title,
            'state': state,
            'engine': engine,
            'mileage': mileage,
            'list_date': list_date
        }
        return info

    def ebay_get_data(self):

        soup = get_soup(self.url)
        info = {}

        price = get_soup_text(soup, "span[itemprop='price']", one=True)
        info['price'] = price

        loc_text = soup.select_one('div[class*="ux-labels-values--shipping"]').text
        location = loc_text[loc_text.find('Located in:') + len('Located in:'):].strip()
        info['location'] = location

        general_info = get_soup_text(soup, 'div[class="vi-cviprow"] div[class*="u-flL"]')
        for i in range(0, len(general_info), 2):
            # print(f'i: {i}')
            if i <= 0 and i + 1 <= len(general_info):
                info[remove_symbols_str(general_info[i])] = general_info[i + 1]

        labels_text = get_soup_text(soup, 'div[class*="labels-content"]')
        values_text = get_soup_text(soup, 'div[class*="values-content"]')

        info.update(dict(zip(labels_text, values_text)))

        return info


    def craigslist_get_data(self):
        soup = get_soup(link)
        info = {}
        
        # add post metadata - id, timestamp
        id_css = 'div[class="postinginfos"] p[class="postinginfo"]'
        info['post_id'] = soup.select_one(id_css).text.split(': ')[1]
        info['post_datetime'] = soup.time.get('datetime')
        
        # add post expiration date (not applicable for all posts)
        expire_date = soup.head.find('meta', {'name': 'robots'}).get('content')
        if expire_date != 'noindex':
            info['post_expire'] = expire_date.split(': ')[1]

        # get listing attributes
        info_list = get_soup_text(soup, 'div[class=mapAndAttrs] p[class=attrgroup] span')
        for item in info_list:
            sep_idx = item.find(':')
            if sep_idx > 0:
                info[item[:sep_idx].strip()] = item[sep_idx+1:].strip()
            else:
                if 'other' in info.keys():
                    info['other'] += f'|{item}'
                else:
                    info['other'] = item

        # adding price, listing geo attributes
        json_css = 'script[id="ld_posting_data"]'
        data = soup.select_one(json_css)
        if data is not None:
            info.update(json.loads(data.get_text(strip=True)))

        # adding seller type
        purveyor_css = 'li[class="crumb section"] a'
        text = soup.select_one(purveyor_css).get_text()
        if text is not None:
            info['seller_type'] = text.split(' ')[-1]

        # adding saler free-form text and url
        body_css = 'section[id="postingbody"]'
        text = soup.select_one(body_css).get_text()
        if text is not None:
            info['seller_notes'] = re.sub('[\\n]+', ' ', text).strip()

        info['url'] = link

        return info


if __name__ == '__main__':
    #dc = DataCollector(platform='kbb', url='https://google.com')
    #dc = DataCollector(platform='ebay', url='https://google.com')
    dc = DataCollector(platform='craigslist', url='https://google.com')

    dc.get_data()