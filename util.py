import json
from os import path
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


def get_selenium_driver():
    adblock_filepath = 'lib/adblock.crx'

    # Can include more chromedrivers if necessary
    driver_path = 'lib/chromedriver_mac64'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--mute-audio')

    # for chrome_argument in chrome_arguments:
    #    chrome_options.add_argument(chrome_argument)

    chrome_options.add_extension(adblock_filepath)
    driver = webdriver.Chrome(driver_path, options=chrome_options)

    return driver


def get_soup(url):
    req = Request(url)
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page, 'html.parser')
    return soup


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


def format_str(s):
    return re.sub("[\n\t]+", '|', s)


def remove_symbols_str(s):
    return re.sub("[|+:,.]", '', s)
