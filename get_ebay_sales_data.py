import time, json
import pandas as pd

from util import get_driver, append_to_json


def get_sales_data(driver, item_link):
    info = {}

    driver.get(item_link)

    price = driver.find_element_by_css_selector('div[class*="vi-price"]').text
    info['price'] = price

    labels = driver.find_elements_by_css_selector('div[class*="labels-content"]')
    values = driver.find_elements_by_css_selector('div[class*="values-content"]')
    labels_text = list(map(lambda x: x.text, labels))
    values_text = list(map(lambda x: x.text, values))
    info.update(dict(zip(labels_text, values_text)))

    # TODO: Get descriptions (cannot get inner HTML)
    # description = driver.find_element_by_css_selector('div[data-testid="d-item-description"]').text
    # info['description'] = description

    return info


sales_links = pd.read_csv('./data/ebay_ev_sales.csv')['link']

# testing
sales_links = sales_links[1:10]

driver = get_driver()
for sl in sales_links:
    print(f'\nsales link: {sl}')
    try:
        data_dict = get_sales_data(driver, sl)
        data_dict['item_link'] = sl
        print(f'data: {data_dict}')

        append_to_json('./data/ebay_ev_data.json', data_dict)

    except Exception as e:
        print(f'failed')
        print(e)

driver.close()
print('\ndone!')
