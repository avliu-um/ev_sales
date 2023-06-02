from util import get_selenium_driver, append_to_csv

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


driver = get_selenium_driver()


page = 0
backstop = 500
while True:
    url = f'https://www.kbb.com/cars-for-sale/used/mount-pleasant-mi?searchRadius=200&zip=48858&marketExtension' \
          f'=include&isNewSearch=false&showAccelerateBanner=false&sortBy=relevance&numRecords=100&firstRecord={page*100}'
    driver.get(url)

    WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-cmp="itemCard"] div[class="item-card-body margin-bottom-auto"] a'))
    )

    link_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-cmp="itemCard"] div[class="item-card-body margin-bottom-auto"] a')

    # When the pages gets out of range, it defaults to the last valid page
    if 'No more results found' in driver.page_source or 'No results found' in driver.page_source or page>=backstop:
        break
    else:
        links = []
        for link_elem in link_elements:
            link = link_elem.get_attribute('href')
            if link:
                links.append(link)
        print(f'{len(links)} links from page {page}')
        append_to_csv('./data/links.csv', links)
        page += 1

    page += 1

print('\ndone!')
