# necessary imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time
import os
import schedule
import random

# constant variables (change if needed)
USERNAME = ""        # advantech email
PASSWORD = ""                     # govwin password
SEARCH_KEY = "Lockheed Martin"                  # company
MIN_DAYS = 180                                  # lower bound for oppys in days
MAX_DAYS = 720                                  # upper bound for oppys in days
# maybe something that checks with NAICS codes

# Function definition to generate random numbers within range (used for times)
def randint(i, j):
    return random.uniform(i, j)

# Function definition for entire bot process - allows for scheduling
def bot():
    options = Options()
    options.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.maximize_window()

    # initialize into govwin
    driver.get('https://iq.govwin.com/cas/login?service=https://iq.govwin.com/neo/myGovwin')
    time.sleep(1)

    # login
    email = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/form/div/div/input') #updated
    email.send_keys(USERNAME) # replace with user credentials

    driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/form/div/span/input[1]').click() #updated
    time.sleep(1)

    pswd = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/form/div/div[2]/input') #updated
    pswd.send_keys(PASSWORD) # replace with user credentials

    driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/form/div/span/input[1]').click() #updated
    time.sleep(2) # click login

    #try: #not sure what this does at all
    #    driver.find_element_by_xpath('/html/body/div[12]/div/button').click()
    #except Exception:
    #    print('No welcome message')
    search = driver.find_element_by_xpath('/html/body/div[1]/header/div[2]/div[2]/div[1]/form/div/input') #updated
    search.send_keys(SEARCH_KEY + Keys.ENTER) # search for specific keywords
    time.sleep(randint(1, 4))
    driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[2]/div/div[2]/div[11]/div[2]/ul/li[1]/a[2]').click() # this must be changed based on the company (updated)
    # driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[1]/ul[2]/li[1]/ul/li/a').click() # this removes keywords
    time.sleep(randint(1, 4))
    link_count = 2
    main_window = driver.current_window_handle
    
    # option[4] is soliciation date 
    sort_by_sol_date = driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[1]/div/div[3]/div[1]/div/select[1]/option[4]') 
    sort_by_sol_date.click()
    time.sleep(0.5)
    # option[1] is new-old
    sort_new_old = driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[1]/div/div[3]/div[1]/div/select[5]/option[1]')
    sort_new_old.click()
    time.sleep(0.5)

    while (link_count < 102): # loop to go into each contract, check location and date, and if in range and in SD or unspecified, flag the op. Will loop through for a while, best to manually exit
        print("-------")
        # selects the drop down menu for each opportunity to flag it
        # cur = driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[1]/div/div[5]/div[2]/div/div[3]/div/div[2]/table/tbody/tr[' + str(link_count) +']/td[4]/a') #maybe broken
        """
        process:
        1. check if a given opportunity is already marked
        if class is markIt unMark
        data-current-level = "100"
        text = 100 or some other
        2. if not, check if the date is within the valid range
        mark it based on a priority level
        """

        """
        previous string to contatenate 
        add onto the rest

        dates
        /html/body/div[4]/div[3]/div[1]/div/div[5]/div[5]/div/div[2]/div[2]/div[2]/table/tbody/tr[1]/td
        /html/body/div[4]/div[3]/div[1]/div/div[5]/div[5]/div/div[3]/div[2]/div[2]/table/tbody/tr[1]/td
        /html/body/div[4]/div[3]/div[1]/div/div[5]/div[5]/div/div[5]/div[2]/div[2]/table/tbody/tr[1]/td

        """

        # mark = driver.find_element_by_class_name
        # drop down menu menu text 
        cur = driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[1]/div/div[5]/div[5]/div/div[' + str(link_count) + ']/div[2]/div[1]/table/tbody/tr[1]/td/div/div/a')
        marked = int(cur.text) != 100       # marked oportunities have 100 text, unmarked have their priority level
        print(cur.text, marked)
        if (marked):
            link_count += 1
            continue
        else:
            sol_date = driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[1]/div/div[5]/div[5]/div/div[' + str(link_count) + ']/div[2]/div[2]/table/tbody/tr[1]/td').text
            print("Date:", sol_date)
            # date = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[' + str(link_count) + ']/div/div/div[1]/div[1]/div[4]/table/tbody/tr[2]/td').text #updated
            if "deltek estimate" in sol_date.lower():
                # extract month and year from date text
                # all ecent soliciation dates are in format MM/YYYY (if they contain deltek estimate)
                oppy_month = int(sol_date[0:2])
                oppy_year = int(sol_date[3:7])
            else:
                # typically opportunities that are full dates and don't have deltek estimates have deadlines that are already passed
                # oppy_day = date[0:2]
                # oppy_month = date[3:5]
                # oppy_year = date[6:10]
                continue

            # set the 1st of each month as the default day since they aren't available
            diff = (datetime(oppy_year, oppy_month, 1) - datetime.now()).days
            print(diff, "days")
            if diff >= MIN_DAYS and diff <= MAX_DAYS:     # matched the time range
                # mark opportunity as 3 by default, change later if needed
                print("MARK OPPORTUNITY")
                # cur.send_keys(Keys.CONTROL + Keys.RETURN)
                """
                drop downs - cur
                checkboxes (data level 1)
                /html/body/div[4]/div[3]/div[1]/div/div[5]/div[5]/div/div[12]/div[2]/div[1]/table/tbody/tr[1]/td/div/div/div/div/div/span[1]/a[2]
                /html/body/div[4]/div[3]/div[1]/div/div[5]/div[5]/div/div[13]/div[2]/div[1]/table/tbody/tr[1]/td/div/div/div/div/div/span[1]/a[2]

                cur.click()


                """
                time.sleep(randint(0.5, 1))
                checkbox = driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[1]/div/div[5]/div[5]/div/div[' + str(link_count) + ']/div[2]/div[1]/table/tbody/tr[1]/td/div/div/div/div/div/span[1]/a[2]')
                cur.click() 
                time.sleep(randint(0.5, 1))
                checkbox.click()               
                continue
            else:
                print("opportunity not marked")
                link_count += 1
                continue

        # print(str(cur.text), str(marked))

        # drop down menu
        # /html/body/div[4]/div[3]/div[1]/div/div[5]/div[5]/div/div[2]/div[2]/div[2]/table/tbody/tr[1]/td
        # /html/body/div[4]/div[3]/div[1]/div/div[5]/div[5]/div/div[3]/div[2]/div[2]/table/tbody/tr[1]/td
        # /html/body/div[4]/div[3]/div[1]/div/div[5]/div[5]/div/div[2]/div[2]/div[1]/table/tbody/tr[1]/td/div/div/a
        # /html/body/div[4]/div[3]/div[1]/div/div[5]/div[5]/div/div[3]/div[2]/div[1]/table/tbody/tr[1]/td/div/div/a
        # /html/body/div[4]/div[3]/div[1]/div/div[5]/div[5]/div/div[5]/div[2]/div[1]/table/tbody/tr[1]/td/div/div/a
        # /html/body/div[4]/div[3]/div[1]/div/div[5]/div[5]/div/div[ + link_count + ]/div[2]/div[1]/table/tbody/tr[1]/td/div/div/a
        # print(cur)
        """
        sort opportunities by solicitation date - new to old

        div class markingLevelsContainer
        data-level = 1, 2, 3, 4, 5
        """


        # old code
        # cur.send_keys(Keys.CONTROL + Keys.RETURN)
        # driver.switch_to.window(driver.window_handles[1]) # not sure what this is doing

        # date = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[3]/div/div/div[1]/div[1]/div[4]/table/tbody/tr[2]/td').text #updated
        # if '2021' in date or '2022' in date:
        #     print('test')
        #     try: #search to see if there is a location for the contract...if just U.S., flag it anyways, else try for SD??
        #         loc = driver.find_element_by_xpath(
        #             '/html/body/div[4]/div[4]/div/div[3]/div/div/div[1]/div[1]/div[4]/table/tbody/tr[13]/td/div/ul/li').text #probably pretty broken (updated tho)
        #         print(loc)
        #         time.sleep(2)
        #         #if ',' not in loc or 'San Diego' in loc:
        #         #    #flag
        #         #    driver.find_element_by_xpath('/html/body/div[4]/div[3]/nav[2]/ul/li[1]/div/div/div[1]/a').click()
        #         #    time.sleep(2)
        #         #    driver.find_element_by_xpath('/html/body/div[4]/div[3]/nav[2]/ul/li[1]/div/div/div[1]/div/div/div/span[1]/a[6]').click()
        #     except Exception:
        #         print('WRONG LOC')
        # elif '2020' in date:
        #     if '9' in date or '10' in date or '11' in date or '12' in date:
        #         print('test2')
        #         try:  # search to see if there is a location for the contract...if just U.S., flag it anyways, else try for SD??
        #             loc = driver.find_element_by_xpath(
        #                 '/html/body/div[4]/div[4]/div/div[3]/div/div/div[1]/div[1]/div[4]/table/tbody/tr[13]/td/div/ul/li').text #probably pretty broken (updated tho)
        #             print(loc)
        #             time.sleep(2)
        #             #if ',' not in loc or 'San Diego' in loc: #united states check is failing - not sure why. Need to debug through it and make sure it matches, maybe check the length
        #             #    # flag
        #             #    driver.find_element_by_xpath(
        #             #        '/html/body/div[4]/div[3]/nav[2]/ul/li[1]/div/div/div[1]/a').click()
        #             #    time.sleep(2)
        #             #    driver.find_element_by_xpath(
        #             #        '/html/body/div[4]/div[3]/nav[2]/ul/li[1]/div/div/div[1]/div/div/div/span[1]/a[6]').click()
        #         except Exception:
        #             print('WRONG LOC')

        driver.close()
        # driver.switch_to.window(main_window) # not sure what this is doing
        link_count += 1

bot()
