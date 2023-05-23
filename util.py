from selenium import webdriver
import sys



def get_driver():

    adblock_filepath = 'conf/webdriver/adblock.crx'
    if sys.platform == 'win32':
        driver_path = 'conf/webdriver/chromedriver_mac64.exe'
    elif sys.platform == 'darwin':
        driver_path = 'conf/webdriver/chromedriver_mac64'
    else:
        driver_path = 'conf/webdriver/chromedriver_linux64'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--mute-audio')

    # for chrome_argument in chrome_arguments:
    #    chrome_options.add_argument(chrome_argument)

    chrome_options.add_extension(adblock_filepath)
    driver = webdriver.Chrome(driver_path, options=chrome_options)
    # driver.maximize_window()

    return driver
