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
    time.sleep(5)

    page_count = 1
    keywords_search = 'Booz Allen'
    driver.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')
    time.sleep(5)
    li_count = 1
    while (page_count != 0):
                title = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div/div/div/div/div/main/div/section/div[2]/ul/li['+str(li_count)+']/div[1]/a/span[4]')

                actions = ActionChains(driver)
                actions.move_to_element(title).perform()
                temp = title.text

                if "Science Specialist" in temp: # and criteria in temp: #need criteria from pamela
                        name = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div/div/div/div/div/main/div/section/div[2]/ul/li['+str(li_count)+']/div[1]/a/span[2]')
                        name = str(name.text)
                        print(name)
                        name = name.split(' ')
                        name = name[0]

                        driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div/div/div/div/div/main/div/section/div[2]/ul/li['+str(li_count)+']/div[2]/div[1]/button/span[1]').click()
                        msgb = driver.find_element_by_xpath('/html/body/div[5]/aside/div[2]/div[1]/form/div[3]/div/div[1]/div[1]/p')
                        time.sleep(2)
                        msgb.send_keys(name + '-THIS IS A BOT TEST')
                        time.sleep(3)
                        driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]/span').click()

                        time.sleep(2)
                        li_count += 1
                else:
                    print('incorrect associate')
                    li_count += 1

bot()
