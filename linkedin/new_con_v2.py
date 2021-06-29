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
    # options.add_argument('--incognito')
    options.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.maximize_window()

    driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
    time.sleep(1)

    # enter login info
    user = driver.find_element_by_xpath('/html/body/div/main/div[2]/div[1]/form/div[1]/input')
    user.send_keys('jack.c.fraser3@gmail.com')
    pswd = driver.find_element_by_xpath('/html/body/div/main/div[2]/div[1]/form/div[2]/input')
    pswd.send_keys('Jandc4ever')
    driver.find_element_by_xpath('/html/body/div/main/div[2]/div[1]/form/div[3]/button').click()
    time.sleep(3)

    # time.sleep(1)
    # # try catch for mobile authentication, seems unnecessary as of now
    # try:
    #     driver.find_element_by_xpath('/html/body/div/div[1]/section/div[2]/div/article/footer/div/div/button').click()
    # except Exception:
    #     print('No auth needed')

    # searcher = driver.find_element_by_xpath('/html/body/div[5]/header/div/div/div/div[1]/div[2]/input')
    # searcher.send_keys('tester')

    # searcher.send_keys(Keys.RETURN)

    
    

    page_count = 20
    keywords_search = 'Booz Allen'
    
    # time.sleep(5)
    # driver.find_element_by_partial_link_text('all people results').click()
    # time.sleep(5)
    while (page_count != 0):
        driver.get('https://www.linkedin.com/search/results/people/?keywords='+ str(keywords_search) +'&origin=CLUSTER_EXPANSION&page='+ str(page_count) +'')
        time.sleep(7)
    #note:10 connections per page
        li_count = 1
        while (li_count != 11):
            try:
                title = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div[1]/div/div[1]/main/div/div/div[2]/ul/li['+ str(li_count) +']/div/div/div[2]/div[1]/div[2]/div/div[1]')
                actions = ActionChains(driver)
                actions.move_to_element(title).perform()
                temp = title.text

                if "Booz Allen" in temp and ("Lead Associate" in temp or "Senior Associate" in temp or "Sr. Associate" in temp or "Vice President" in temp or "Program Manager" in temp or "VP" in temp or "V.P." in temp or "Sr Associate" in temp): # and criteria in temp: #need criteria from pamela
                        name = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div[1]/div/div[1]/main/div/div/div[2]/ul/li[' + str(li_count) +']/div/div/div[2]/div[1]/div[1]/div/span[1]/span/a/span/span[1]')
                        name = str(name.text)
                        print(name)
                        name = name.split(' ')
                        name = name[0]

                        testButton = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div[1]/div/div[1]/main/div/div/div[2]/ul/li['+ str(li_count) +']/div/div/div[3]/div/button/span')
                        
                        testButton = str(testButton.text)
                        if(testButton != "Connect"):
                            if(testButton == "Message"):
                                print("Already connected")
                                li_count += 1
                            else:

                            #to do
                                #driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div[1]/div/div[1]/main/div/div/div[2]/ul/li['+str(li_count)+']/div/div/div[2]/div[1]/div[1]/div/span[1]/span/a/span/span[1]').click()
                                li_count += 1
                                time.sleep(4)
                                # try:
                                    
                                #     driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div/div/div[2]/div/div/main/div/section/div[2]/div[3]/div/a').click()

                                #     msgb = driver.find_element_by_xpath('/html/body/div[5]/aside/div[2]/div[1]/div[4]/div[3]/form/div[3]/div/div/div[1]/p/br')
                                #     time.sleep(2)
                                #     msgb.send_keys(name + '- Advantech has won with BAH for 14+yr as a key small biz HUBZone exclusive to tech & prof services, & fortunate to have BAH VP/Market Leads recommendations. www.advantech-gs.com. Happy to connect & also support you in staying ahead of market needs. R/ Jack 858.705.3069')
                                #     time.sleep(3)
                                #     driver.find_element_by_xpath('/html/body/div[5]/aside/div[2]/div[1]/div[4]/div[3]/form/footer/div[2]/div/button').click()
                                #     driver.execute_script("window.history.go(-1)")

                                #     time.sleep(2)
                                #     li_count += 1
                                
                                # except Exception:
                                #     print('oops')
                                #     driver.execute_script("window.history.go(-1)")
                                #     li_count += 1
                                #     continue
                        else:
                        #clicks on the add a note button
                                driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div[1]/div/div[1]/main/div/div/div[2]/ul/li['+str(li_count)+']/div/div/div[3]/div/button/span').click()
                                driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[1]/span').click()
                                msgb = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/div[1]/textarea')
                                time.sleep(2)
                                msgb.send_keys(name + '- Advantech has won with BAH for 14+yr as a key small biz HUBZone exclusive to tech & prof services, & fortunate to have BAH VP/Market Leads recommendations. www.advantech-gs.com. Happy to connect & also support you in staying ahead of market needs. R/ Jack 858.705.3069')
                                time.sleep(3)
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
        page_count += 1
bot()
