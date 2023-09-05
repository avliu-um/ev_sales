import datetime
import time, json, os
import traceback
import mysql.connector

import pandas as pd

from scraper_util_avliu.util import get_soup, get_soup_text, append_to_json, remove_symbols_str


# Parse a selse link for the data we require, including price, location, and other info
def get_data(url):
    if not url:
        url = os.environ.get('url')

    soup = get_soup(url)
    info = {}

    price = get_soup_text(soup, "span[itemprop='price']", one=True)
    info['price'] = price

    loc_text = soup.select_one('div[class*="ux-labels-values--shipping"]').text
    location = loc_text[loc_text.find('Located in:') + len('Located in:'):].strip()
    info['location'] = location

    general_info = get_soup_text(soup, 'div[class="vi-cviprow"] div[class*="u-flL"]')
    for i in range(0, len(general_info), 2):
        # print(f'i: {i}')
        if i <= 0 and i + 1 <= len(general_info):
            info[remove_symbols_str(general_info[i])] = general_info[i + 1]

    labels_text = get_soup_text(soup, 'div[class*="labels-content"]')
    values_text = get_soup_text(soup, 'div[class*="values-content"]')

    info.update(dict(zip(labels_text, values_text)))

    return info


# Get remaining links to scrape by comparing data/links.csv and the items already in data/data.json
def get_remaining_item_links():
    all_item_links = pd.read_csv('data/links.csv', header=None)[0]

    data_file = './data/data.json'
    if not os.path.exists(data_file):
        return all_item_links

    with open(data_file) as f:
        data = json.load(f)
        scraped_item_ids = list(map(lambda x: x['ebay_item_id'], data))
        all_item_ids = all_item_links.apply(lambda x: x[len('https://www.ebay.com/itm/'):x.find('?')])

        leftover_items = ~all_item_ids.isin(scraped_item_ids)
        leftover = all_item_links[leftover_items]
        leftover = leftover.unique()
        return leftover


if __name__ == '__main__':
    # Make a mysql connection and create a table if it exists
    table_name = 'ebay_ev_sales'
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="root",
      database="ev_mysql"
    )
    mycursor = mydb.cursor()
    mycursor.execute(
        f"CREATE TABLE IF NOT EXISTS {table_name} "
        f"("
        f"vin VARCHAR(255), "
        f"date_accessed date, "
        f"make VARCHAR(255), "
        f"model VARCHAR(255), "
        f"price VARCHAR(255), "
        f"location VARCHAR(255), "
        f"fuel VARCHAR(255),"
        f"ebay_item_id VARCHAR(255),"
        f"PRIMARY KEY (vin, date_accessed)"
        f")"

    )


    leftover_item_links = get_remaining_item_links()
    # testing
    # leftover_item_links = leftover_item_links[:10]

    for item_link in leftover_item_links:
        print(f'\nitem link: {item_link}')
        try:
            data_dict = get_data(item_link)
            data_dict['ebay_item_id'] = item_link[len('https://www.ebay.com/itm/'):item_link.find('?')]
            data_dict['time'] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            print(f'data: {data_dict}')

            # write to json
            append_to_json('data/data.json', data_dict)

            # write to mysql
            sql = f"INSERT IGNORE INTO {table_name} VALUES (%s, now(), %s, %s, %s, %s, %s, %s)"
            val_list = []
            for col in ['vin', 'make', 'model', 'price', 'location', 'fuel', 'ebay_item_id']:
                filt_keys = list(filter(lambda x: col in x.lower(), data_dict.keys()))
                if len(filt_keys) == 0:
                    val_list.append('')
                else:
                    val_list.append(data_dict[filt_keys[0]])
            val = tuple(val_list)
            mycursor.execute(sql, val)
            mydb.commit()

        except Exception as e:
            print(f'failed')
            traceback.print_exc()
            print(e)

    print('\ndone!')
