# ev_sales

Collecting dataset of past Eletric Vehicles sales from public sources.

Currently processing Ebay data.  The process is as follows:
* ```get_vehicle_data``` scrapes publically-available dataset for names of EV's (writes to ```data/all_ev's.csv```)
* ```get_ebay_sales_links``` queries Ebay site with EV names and the "sold" requirement to get past sales, collects links of each item sold (writes to ```data/ebay_ev_sales_links.csv```)
* ```get_ebay_sales_data``` queries each item sold and scrapes product details (writes to ```data/ebay_ev_sales_data.csv```)
* ```clean_ebay_sales_data``` cleans product details and narrows the data to columns required (writes to ```data/ebay_ev_sales_data_cleaned.csv```)
