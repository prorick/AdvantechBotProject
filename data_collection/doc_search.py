# necessary imports
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import os

# main function for bot, allows for scheduling
def bot():
    IDS = [] # lsit of identifiers for people - names, emails, etc.
    for op in IDS: # loop through ids
        directory = op.replace('"', '')
        parent_dir = '' # specify download directory here


        path = os.path.join(parent_dir, directory)
        os.mkdir(path)
        path = path.replace('/', '\\')
        print(path)


        # DRIVER WITH SET DOWNLOAD LOCATION
        options = Options()
        options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
        prefs = {"plugins.always_open_pdf_externally": True, 'download.default_directory': str(path)}
        options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        actions = ActionChains(driver)

        driver.maximize_window()

        main_window = driver.current_window_handle
        
        # search through google, download documents that come up besides the leaked bah sheet
        new_op = op + " filetype:pdf"
        driver.get("https://www.google.com/")

        search = driver.find_element_by_xpath('/html/body/div[2]/div[3]/form/div[2]/div[1]/div[1]/div/div[2]/input')
        search.send_keys(new_op + Keys.ENTER)

        time.sleep(1)

        results = driver.find_elements_by_xpath('//*[@id="rso"]/div/div/div/a/div')
        links = driver.find_elements_by_xpath('//*[@id="rso"]/div/div/div/a')
        link_count = 0
        for r in results:
            print(r.text)
            if "jar2" in str(r.text):
                links.pop(0)
                continue
            else:
                actions.key_down(Keys.CONTROL).click(links[link_count]).perform()
                links.pop(0)
                time.sleep(2)
        driver.close()

bot()
