
from selenium.webdriver.common.by import By
import time

import pandas as pd

from util import get_driver


def get_ebay_sales_links(driver, keyword):

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

# testing
#ev_names = ev_names[:2]

for ev_name in ev_names:
    try:
        links = get_ebay_sales_links(driver, ev_name)
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

driver.close()
print('done!')
