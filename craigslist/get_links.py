from util import get_selenium_driver, append_to_csv

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = get_selenium_driver()
cities = [
    'annarbor',
    'battlecreek',
    'centralmich',
    'detroit',
    'flint',
    'grandrapids',
    'holland',
    'jxn',
    'kalamazoo',
    'lansing',
    'monroemi',
    'muskegon',
    'nmi',
    'porthuron',
    'saginaw',
    'southbend',
    'swmi',
    'thumb',
    'up'
]

for city in cities:
    page = 0

    while True:
        city_car_url = f'https://{city}.craigslist.org/search/cta#search=1~list~{page}~0'
        driver.get(city_car_url)

        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[class="titlestring"]'))
        )

        link_elements = driver.find_elements(By.CSS_SELECTOR, 'a[class="titlestring"]')

        # When the pages gets out of range, it defaults to the last valid page
        if driver.current_url == city_car_url:
            links = []
            for link_elem in link_elements:
                link = link_elem.get_attribute('href')
                if link:
                    links.append(link)
            print(f'{len(links)} links from page {page} of city {city}')
            append_to_csv('./data/links.csv', links)
            page += 1
        else:
            break

print('\ndone!')
