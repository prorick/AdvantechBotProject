# this file is extremely similar to the v1, with some slight improvements as well as an updated message with linkes to a li post and website.
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import time
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys

def bot():
    # set paths for webdriver + initialize
    options = Options()
    options.add_argument('--incognito')
    options.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.maximize_window()

    driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
    time.sleep(1)


    # enter login info
    user = driver.find_element_by_xpath('/html/body/div/main/div[2]/div[1]/form/div[1]/input')
    user.send_keys('alanparkerc@gmail.com')
    pswd = driver.find_element_by_xpath('/html/body/div/main/div[2]/div[1]/form/div[2]/input')
    pswd.send_keys('Calikona123')
    driver.find_element_by_xpath('/html/body/div/main/div[2]/div[1]/form/div[3]/button').click()
    time.sleep(3)
    # submit form, try catch because it was having issues finding the button by a single absolute path
    # try:
    #     driver.find_element_by_xpath('/html/body/div/main/div[2]/form/div[4]').click()
    # except Exception:
    #     try:
    #         driver.find_element_by_xpath('/html/body/div/main/div[2]/form/div[3]/button').click()
    #     except Exception:
    #         driver.find_element_by_xpath('//*[@id="app__container"]/main/div[2]/form/div[4]/button').click()
    #         try:
    #             driver.find_element_by_link_text('Sign in').click()
    #         except Exception:
    #             quit()

    time.sleep(1)
    # try catch for mobile authentication, seems unnecessary as of now
    try:
        driver.find_element_by_xpath('/html/body/div/div[1]/section/div[2]/div/article/footer/div/div/button').click()
    except Exception:
        print('No auth needed')

    searcher = driver.find_element_by_xpath('/html/body/div[5]/header/div/div/div/div[1]/div[2]/input')
    searcher.send_keys('team member')

    searcher.send_keys(Keys.RETURN)

    time.sleep(5)
    # driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div/div/div/aside/div/div/div[1]/section/div/div[1]/a').click()
    # time.sleep(3)
    # need a way to both A: scroll through every single connection  B: search for specific line in header of title

    # NEED CRITERIA AND MESSAGE TO SEND


    #note:10 connections per page
    li_count = 1
    while (li_count != 12):
        try:
            title = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div[1]/div/div[1]/main/div/div/div[2]/ul/li[' + str(li_count) + ']/div/div/div[2]/div[1]/div[2]/div/div[1]')
            actions = ActionChains(driver)
            actions.move_to_element(title).perform()
            temp = title.text
            # if li_count < 123:
            #     li_count += 1
            #     continue
            


            if "Booz Allen" in temp and ("Lead Associate" in temp or "Senior Associate" in temp or "Sr. Associate" in temp or "Vice President" in temp or "Program Manager" in temp or "VP" in temp or "V.P." in temp): # and criteria in temp: #need criteria from pamela
                    name = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div[1]/div/div[1]/main/div/div/div[2]/ul/li[' + str(li_count) +']/div/div/div[2]/div[1]/div[1]/div/span[1]/span/a/span/span[1]')
                    name = str(name.text)
                    print(name)
                    name = name.split(' ')
                    name = name[0]

                    driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div[1]/div/div[1]/main/div/div/div[2]/ul/li[' + str(li_count) + ']/div/div/div[2]/div[1]/div[1]/div/span[1]/span/a/span/span[1]').click()


                    driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div[1]/div/div[1]/main/div/div/div[2]/ul/li[' + str(li_count) +']/div/div/div[3]/div/button/span').click()
                    driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[1]/span').click()
                    #this will be the code for checking the blue button
                    # checkButton = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div/div/div[2]/div/div/main/div/section/div[2]/div[3]/div/button')
                    # checkButton = str(checkButton.text)
                    # if(checkButton == "Connect"):
                    #     driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div/div/div[2]/div/div/main/div/section/div[2]/div[3]/div/button').click
                    #     li_count += 1
                    #     driver.execute_script("window.history.go(-1)")
                    # else:
                    #     driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div/div/div[2]/div/div/main/div/section/div[2]/div[3]/div/div[1]/button/span').click()
                    # if ():

                    # if ():


                    #message in 4th position after pending    
                    msgb = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/div[1]/textarea')
                    time.sleep(2)
                    msgb.send_keys(name + '- Glad to connect here. \n')
                    time.sleep(2)
                    driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]/span').click()


                    time.sleep(2)
                    li_count += 1
            else:
                print('incorrect associate')
                li_count += 1
        except Exception:
            print('failed to find title')
            li_count += 1
            continue

bot()

