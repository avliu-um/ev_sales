import json
import sys
from os import path

from selenium import webdriver


def get_driver():
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


def append_to_json(json_file, new_data):
    if path.isfile(json_file):
        with open(json_file, 'r') as fp:
            all_data = json.load(fp)
    else:
        all_data = []

    all_data.append(new_data)

    with open(json_file, 'w') as fp:
        json.dump(all_data, fp, indent=4, separators=(',', ': '))
