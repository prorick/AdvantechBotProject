# necessary imports
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import time
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Function definition for entire bot process, allows it to be called if scheduling is necessary
def bot():
    # lists initialized for storing data of employees
    names = []
    abouts = []
    expers = []
    locs = []
    titles = []
    
    # set paths for webdriver + initialize
    options = Options()
    options.add_argument('--incognito')
    options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    
    driver.maximize_window()
    
    # load into linkedin site 
    driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
    time.sleep(1)
    
    # enter login info
    user = driver.find_element_by_xpath('/html/body/div/main/div[2]/form/div[1]/input')
    user.send_keys('EMAIL') # REPLACE WITH USER EMAIL
    pswd = driver.find_element_by_xpath('/html/body/div/main/div[2]/form/div[2]/input')
    pswd.send_keys('PASSWORD') # REPLACE WITH USER PASSWORD
    
    # submit form, try catch because it was having issues finding the button by a single absolute path
    try:
        driver.find_element_by_xpath('/html/body/div/main/div[2]/form/div[4]').click()
    except Exception:
        try:
            driver.find_element_by_xpath('/html/body/div/main/div[2]/form/div[3]/button').click()
        except Exception:
            driver.find_element_by_xpath('//*[@id="app__container"]/main/div[2]/form/div[4]/button').click()
            try:
                driver.find_element_by_link_text('Sign in').click()
            except Exception:
                quit()
    
    time.sleep(1)
    # try catch for mobile authentication, seems unnecessary as of now
    try:
        driver.find_element_by_xpath('/html/body/div/div[1]/section/div[2]/div/article/footer/div/div/button').click()
    except Exception:
        print('No auth needed')
    
    # keep track of what page script is on
    page_tracker = 1
    
    # boolean li query, must first search in google then copy search address
    site = 'QUERY LINK AFTER SEARCHED'
    driver.get(site)
    
    # main loop for handling bot
    while True: 
        # set the main window and intialize a random user agent to avoid captchas
        main_window = driver.current_window_handle
        link_counter = 0
        ua = UserAgent()
        userAgent = ua.random
        print(userAgent)
    
        time.sleep(1)
        
        # find all clickable links, the iterate though them
        data = driver.find_elements_by_partial_link_text('linkedin.com')
    
        for data[link_counter] in data:
            data = driver.find_elements_by_partial_link_text('linkedin.com')
            data[link_counter].send_keys(Keys.CONTROL + Keys.RETURN) # open in new tab
    
            driver.switch_to.window(driver.window_handles[1]) # switch to new tab
    
            time.sleep(2)
    
            # Block to figure out their name: if both attempts fail, go to essentially end of task loop and resume
            # process or move on to next page
            try:
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
            
            # block to find location - if not specificied or undistinguishable, leave empty and move on
            try:
                location = driver.find_element_by_xpath(
                    '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[1]/ul[2]/li[1]').text
            except:
                location = ""
    
            # block to make sure ths is a real person account and create an anchor for later (to a specific point on their profile page)
            try:
                head = driver.find_element_by_xpath(
                    '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[1]/section/header/h2')
            except Exception:
                try:
                    head = driver.find_element_by_xpath(
                        '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[6]/span/div/section/div[1]/section/header/h2')
                except Exception:
                    ua = UserAgent()
                    userAgent = ua.random
                    print(userAgent)
                    driver.close()
                    driver.switch_to.window(main_window)
                    link_counter += 1
                    time.sleep(1)
                    break
            
            # block to expand the about section
            try:
                driver.find_element_by_xpath(
                    '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[3]/section/p/span[3]/span/a').click()
            except Exception:
                print('about expanded')
               
            # now, grab about text
            try:
                about = driver.find_element_by_xpath(
                    '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[3]/section/p/span[1]')
                about = str(about.text)
            except Exception:
                about = "EMPTY"
            
            # move to head anchor
            actions = ActionChains(driver)
            actions.move_to_element(head).perform()
            
            # blovk to grab their title
            try:
                title = driver.find_element_by_xpath(
                    '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[1]/section/ul/li[1]/section/div/div/a/div[2]/h3')
                title = title.text
            except Exception:
                try:
                    title = driver.find_element_by_xpath(
                        '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[6]/span/div/section/div[1]/section/ul/li[1]/section/ul/li[1]/div/div/div/div/div/div/h3/span[2]')
                    title = title.text
                except Exception:
                    print('Now what...')
            
            # block to expand experience tab
            try:
                driver.find_element_by_xpath(
                    '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[1]/section/ul/li[1]/section/div/div/div/p/span/button').click()
            except Exception:
                print('No see more button')
                
            # now, try to grab the experience text
            try:
                experience = driver.find_element_by_xpath(
                    '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[1]/section/ul/li[1]/section/div/div/div/p')
                experience = experience.text
            except Exception:
                print('No experience for this chum')
                experience = ""
            
            # convert to string for data normalization
            con_name = str(con_name.text)
    
            # print fields for testing, then append them to the lists
            print(con_name)
            print(location)
            print(title)
            print(about)
            print(experience)
    
            expers.append(experience)
            abouts.append(about)
            names.append(con_name)
            locs.append(location)
            titles.append(title)
            
            # initialize new user agent for anonymity, then go back to main window and close any extra tabs
            ua = UserAgent()
            userAgent = ua.random
            print(userAgent)
            driver.close()
            driver.switch_to.window(main_window)
            link_counter += 1
            time.sleep(1)
    
        # block to continue to next page on google search, < num pages to go through. Default cap is 25, change here if less is desired
        if page_tracker < 25: 
            time.sleep(.75 * 60) # sleep time, helps avoid google captchas 
            driver.find_element_by_xpath(
                '/html/body/div[8]/div[2]/div[10]/div[1]/div[2]/div/div[5]/div[2]/span[1]/div/table/tbody/tr/td[12]/a/span[2]').click()
            page_tracker += 1
            time.sleep(1)
            main_window = driver.current_window_handle
        else:
            driver.quit()
            break
    
    # convert lists to pandas series so they can be placed in a dataframe for storage
    names_ser = pd.Series(names)
    exp_ser = pd.Series(expers)
    about_ser = pd.Series(abouts)
    locs_ser = pd.Series(locs)
    titles_ser = pd.Series(titles)
    
    frame = {'Name': names_ser, 'Description/Bio': about_ser, 'Location': locs_ser, 'Title': titles_ser, 'Expertise (subj matter)': exp_ser}
    final = pd.DataFrame(frame)
    final.to_csv('DESIRED NAME.csv') # specify file name here
    
    time.sleep(10)
    
    # sleep for 10 seconds then continue on to next batch of people. If no other queries are necessary, comment out the next blocks of code. 
    
    names = []
    abouts = []
    expers = []
    locs = []
    titles = []
    # set paths for webdriver + initialize
    options = Options()
    options.add_argument('--incognito')
    options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
    driver_path = "C:/Users/Matt Turi/Downloads/chromedriver_win32/chromedriver.exe"
    driver = webdriver.Chrome(options=options, executable_path=driver_path)
    
    driver.maximize_window()
    
    driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
    time.sleep(1)
    
    # enter login info
    user = driver.find_element_by_xpath('/html/body/div/main/div[2]/form/div[1]/input')
    user.send_keys('EMAIL')
    pswd = driver.find_element_by_xpath('/html/body/div/main/div[2]/form/div[2]/input')
    pswd.send_keys('PASSWORD')
    
    # submit form, try catch because it was having issues finding the button by a single absolute path
    try:
        driver.find_element_by_xpath('/html/body/div/main/div[2]/form/div[4]').click()
    except Exception:
        try:
            driver.find_element_by_xpath('/html/body/div/main/div[2]/form/div[3]/button').click()
        except Exception:
            driver.find_element_by_xpath('//*[@id="app__container"]/main/div[2]/form/div[4]/button').click()
            try:
                driver.find_element_by_link_text('Sign in').click()
            except Exception:
                quit()
    
    time.sleep(1)
    # try catch for mobile authentication, seems unnecessary as of now
    try:
        driver.find_element_by_xpath('/html/body/div/div[1]/section/div[2]/div/article/footer/div/div/button').click()
    except Exception:
        print('No auth needed')
    
    page_tracker = 1
    
    # boolean li query, must first search in google then copy search address
    site = 'GOOGLE QUERY'
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
    
        for data[link_counter] in data:
            data = driver.find_elements_by_partial_link_text('linkedin.com')
            data[link_counter].send_keys(Keys.CONTROL + Keys.RETURN)
    
            driver.switch_to.window(driver.window_handles[1])
    
            time.sleep(2)
    
            # Block to figure out their name: if both attempts fail, go to essentially end of task loop and resume
            # process or move on to next page
            try:
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
    
            try:
                location = driver.find_element_by_xpath(
                    '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[1]/ul[2]/li[1]').text
            except:
                location = ""
    
            try:
                head = driver.find_element_by_xpath(
                    '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[1]/section/header/h2')
            except Exception:
                # driver.execute_script("window.scrollTo(0, 400)")
                try:
                    head = driver.find_element_by_xpath(
                        '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[6]/span/div/section/div[1]/section/header/h2')
                except Exception:
                    ua = UserAgent()
                    userAgent = ua.random
                    print(userAgent)
                    driver.close()
                    driver.switch_to.window(main_window)
                    link_counter += 1
                    time.sleep(1)
                    break
    
            try:
                driver.find_element_by_xpath(
                    '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[3]/section/p/span[3]/span/a').click()
            except Exception:
                print('about expanded')
            try:
                about = driver.find_element_by_xpath(
                    '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[3]/section/p/span[1]')
                about = str(about.text)
            except Exception:
                about = "EMPTY"
    
            actions = ActionChains(driver)
            actions.move_to_element(head).perform()
    
            try:
                title = driver.find_element_by_xpath(
                    '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[1]/section/ul/li[1]/section/div/div/a/div[2]/h3')
                title = title.text
            except Exception:
                try:
                    title = driver.find_element_by_xpath(
                        '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[6]/span/div/section/div[1]/section/ul/li[1]/section/ul/li[1]/div/div/div/div/div/div/h3/span[2]')
                    title = title.text
                except Exception:
                    print('Now what...')
    
            try:
                driver.find_element_by_xpath(
                    '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[1]/section/ul/li[1]/section/div/div/div/p/span/button').click()
            except Exception:
                print('No see more button')
            try:
                experience = driver.find_element_by_xpath(
                    '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[1]/section/ul/li[1]/section/div/div/div/p')
                experience = experience.text
            except Exception:
                print('No experience for this chum')
                experience = ""
    
            con_name = str(con_name.text)
    
            print(experience)
            print(about)
            print(con_name)
    
            expers.append(experience)
            abouts.append(about)
            names.append(con_name)
            locs.append(location)
            titles.append(title)
    
            ua = UserAgent()
            userAgent = ua.random
            print(userAgent)
            driver.close()
            driver.switch_to.window(main_window)
            link_counter += 1
            time.sleep(1)
    
        # block to continue to next page on google search, <num pages to go through. Default cap is 25, change here if less is desired
        if page_tracker < 25:  
            time.sleep(.75 * 60)
            driver.find_element_by_xpath(
                '/html/body/div[8]/div[2]/div[10]/div[1]/div[2]/div/div[5]/div[2]/span[1]/div/table/tbody/tr/td[12]/a/span[2]').click()
            page_tracker += 1
            time.sleep(1)
            main_window = driver.current_window_handle
        else:
            driver.quit()
            break
    
    names_ser = pd.Series(names)
    exp_ser = pd.Series(expers)
    about_ser = pd.Series(abouts)
    locs_ser = pd.Series(locs)
    titles_ser = pd.Series(titles)
    
    frame = {'Name': names_ser, 'Description/Bio': about_ser, 'Location': locs_ser, 'Title': titles_ser, 'Expertise (subj matter)': exp_ser}
    final = pd.DataFrame(frame)
    final.to_csv('NAME HERE.csv')
    
    time.sleep(10)

    names = []
    abouts = []
    expers = []
    locs = []
    titles = []
    # set paths for webdriver + initialize
    options = Options()
    options.add_argument('--incognito')
    options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
    driver_path = "C:/Users/Matt Turi/Downloads/chromedriver_win32/chromedriver.exe"
    driver = webdriver.Chrome(options=options, executable_path=driver_path)

    driver.maximize_window()

    driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
    time.sleep(1)

    # enter login info
    user = driver.find_element_by_xpath('/html/body/div/main/div[2]/form/div[1]/input')
    user.send_keys('EMAIL')
    pswd = driver.find_element_by_xpath('/html/body/div/main/div[2]/form/div[2]/input')
    pswd.send_keys('PASSWORD')

    # submit form, try catch because it was having issues finding the button by a single absolute path
    try:
        driver.find_element_by_xpath('/html/body/div/main/div[2]/form/div[4]').click()
    except Exception:
        try:
            driver.find_element_by_xpath('/html/body/div/main/div[2]/form/div[3]/button').click()
        except Exception:
            driver.find_element_by_xpath('//*[@id="app__container"]/main/div[2]/form/div[4]/button').click()
            try:
                driver.find_element_by_link_text('Sign in').click()
            except Exception:
                quit()

    time.sleep(1)
    # try catch for mobile authentication, seems unnecessary as of now
    try:
        driver.find_element_by_xpath('/html/body/div/div[1]/section/div[2]/div/article/footer/div/div/button').click()
    except Exception:
        print('No auth needed')

    page_tracker = 1

    # boolean li query, must first search in google then copy search address
    site = ''
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

        for data[link_counter] in data:
            data = driver.find_elements_by_partial_link_text('linkedin.com')
            data[link_counter].send_keys(Keys.CONTROL + Keys.RETURN)

            driver.switch_to.window(driver.window_handles[1])

            time.sleep(2)

            # Block to figure out their name: if both attempts fail, go to essentially end of task loop and resume
            # process or move on to next page
            try:
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

            try:
                location = driver.find_element_by_xpath(
                    '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[1]/ul[2]/li[1]').text
            except:
                location = ""

            try:
                head = driver.find_element_by_xpath(
                    '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[1]/section/header/h2')
            except Exception:
                # driver.execute_script("window.scrollTo(0, 400)")
                try:
                    head = driver.find_element_by_xpath(
                        '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[6]/span/div/section/div[1]/section/header/h2')
                except Exception:
                    ua = UserAgent()
                    userAgent = ua.random
                    print(userAgent)
                    driver.close()
                    driver.switch_to.window(main_window)
                    link_counter += 1
                    time.sleep(1)
                    break

            try:
                driver.find_element_by_xpath(
                    '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[3]/section/p/span[3]/span/a').click()
            except Exception:
                print('about expanded')
            try:
                about = driver.find_element_by_xpath(
                    '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[3]/section/p/span[1]')
                about = str(about.text)
            except Exception:
                about = "EMPTY"

            actions = ActionChains(driver)
            actions.move_to_element(head).perform()

            try:
                title = driver.find_element_by_xpath(
                    '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[1]/section/ul/li[1]/section/div/div/a/div[2]/h3')
                title = title.text
            except Exception:
                try:
                    title = driver.find_element_by_xpath(
                        '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[6]/span/div/section/div[1]/section/ul/li[1]/section/ul/li[1]/div/div/div/div/div/div/h3/span[2]')
                    title = title.text
                except Exception:
                    print('Now what...')

            try:
                driver.find_element_by_xpath(
                    '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[1]/section/ul/li[1]/section/div/div/div/p/span/button').click()
            except Exception:
                print('No see more button')
            try:
                experience = driver.find_element_by_xpath(
                    '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[1]/section/ul/li[1]/section/div/div/div/p')
                experience = experience.text
            except Exception:
                print('No experience for this chum')
                experience = ""

            con_name = str(con_name.text)

            print(experience)
            print(about)
            print(con_name)

            expers.append(experience)
            abouts.append(about)
            names.append(con_name)
            locs.append(location)
            titles.append(title)

            ua = UserAgent()
            userAgent = ua.random
            print(userAgent)
            driver.close()
            driver.switch_to.window(main_window)
            link_counter += 1
            time.sleep(1)

        # block to continue to next page on google search, <num pages to go through. Default cap is 25, change here if less is desired
        if page_tracker < 3:  # page_stop: # 30:
            time.sleep(.75 * 60)
            driver.find_element_by_xpath(
                '/html/body/div[8]/div[2]/div[10]/div[1]/div[2]/div/div[5]/div[2]/span[1]/div/table/tbody/tr/td[5]/a/span[2]').click()
            page_tracker += 1
            time.sleep(1)
            main_window = driver.current_window_handle
        else:
            driver.quit()
            break

    names_ser = pd.Series(names)
    exp_ser = pd.Series(expers)
    about_ser = pd.Series(abouts)
    locs_ser = pd.Series(locs)
    titles_ser = pd.Series(titles)

    frame = {'Name': names_ser, 'Description/Bio': about_ser, 'Location': locs_ser, 'Title': titles_ser,
             'Expertise (subj matter)': exp_ser}
    final = pd.DataFrame(frame)
    final.to_csv('FILE NAME HERE.csv')

bot()
