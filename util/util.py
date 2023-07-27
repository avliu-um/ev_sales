import json
from os import path
import re
import time

from selenium import webdriver
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib.error

import mysql.connector


def get_selenium_driver(undetected=False):

    adblock_filepath = '../lib/adblock.crx'

    if undetected:
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument('--mute-audio')
        chrome_options.add_extension(adblock_filepath)
        driver = uc.Chrome(options=chrome_options)

    else:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--mute-audio')
        chrome_options.add_extension(adblock_filepath)
        driver = webdriver.Chrome(options=chrome_options)

    return driver


def get_soup(url):
    success = False
    sleep_time = 1
    max_sleep_time = 60 * 5

    req, html_page = None, None
    while not success:
        try:
            req = Request(url)
            html_page = urlopen(req)
            success = True
        except urllib.error.HTTPError as e:
            print(f'error {e.code}')
            if 500 <= e.code <= 599 and sleep_time < max_sleep_time:
                print(f'server error; sleep {sleep_time} seconds')
                time.sleep(sleep_time)
                sleep_time *= 2
            else:
                raise e

    soup = BeautifulSoup(html_page, 'html.parser')
    return soup


# Get all the text within elements found using search_str
def get_soup_text(soup: BeautifulSoup, search_str: str, one=False):
    if one:
        return format_str(soup.select_one(search_str).text)
    else:
        return list(map(lambda x: format_str(x.text), soup.select(search_str)))


def append_to_json(json_file, new_data):
    if path.isfile(json_file):
        with open(json_file, 'r') as fp:
            all_data = json.load(fp)
    else:
        all_data = []

    all_data.append(new_data)

    with open(json_file, 'w') as fp:
        json.dump(all_data, fp, indent=4, separators=(',', ': '))


def append_to_file(file_name, new_data):
    with open(file_name, 'a') as f:
        for data in new_data:
            f.write(f'{data}\n')


# Replace newlines/tabs with the symbol |
def format_str(s):
    return re.sub("[\n\t\r]+", '|', s)


# Remove unnecessary symbols from a string
def remove_symbols_str(s):
    return re.sub("[|+:,.]", '', s)


def write_to_rds():
    # Make a mysql connection and create a table if it exists
    table_name = 'ebay_ev_sales'
    mydb = mysql.connector.connect(
        host="database-1.cchq0zbz9fej.us-east-1.rds.amazonaws.com",
        user="admin",
        password="12345678",
        database="ev-database-test"
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


if __name__ == '__main__':
    write_to_rds()
