from util import get_selenium_driver, append_to_json
import pandas as pd
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time


def get_sales_data(driver, link):
    driver.get(link)

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

# TODO
#all_item_links = pd.read_csv('./data/links.csv', header=None)[0]
all_item_links = [
    'https://www.kbb.com/cars-for-sale/vehicledetails.xhtml/?listingId=683814570&listingTypes=USED&city=Mount'
    '%20Pleasant&state=MI&zip=48858&searchRadius=200&marketExtension=include&isNewSearch=false&showAccelerateBanner'
    '=false&sortBy=relevance&numRecords=100&firstRecord=300&referrer=%2Fcars-for-sale%2Fused%2Fmount-pleasant-mi'
    '%3FsearchRadius%3D200%26zip%3D48858%26marketExtension%3Dinclude%26isNewSearch%3Dfalse%26showAccelerateBanner'
    '%3Dfalse%26sortBy%3Drelevance%26numRecords%3D100%26firstRecord%3D300&clickType=listing '
]

driver = get_selenium_driver(undetected=True)

start_secs = time.time()
for item_link in all_item_links:
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



