# necessary imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import schedule
from subprocess import Popen

# Function definition for entire bot process
def bot():
    # set paths for webdriver + initialize
    options = Options()
    options.add_argument('--incognito')
    options.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.maximize_window()

    driver.get('https://www.linkedin.com/')
    time.sleep(1)

    # find + click signin
    driver.find_element_by_xpath('/html/body/nav/div/a[2]').click()
    time.sleep(1)

    # enter login info
    user = driver.find_element_by_xpath('/html/body/div/main/div[2]/div[1]/form/div[1]/input')
    user.send_keys('alanparkerc@gmail.com') # replace with user credentials
    pswd = driver.find_element_by_xpath('/html/body/div/main/div[2]/div[1]/form/div[2]/input')
    pswd.send_keys('Calikona123')  # replace with user credentials
    driver.find_element_by_xpath('/html/body/div/main/div[2]/div[1]/form/div[3]/button').click()

    # submit form, try catch because it was having issues finding the button by a single absolute path
    #try:
    #    driver.find_element_by_xpath('/html/body/div/main/div[2]/form/div[4]').click()
    #except Exception:
    #    try:
    #        driver.find_element_by_xpath('/html/body/div/main/div[2]/form/div[3]/button').click()
    #    except Exception:
    #        driver.find_element_by_xpath('//*[@id="app__container"]/main/div[2]/form/div[4]/button').click()
    #        try:
    #            driver.find_element_by_link_text('Sign in').click()
    #        except Exception:
    #            quit()

    time.sleep(3)
    # try catch for mobile authentication, seems unnecessary as of now
    #try:
    #    driver.find_element_by_xpath('/html/body/div/div[1]/section/div[2]/div/article/footer/div/div/button').click()
    #except Exception:
    #    print('No auth needed')

    page_tracker = 1

    # boolean li query, must first search in google then copy search address (fill site var)
    site = input("Enter the LinkedIn hack search: ")
    driver.get(site)

    # main loop for handling bot
    while True:
        main_window = driver.current_window_handle
        link_counter = 0
        ua = UserAgent()
        userAgent = ua.random
        print(userAgent)

        time.sleep(1)

        data = driver.find_elements_by_partial_link_text('linkedin.com')

        for data[link_counter] in data: # opens each person in new tab
            data[link_counter].send_keys(Keys.CONTROL + Keys.RETURN)

            driver.switch_to.window(driver.window_handles[1])

            time.sleep(2)

            #probably gonna change this
            try: # block to find their name in linkedin profile, if unable to, move on to next person from search
                con_name = driver.find_element_by_xpath(
                    '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[1]/ul[1]/li[1]')
            except Exception:
                try:
                    con_name = driver.find_element_by_xpath(
                        '/html/body/div[8]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[1]/ul[1]/li[1]')
                except Exception:
                    ua = UserAgent()
                    userAgent = ua.random
                    print(userAgent)
                    driver.close()
                    driver.switch_to.window(main_window)
                    link_counter += 1
                    time.sleep(1)
                    continue

            # block for splicing connection name, obtaining first name only
            con_name = str(con_name.text)
            if ',' in con_name:
                con_name = con_name.split(', ')
                con_name = con_name[0]
            elif '-' in con_name:
                con_name = con_name.split('-')
                con_name = con_name[0]

            if ' ' in con_name:
                con_name = con_name.split(' ')
                con_name = con_name[0]

            print(con_name)

            if len(con_name) < 16: # if their FIRST NAME is longer than 16 characters, its probably wrong so don't send anything
                # Try catch for different linkedin headers to find the conect with a amessage box
                try:
                    driver.find_element_by_xpath(
                        '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[1]/div[2]/div/div/span[1]/div/button').click()
                except Exception:
                    try:
                        driver.find_element_by_xpath(
                            '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[1]/div[2]/div/div/div/div/button/span').click()
                        time.sleep(1)
                        driver.find_element_by_xpath(
                            '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[1]/div[2]/div/div/div/div/div/div/ul/li[4]/div/div/span[1]').click()
                    except Exception:
                        # If a connect button either is not there or is unclickable, just move on
                        ua = UserAgent()
                        userAgent = ua.random
                        print(userAgent)
                        driver.close()
                        driver.switch_to.window(main_window)
                        link_counter += 1
                        time.sleep(1)
                        # block to continue to next page on google search
                        if page_tracker < 190:
                            driver.find_element_by_xpath(
                                '/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[5]/div[2]/span[1]/div/table/tbody/tr/td[' + str(
                                    page_tracker) + ']/a').click()
                            page_tracker += 1
                            time.sleep(1)
                            main_window = driver.current_window_handle
                            continue
                        else:
                            driver.quit()
                            break

                # block for sending a personalized note with connection
                time.sleep(1)
                try:
                    driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[1]/span').click()
                    tbox = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/div[1]/textarea')
                    time.sleep(1)
                    tbox.send_keys('Hi ' + con_name + '- We have common contacts and I thought we might also connect. Advantech has teamed with BAH for 13+ years as the prof services HUBZone: www.advantech-gs.com. We\'re nationwide, and happy to support/provide any info to help you stay ahead of market needs.\nJack 858.705.3069')
                    time.sleep(1)

                    # This the send connection line
                    driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]').click()
                    time.sleep(1)

                except Exception:
                    print('Already Connected')

            ua = UserAgent()
            userAgent = ua.random
            print(userAgent)
            driver.close()
            driver.switch_to.window(main_window)
            link_counter += 1
            time.sleep(1)

        # block to continue to next page on google search, <num pages to go through. Default cap is 25, change here if less is desired
        if page_tracker < 25: 
            time.sleep(2 * 60) # pause to avoid google and linkedin captchas
            driver.find_element_by_xpath(
                '/html/body/div[8]/div[2]/div[10]/div[1]/div[2]/div/div[5]/div[2]/span[1]/div/table/tbody/tr/td[12]/a/span[2]').click()
            page_tracker += 1
            time.sleep(1)
            main_window = driver.current_window_handle
        else:
            driver.quit()
            break
bot()

