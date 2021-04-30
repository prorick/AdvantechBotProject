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
    options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

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

    driver.find_element_by_xpath('/html/body/div[7]/header/div[2]/nav/ul/li[2]/a/span').click()
    time.sleep(5)
    driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div/div/div/aside/div/div/div[1]/section/div/div[1]/a').click()
    time.sleep(3)
    # need a way to both A: scroll through every single connection  B: search for specific line in header of title

    # NEED CRITERIA AND MESSAGE TO SEND

    li_count = 11
    while True:
        try:
            title = driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div/div/div/div/div/div/section/ul/li[' + str(li_count) + ']/div[1]/a/span[4]')
            actions = ActionChains(driver)
            actions.move_to_element(title).perform()
            temp = title.text
            # if li_count < 123:
            #     li_count += 1
            #     continue
            if "Booz Allen" in temp and ("Lead Associate" in temp or "Senior Associate" in temp or "Sr. Associate" in temp) and ("Vice President" not in temp or "Program Manager" not in temp): # and criteria in temp: #need criteria from pamela
                    name = driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div/div/div/div/div/div/section/ul/li[' + str(li_count) + ']/div[1]/a/span[2]')
                    name = str(name.text)
                    print(name)
                    name = name.split(' ')
                    name = name[0]
                    driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div/div/div/div/div/div/section/ul/li[' + str(li_count) + ']/div[2]/div[1]/button/span[1]').click()
                    msgb = driver.find_element_by_xpath('/html/body/div[7]/aside/div[2]/div[1]/form/div[3]/div/div[1]/div[1]')
                    time.sleep(2)
                    msgb.send_keys(name + '- Glad to connect here. Advantech proudly continues to receive accolades from BAH VPs and PMs as your Technical & Professional Services HUBZone teammate for over 14 years, having supported BAH on 40+ national contracts, which is the reason our organization mirrors Booz Allen.\nPlease take a look at us at: http://advantech-gs.com.\n\nWe help Booz win by adding the hard to meet HUBZone goals; as you know, HUBZones in the professional service sector are very rare, so we are proud to provide competence and excellence in services, a differentiation that adds value to your team!\n\nWe\'re very proud of our reputation providing successful staff and contract management to support BAH, and I\'ve linked a reference here for you, if you\'d like to see what others at BAH have to say.\nhttps://www.linkedin.com/posts/advantech-gs-enterprises-inc_activity-6719290412378537984-2u8g\n\nPlease let me know what other information we can provide, or if you\'d like to have a quick call re: how else we can help you.\n\nMy email address is jcfraser@advantechglobal.org, and my cell number is 858.705.3069.\n\nThank you for your continued support!\nVery respectfully,\nJack Fraser, President & CEO\n')
                    time.sleep(2)
                    driver.find_element_by_xpath('/html/body/div[7]/aside/div[2]/div[1]/form/footer/div[2]/div[1]/button').click()
                    time.sleep(2)
                    driver.find_element_by_xpath('/html/body/div[7]/aside/div[2]/header/section[2]/button[2]').click()
                    li_count += 1
            else:
                li_count += 1
        except Exception:
            print('failed to find title')
            li_count += 1
            continue

bot()

