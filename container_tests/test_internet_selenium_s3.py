import boto3
import datetime
import os
from util import get_soup, write_to_bucket, get_selenium_driver


# Test the following on the container:
# (1) Internet connection,
# (2) Selenium (i.e. chromedriver installation),
# (3) Writing to S3 (i.e. AWS permissions)

def get_driver_write(url):
    driver = get_selenium_driver(undetected=True)
    driver.get(url)
    html = driver.page_source

    with open("./output.html", "w", encoding='utf-8') as file:
        # prettify the soup object and convert it into a string
        file.write(html)
    write_to_bucket('ev-cloud-testing', './output.html', 'test_write_output.html')


if __name__ == '__main__':
    print(f'pwd: {os.getcwd()}')
    get_driver_write('https://google.com')