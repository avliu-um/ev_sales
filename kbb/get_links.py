from scraper_util_avliu.util import get_selenium_driver, append_to_file, write_to_sqs

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import os


def get_links(zip_code, radius, sqs_queue_id, page_limit=500):
    if not zip_code or not radius:
        zip_code = os.environ.get('zip_code')
        radius = os.environ.get('radius')
        sqs_queue_id = os.environ.get('sqs_queue_id')

    print(f'running get_links on kbb with zip={zip_code} and radius={radius}')

    driver = get_selenium_driver(undetected=True)

    page = 0
    while True:
        url = f'https://www.kbb.com/cars-for-sale/used/mount-pleasant-mi?searchRadius={radius}&zip={zip_code}&marketExtension' \
              f'=include&isNewSearch=false&showAccelerateBanner=false&sortBy=relevance&numRecords=100&firstRecord={page*100}'
        driver.get(url)

        # Wait for the links to show up, becuase they take a while to render
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-cmp="itemCard"] div[class="item-card-body margin-bottom-auto"] a'))
        )

        link_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-cmp="itemCard"] div[class="item-card-body margin-bottom-auto"] a')

        # When the pages gets out of range, it defaults to the last valid page
        if 'No more results found' in driver.page_source or page > page_limit:
            break
        else:
            links = []
            for link_elem in link_elements:
                try:
                    link = link_elem.get_attribute('href')
                except Exception as e:
                    pass
                if link:
                    links.append(link)
            print(f'{len(links)} links from page {page}')

            # Write the data:
            append_to_file('./data/links.csv', links)
            if sqs_queue_id:
                sqs_messages = [{"service": "data", "platform": "kbb", "url": link} for link in links]
                write_to_sqs(sqs_queue_id, sqs_messages)

        page += 1

    print('\ndone!')


if __name__ == '__main__':
    get_links(48858, 200, 'ev_test_sqs_queue')