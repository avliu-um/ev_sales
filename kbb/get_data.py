from scraper_util_avliu.util import get_selenium_driver, append_to_json, get_soup, find_in_dict
import pandas as pd
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import time
import re
import json
import os


# Parse a selse link for the data we require, including price, location, and vin
def get_data(url):
    if not url:
        url = os.environ.get('url')

    driver = get_selenium_driver(undetected=True)
    driver.get(url)

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
    vin = comment[vin_idx:vin_idx+vin_length]

    price = driver.find_element(By.CSS_SELECTOR, 'div[data-cmp="pricing"]').text.lower()
    title = driver.find_element(By.CSS_SELECTOR, 'h1[data-cmp="heading"]').text.lower()

    url = driver.current_url
    state_idx = url.find('&state=') + len('&state=')
    state = url[state_idx:state_idx+2]

    # fuel type and mileage are in a table and the only sensible labels don't actually contain the text we want;
    # hence, the workaround by searching the table text itself
    list_elem = driver.find_element(By.CSS_SELECTOR, 'div[data-cmp="section"]').text.lower()
    words = re.split('[\n ]', list_elem)

    engine_idx = words.index('engine')-1
    engine = words[engine_idx].strip()

    miles_idx = words.index('miles')-1
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


if __name__ == '__main__':

    all_item_links = pd.read_csv('./data/links.csv', header=None)[0]

    start_secs = time.time()
    for item_link in all_item_links:
        print(f'processing link: {item_link}')
        try:
            data_dict = get_data(item_link)
            print(f'data: {data_dict}')
            append_to_json('data/data.json', data_dict)
        except Exception as e:
            print(f'failed')
            traceback.print_exc()
            print(e)
    end_secs = time.time()
    print('\ndone!')
    print(f'took {end_secs - start_secs} seconds')



