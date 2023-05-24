import time, json
import traceback

import pandas as pd

from util import get_soup, get_soup_text, append_to_json, remove_symbols_str


def get_sales_data(item_link):
    soup = get_soup(item_link)
    info = {}

    general_info = get_soup_text(soup, 'div[class="vi-cviprow"] div[class*="u-flL"]')
    for i in range(0, len(general_info), 2):
        #print(f'i: {i}')
        if i <= 0 and i+1 <= len(general_info):
            info[remove_symbols_str(general_info[i])] = general_info[i+1]

    labels_text = get_soup_text(soup, 'div[class*="labels-content"]')
    values_text = get_soup_text(soup, 'div[class*="values-content"]')

    info.update(dict(zip(labels_text, values_text)))

    # TODO: Get descriptions (cannot get inner HTML)
    # description = get_soup_text(soup, 'div[data-testid="d-item-description"]', one=True)
    # info['description'] = description

    return info


all_item_links = pd.read_csv('data/ebay_ev_sales_links.csv')['link']

# Get remaining links to scrape
with open('./data/ebay_ev_sales_data.json') as f:
    data = json.load(f)
    scraped_item_ids = list(map(lambda x: x['ebay_item_id'], data))
    all_item_ids = all_item_links.apply(lambda x: x[len('https://www.ebay.com/itm/'):x.find('?')])

    leftover_items = ~all_item_ids.isin(scraped_item_ids)
    leftover_item_links = all_item_links[leftover_items]
    leftover_item_links = leftover_item_links.unique()

# testing
#sales_links = sales_links[1:10]

for item_link in leftover_item_links:
    print(f'\nitem link: {item_link}')
    try:
        data_dict = get_sales_data(item_link)
        data_dict['ebay_item_id'] = item_link[len('https://www.ebay.com/itm/'):item_link.find('?')]

        print(f'data: {data_dict}')

        append_to_json('data/ebay_ev_sales_data.json', data_dict)

    except Exception as e:
        print(f'failed')
        traceback.print_exc()
        print(e)

print('\ndone!')
