import pandas as pd
from util import get_soup, get_soup_text, append_to_json
import traceback


# Parse a sales link for the data we require
def get_sales_data(link):
    soup = get_soup(link)
    info = {}

    # adding post metadata - id, timestamp, expire time
    id_css = 'div[class="postinginfos"] p[class="postinginfo"]'
    info['post_id'] = soup.select_one(id_css).text.split(': ')[1]
    
    info['post_datetime'] = soup.time.get('datetime')
    info['post_expire'] = soup.head.find('meta', {'name': 'robots'}).get('content').split(': ')[1]
    
    # get listing attributes
    info_list = get_soup_text(soup, 'div[class=mapAndAttrs] p[class=attrgroup] span')
    for item in info_list:
        sep_idx = item.find(':')
        if sep_idx > 0:
            info[item[:sep_idx].strip()] = item[sep_idx+1:].strip()
        else:
            if 'other' in info.keys():
                info['other'] += f'|{item}'   #Q for Alex !!! this seems to be make, model and year
            else:
                info['other'] = item
                
    
    # adding price, listing geo attributes
    json_css = 'script[id="ld_posting_data"]'
    data = soup.select_one(json_css)
    info.update(json.loads(data.get_text(strip=True)))
    
    # adding saler free-form text and url
    body_css = 'section[id="postingbody"]'
    text = soup.select_one(body_css).get_text()
    info['seller_notes'] = re.sub('[\\n]+', ' ', text).strip()

    info['url'] = link

    return info


all_item_links = pd.read_csv('./data/links.csv', header=None)[0]  #need to update this, how do we want to keep track of links

for item_link in all_item_links:

    try:
        data_dict = get_sales_data(item_link)
        print(f'data: {data_dict}')
        append_to_json('data/data.json', data_dict)      # maybe get sales check post date or only new links from day before?
    except Exception as e:
        print(f'failed')
        traceback.print_exc()
        print(e)

print('\ndone!')
