
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import time

import pandas as pd

def get_driver():

    adblock_filepath = 'conf/webdriver/adblock.crx'
    if sys.platform == 'win32':
        driver_path = 'conf/webdriver/chromedriver_mac64.exe'
    elif sys.platform == 'darwin':
        driver_path = 'conf/webdriver/chromedriver_mac64'
    else:
        driver_path = 'conf/webdriver/chromedriver_linux64'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--mute-audio')

    # for chrome_argument in chrome_arguments:
    #    chrome_options.add_argument(chrome_argument)

    chrome_options.add_extension(adblock_filepath)
    driver = webdriver.Chrome(driver_path, options=chrome_options)
    driver.maximize_window()

    return driver


def get_sales_links(driver, keyword):

    formatted_keyword = keyword.replace(' ', '+')
    driver.get(f'https://www.ebay.com/sch/6001/i.html?_from=R40&_nkw={formatted_keyword}+&LH_TitleDesc=1&_sop=-1&LH_Complete=1&LH_Sold=1&_ipg=240')
    time.sleep(5)
    items = driver.find_elements(By.CSS_SELECTOR, 'div[class="s-item__wrapper clearfix"] div[class="s-item__info '
                                                  'clearfix"] a[class=s-item__link]')
    # get_attribute returns None if there's no such attribute
    links = list(map(lambda x: x.get_attribute('href'), items))
    return links


driver = get_driver()

ev_names_df = pd.read_csv('./data/all_evs.csv',header=None)
ev_names = list(ev_names_df[0].values)

# TODO: Place on Github
# TODO: Other search phrases, such as "electric vehicles"

# testing
#ev_names = ev_names[:2]

for ev_name in ev_names:
    try:
        links = get_sales_links(driver, ev_name)
        links_df = pd.DataFrame(data={
            'ev_name': [ev_name for i in range(len(links))],
            'link': links
        })

        print(f'ev_name: {ev_name}')
        print(f'link count: {len(links)}')

        links_df.to_csv('./data/ebay_ev_sales.csv', mode='a',index=False)
    except Exception as e:
        print(f'failed for ev {ev_name}')
        print(e)

# TODO exit the driver!
print('done!')
