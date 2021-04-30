# necessary import packages
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# setting up and intializing webdriver
options = Options()
options.add_argument('--incognito')
options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

driver.maximize_window()

# load into BAH site
driver.get('https://www.boozallen.com/search-results.html#?i=1;q=people;q1=People;sp_k=Boozallen;x1=category')
time.sleep(1)

# three lists to store data grabbed from site
names = []
cats = []
descr = []

# counts for page number ends and and to keep track of what person the script is on
page_count = 1
per_count = 1

# main loop, will grab the specified fields for each employee listed, ends once the pages run out
while True:
    while per_count < 11:
        name = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[3]/div[' + str(per_count) + ']/div/a[1]').text
        desc = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[3]/div[' + str(per_count) + ']/div/p').text
        tag = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[3]/div[' + str(per_count) + ']/div/a[2]/span')

        actions = ActionChains(driver)
        actions.move_to_element(tag).perform()
        
        # replacing special characters 
        tag = tag.text
        desc = str(desc)
        desc = desc.replace('\'', '')
        desc = desc.replace("'", '')
        
        # appending to lists for storage
        names.append(name)
        descr.append(desc)
        cats.append(tag)
        per_count += 1

    per_count = 1
    page_count += 1
    if page_count == 31:
        break
    driver.get('https://www.boozallen.com/search-results.html#?i=1;page=' + str(page_count) + ';q=people;q1=People;sp_k=Boozallen;x1=category')
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, 0);")

# convert lists to pandas series so they can be put into a dataframe
names_ser = pd.Series(names)
cats_ser = pd.Series(cats)
descr_ser = pd.Series(descr)

# save to a .csv file with specified headers
frame = {'Name' : names_ser, 'Category' : cats_ser, 'Description' : descr_ser}
final = pd.DataFrame(frame)
final.to_csv('BAH_PEOPLE.csv')




