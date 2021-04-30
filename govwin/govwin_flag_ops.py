# necessary imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import schedule

# Function definition for entire bot process - allows for scheduling
def bot():
    options = Options()
    options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.maximize_window()

    # initialize into govwin
    driver.get('https://iq.govwin.com/cas/login?service=https://iq.govwin.com/neo/myGovwin')
    time.sleep(1)

    # login
    email = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/form/div/div/input')
    email.send_keys('EMAIL') # replace with user credentials

    driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/form/div/span/input[1]').click()
    time.sleep(1)

    pswd = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/form/div/div[2]/input')
    pswd.send_keys('PASSWORD') # replace with user credentials

    driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/form/div/span/input[1]').click()
    time.sleep(2) # click login

    try:
        driver.find_element_by_xpath('/html/body/div[12]/div/button').click()
    except Exception:
        print('No welcome message')

    search = driver.find_element_by_xpath('/html/body/div[1]/header/div[2]/div[2]/div[2]/form/div/input')
    search.send_keys('leidos' + Keys.ENTER) # search for specific keywords. Change leidos here to whatever is necessary
    time.sleep(10)
    driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[2]/div/div[2]/div[11]/div[2]/ul/li[1]/a[2]').click() # this sets incumbent contarctor as leidos for a search field
    time.sleep(10)
    driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[1]/ul[2]/li[1]/ul/li/a').click() # this removes keywords
    time.sleep(10)
    link_count = 2
    main_window = driver.current_window_handle
    while True: # loop to go into each conract, check location and date, and if in range and in SD or unspecified, flag the op. Will loop through for a while, best to manually exit
        cur = driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[1]/div/div[5]/div[5]/div/div['+ str(link_count) + ']/h3/a')
        cur.send_keys(Keys.CONTROL + Keys.RETURN)
        driver.switch_to.window(driver.window_handles[1])

        date = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div[2]/div/div/table/tbody/tr[2]/td').text
        if '2021' in date or '2022' in date:
            print('test')
            try: #search to see if there is a location for the contract...if just U.S., flag it anyways, else try for SD??
                loc = driver.find_element_by_xpath(
                    '/html/body/div[4]/div[4]/div/div[3]/div/div/div[1]/div[1]/div[4]/table/tbody/tr[13]/td/div').text
                print(loc)
                time.sleep(2)
                if ',' not in loc or 'San Diego' in loc:
                    #flag
                    driver.find_element_by_xpath('/html/body/div[4]/div[3]/nav[2]/ul/li[1]/div/div/div[1]/a').click()
                    time.sleep(2)
                    driver.find_element_by_xpath('/html/body/div[4]/div[3]/nav[2]/ul/li[1]/div/div/div[1]/div/div/div/span[1]/a[6]').click()
            except Exception:
                print('WRONG LOC')
        elif '2020' in date:
            if '9' in date or '10' in date or '11' in date or '12' in date:
                print('test2')
                try:  # search to see if there is a location for the contract...if just U.S., flag it anyways, else try for SD??
                    loc = driver.find_element_by_xpath(
                        '/html/body/div[4]/div[4]/div/div[3]/div/div/div[1]/div[1]/div[4]/table/tbody/tr[13]/td/div').text
                    print(loc)
                    time.sleep(2)
                    if ',' not in loc or 'San Diego' in loc: #united states check is failing - not sure why. Need to debug through it and make sure it matches, maybe check the length
                        # flag
                        driver.find_element_by_xpath(
                            '/html/body/div[4]/div[3]/nav[2]/ul/li[1]/div/div/div[1]/a').click()
                        time.sleep(2)
                        driver.find_element_by_xpath(
                            '/html/body/div[4]/div[3]/nav[2]/ul/li[1]/div/div/div[1]/div/div/div/span[1]/a[6]').click()
                except Exception:
                    print('WRONG LOC')

        driver.close()
        driver.switch_to.window(main_window)
        link_count += 1

bot()
