# ev_sales

Collecting dataset of past Eletric Vehicles sales from public sources.

Currently processing Ebay listings in ```ebay```.  The process is as follows:
* ```get_links``` queries Ebay site for listings (writes to ```data/links.csv```)
* ```get_data``` queries each listing scrapes product details (writes to ```data/data.json```)
* ```util``` contains helper functions such as BeautifulSoup scraper, Selenium webdriver, data storage, and string manipulation

```ebay_historical``` contains scripts to collect *historical* listings. 
