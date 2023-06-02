import pandas as pd
from util import get_soup, get_soup_text, append_to_json
import traceback


# Parse a selse link for the data we require
def get_sales_data(link):
    soup = get_soup(link)
    info = {}

    info_list = get_soup_text(soup, 'div[class=mapAndAttrs] p[class=attrgroup] span')
    for item in info_list:
        sep_idx = item.find(':')
        if sep_idx > 0:
            info[item[:sep_idx].strip()] = item[sep_idx+1:].strip()
        else:
            if 'other' in info.keys():
                info['other'] += f'|{item}'
            else:
                info['other'] = item

    return info


all_item_links = pd.read_csv('./data/links.csv', header=None)[0]

for item_link in all_item_links:

    try:
        data_dict = get_sales_data(item_link)
        print(f'data: {data_dict}')
        append_to_json('data/data.json', data_dict)
    except Exception as e:
        print(f'failed')
        traceback.print_exc()
        print(e)

print('\ndone!')
