import os
from util import append_to_file, write_to_sqs, get_selenium_driver, get_soup, get_today
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# Set page limit
check_page_limit = int(os.environ.get('page_limit'))
if check_page_limit:
    page_limit = check_page_limit
else:
    page_limit = 500


class LinkCollector:

    def __init__(self, platform, zip_code, radius, sqs_queue_id=None):

        self.platform = platform
        self.zip_code = zip_code
        self.radius = radius
        self.sqs_queue_id = sqs_queue_id

        self.file_name = f'links_{get_today()}_{self.platform}'

    def get_links(self):
        print(f'getting links for platform {self.platform} with zip code {self.zip_code} and radius {self.radius}')

        links = None
        if self.platform == 'kbb':
            links = self.kbb_get_links()
        elif self.platform == 'craigslist':
            links = self.craigslist_get_links()
        elif self.platform == 'ebay':
            links = self.ebay_get_links()
        else:
            print('crying')

        # Write the links
        append_to_file(f'./data/{self.file_name}.csv', links)
        if self.sqs_queue_id:
            sqs_messages = [{"platform": "ebay", "url": link} for link in links]
            write_to_sqs(self.sqs_queue_id, sqs_messages)

    def kbb_get_links(self):

        print(f'running get_links on kbb with zip={self.zip_code} and radius={self.radius}')

        driver = get_selenium_driver(undetected=True)

        page = 0
        links = []
        while True:
            url = f'https://www.kbb.com/cars-for-sale/used/mount-pleasant-mi?searchRadius={self.radius}&zip={self.zip_code}&marketExtension' \
                  f'=include&isNewSearch=false&showAccelerateBanner=false&sortBy=relevance&numRecords=100&firstRecord={page * 100}'
            driver.get(url)

            # Wait for the links to show up, becuase they take a while to render
            WebDriverWait(driver, 40).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div[data-cmp="itemCard"] div[class="item-card-body margin-bottom-auto"] a'))
            )

            link_elements = driver.find_elements(By.CSS_SELECTOR,
                                                 'div[data-cmp="itemCard"] div[class="item-card-body margin-bottom-auto"] a')

            # When the pages gets out of range, it defaults to the last valid page
            if 'No more results found' in driver.page_source or page > page_limit:
                break
            else:
                for link_elem in link_elements:
                    try:
                        link = link_elem.get_attribute('href')
                    except Exception as e:
                        link = None
                        pass
                    if link:
                        links.append(link)
                print(f'{len(links)} links from page {page}')

            page += 1

        return links

    def ebay_get_links(self):
        page = 1

        links = []

        while True:
            # itemCondition=3000 means used
            # stpos is the center zip code
            # sadis is the radius
            # we include all the years as a workaround for not being able to see ALL results at once while searching
            url = f'https://www.ebay.com/b/Cars-Trucks/6001?mag=1&_fsrp=0&rt=nc&_sacat=6001&LH_ItemCondition=3000&Model%2520' \
                  f'Year=2023%7C2022%7C2021%7C2020%7C2019%7C2018%7C2017%7C2016%7C2015%7C2014%7C2013%7C2012%7C2011%7C2010' \
                  f'%7C2009%7C' \
                  f'2008%7C2007%7C2006%7C2005%7C2004%7C2003%7C2002%7C2001%7C2000' \
                  f'&LH_PrefLoc=99&_stpos={self.zip_code}&_sadis={self.radius}&_fspt=1&_pgn={page}'
            print(url)
            soup = get_soup(url)
            link_elements = soup.select('div[class="s-item__wrapper clearfix"] div[class="s-item__info clearfix"] '
                                        'a[class=s-item__link]')
            if len(link_elements) == 0 or page > page_limit:
                break

            for link_elem in link_elements:
                if 'href' in link_elem.attrs.keys():
                    links.append(link_elem['href'])

            page += 1

        return links


    def craigslist_get_links(self):
        
        print(f'running get_links on cragslist with zip={self.zip_code} and radius={self.radius}')
        
        links = []
        page = 1
        ev_only = True
        
        if ev_only:
            car_type = 'EVs'
            url = f'https://annarbor.craigslist.org/search/cta?auto_fuel_type=4&bundleDuplicates=1' \
                  f'&postal={zip_code}&search_distance={radius}#search=1~gallery~{page}~0'
            #note: city gets redirected by zipcode, using ann arbor as starting point
        else:
            car_type = 'all'
            url = f'https://annarbor.craigslist.org/search/cta?bundleDuplicates=1' \
                  f'&postal={zip_code}&search_distance={radius}#search=1~gallery~{page}~0'
            # to-do: research price brackets for all vehicles

        
        try: 
            soup = get_soup(url)
            cars_css = 'li[class="cl-static-search-result"] a'
            cars = soup.select(cars_css) 
            links = [car.get('href') for car in cars]    
            
            print(f'{len(links)} links found for {car_type} in {self.radius} radius around zip {self.zip_code}')

        except Exception as e:
            print(f'get links failed: {e}, url: {url}')
              
        return links


if __name__ == '__main__':
    #lc = LinkCollector(platform='kbb', zip_code=48103, radius=200, sqs_queue_id='ev_test_sqs_queue')
    #lc = LinkCollector(platform='ebay', zip_code=48103, radius=200, sqs_queue_id='ev_test_sqs_queue')
    lc = LinkCollector(platform='craigslist', zip_code=48103, radius=200, sqs_queue_id='ev_test_sqs_queue')

    lc.get_links()
