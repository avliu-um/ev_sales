from util import get_soup, get_soup_text, append_to_csv, remove_symbols_str

# stpos is the center zip code
# sadis is the radius
# _pgn=6


center_zip = 48858
radius = 150
page = 1

backstop = 500
while True:
    url = f'https://www.ebay.com/b/Cars-Trucks/6001?mag=1&_fsrp=0&rt=nc&_sacat=6001&LH_ItemCondition=3000&Model%2520' \
          f'Year=2023%7C2022%7C2021%7C2020%7C2019%7C2018%7C2017%7C2016%7C2015%7C2014%7C2013%7C2012%7C2011%7C2010' \
          f'%7C2009%7C' \
          f'2008%7C2007%7C2006%7C2005%7C2004%7C2003%7C2002%7C2001%7C2000' \
          f'&LH_PrefLoc=99&_stpos={center_zip}&_sadis={radius}&_fspt=1&_pgn={page}'
    print(url)
    soup = get_soup(url)
    link_elements = soup.select('div[class="s-item__wrapper clearfix"] div[class="s-item__info clearfix"] '
                                'a[class=s-item__link]')
    if len(link_elements) == 0 or page > backstop:
        break

    links = []
    for link_elem in link_elements:
        if 'href' in link_elem.attrs.keys():
            links.append(link_elem['href'])

    append_to_csv('./data/links.csv', links)

    page += 1
