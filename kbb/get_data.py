from util.util import get_selenium_driver, append_to_json
import pandas as pd
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import time


# Parse a selse link for the data we require, including price, location, and vin
def get_sales_data(driver, link):
    driver.get(link)

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
    comment = driver.find_element(By.CSS_SELECTOR, 'div[id="sellerComments"] div[data-cmp="heading"]').text

    vin_idx = comment.lower().find('vin: ') + len('vin: ')
    # https://www.lithia.com/research/how-to/how-to-decode-your-cars-vin-number.htm
    vin_length = 17
    vin = comment[vin_idx:vin_idx+vin_length]
    price = driver.find_element(By.CSS_SELECTOR, 'div[data-cmp="pricing"]').text
    title = driver.find_element(By.CSS_SELECTOR, 'h1[data-cmp="heading"]').text

    url = driver.current_url
    state_idx = url.find('&state=') + len('&state=')
    state = url[state_idx:state_idx+2]

    info = {
        'vin': vin,
        'price': price,
        'title': title,
        'state': state
    }
    return info


all_item_links = pd.read_csv('./data/links.csv', header=None)[0]

driver = get_selenium_driver(undetected=True)

start_secs = time.time()
for item_link in all_item_links:
    print(f'processing link: {item_link}')
    try:
        data_dict = get_sales_data(driver, item_link)
        print(f'data: {data_dict}')
        append_to_json('data/data.json', data_dict)
    except Exception as e:
        print(f'failed')
        traceback.print_exc()
        print(e)
end_secs = time.time()
print('\ndone!')
print(f'took {end_secs - start_secs} seconds')



