import boto3
import datetime
import os
from scraper_util_avliu.util import get_soup, write_to_bucket, get_selenium_driver
import undetected_chromedriver as uc

# TODO: Abstract these functions into util

def get_soup_write(url):
    soup = get_soup(url)
    with open("./output.html", "w", encoding='utf-8') as file:
        # prettify the soup object and convert it into a string
        file.write(str(soup.prettify()))
    write_to_bucket('ev-cloud-testing', './output.html',  'test_write_output.html')

def get_driver_write(url):
    # TODO: Update the get_driver function in util to allow driver path flexibility
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument('--mute-audio')
    # chrome_options.add_extension(adblock_filepath)
    driver = uc.Chrome(options=chrome_options,
                       use_subprocess=True,
                       headless=True,
                       driver_executable_path='/usr/bin/chromedriver')

    #driver = get_selenium_driver(undetected=True)
    driver.get(url)
    html = driver.page_source

    with open("./output.html", "w", encoding='utf-8') as file:
        # prettify the soup object and convert it into a string
        file.write(html)
    write_to_bucket('ev-cloud-testing', './output.html',  'test_write_output.html')


if __name__ == '__main__':
    print(f'pwd: {os.getcwd()}')
    url = ('https://www.ebay.com/itm/256048040264?hash=item3b9da70948:g:fHIAAOSwieBkPtU~&amdata=enc'
           '%3AAQAIAAAAwMYpbKTPPpChZHBE9RJjvHvE%2B%2BxiqM7FG0BDDo0B502BPtXd1VpmOIjdlLj3wxzDc%2Fc'
           '%2Bm36IDbLHZAL4uxZXcIjHRoTmvK0QdYIILdy2AhV1CvRYpsdZg0'
           '%2FXnc2XZrwuw4J7YpWbHJiny14CAnLuEJPnuvvGZV6Hbh7ZJo5WucloyV0Hp3vQUGXNjxK129a9S%2FawYgT5'
           '%2Br0SR81vzzrrEVmXQDD60H4HqzPbhyenwROg9C5hIh3ThQtf01qzjbOvBQ%3D%3D%7Ctkp%3ABk9SR4KS4eGIYg')
    get_driver_write(url)
