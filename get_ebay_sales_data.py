import time, json
import pandas as pd

from util import get_soup, get_soup_text, append_to_json


def get_sales_data(item_link):
    soup = get_soup(item_link)
    info = {}

    price = get_soup_text(soup, 'div[class*="vi-price"]', one=True)
    info['price'] = price

    # TODO: Get the Item ID as a key
    # TODO: Location
    # TODO: Confirm sold

    labels_text = get_soup_text(soup, 'div[class*="labels-content"]')
    values_text = get_soup_text(soup, 'div[class*="values-content"]')

    info.update(dict(zip(labels_text, values_text)))

    # TODO: Get descriptions (cannot get inner HTML)
    # description = get_soup_text(soup, 'div[data-testid="d-item-description"]', one=True)
    # info['description'] = description

    return info


sales_links = pd.read_csv('data/ebay_ev_sales_links.csv')['link']

# testing
sales_links = sales_links[1:10]

for sl in sales_links:
    print(f'\nsales link: {sl}')
    try:
        data_dict = get_sales_data(sl)
        data_dict['item_link'] = sl
        print(f'data: {data_dict}')

        append_to_json('data/ebay_ev_sales_data.json', data_dict)

    except Exception as e:
        print(f'failed')
        print(e)

print('\ndone!')
