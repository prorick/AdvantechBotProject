# necessary imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time

# Function definition for entire bot process
def bot():
    # set paths for webdriver + initialize
    options = Options()
    options.add_argument('--incognito')
    options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    actions = ActionChains(driver)
    driver.maximize_window()
    
    # load into linkedin
    driver.get('https://www.linkedin.com/')
    time.sleep(1)

    # find + click signin
    driver.find_element_by_xpath('/html/body/nav/div/a[2]').click()
    time.sleep(1)

    # enter login info
    user = driver.find_element_by_xpath('/html/body/div/main/div[2]/form/div[1]/input')
    user.send_keys('EMAIL') # replace with user credentials
    pswd = driver.find_element_by_xpath('/html/body/div/main/div[2]/form/div[2]/input')
    pswd.send_keys('PASSWORD') # replace with user credentials

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

    driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div/aside[1]/div[2]/section/div[2]/div/a[2]/div').click()
    time.sleep(2)

    main_window = driver.current_window_handle
    
    # open linkedin admin page
    driver.execute_script('''window.open("https://www.linkedin.com/mynetwork/?lipi=urn%3Ali%3Apage%3Ad_flagship3_feed%3BNGEpzm4cQvOwXtNhBJIMqA%3D%3D&licu=urn%3Ali%3Acontrol%3Ad_flagship3_feed-nav.mynetwork","_blank");''')
    
    # switch to new tab
    driver.switch_to.window(driver.window_handles[1])

    time.sleep(2)
    
    # block to navigate to the invite new connections to the company li page, filters to only BAH people
    driver.find_element_by_xpath('/html/body/div[8]/div[3]/div/div/div/div/div/aside/div/div/div[1]/section/div/div[1]/a/div/div[1]/li-icon').click()
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[8]/div[3]/div/div/div/div/div/div/div/div/section/div/div[2]/a').click()
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[8]/div[3]/div/div[1]/header/div/div/div[2]/div/div/div[2]/ul/li[2]/form/button').click()
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[8]/div[3]/div/div[1]/header/div/div/div[2]/div/div/div[2]/ul/li[2]/form/div/fieldset/div/ul/li[2]/label/p/span').click()
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[8]/div[3]/div/div[1]/header/div/div/div[2]/div/div/div[2]/ul/li[2]/form/div/fieldset/div/div[2]/button[2]').click()
    time.sleep(2)

    all_names = []

    li_count = 1
    max_names = 96
    while True: # block to invite each person and scroll through the list until the connections limit is reached
        if li_count == 9:
            print('scrolling')
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        temp = driver.find_element_by_xpath(
            '/html/body/div[8]/div[3]/div/div[2]/div/div[2]/div/div/div/div/ul/li[' + str(
            li_count) + ']/div/div/div[2]/a/h3/span/span/span[1]')
        temp = temp.text
        all_names.append(temp)
        li_count += 1
        if len(all_names) > 96:
            print('no more pages')
            driver.switch_to.window(main_window)
            driver.find_element_by_xpath(
                '/html/body/div[7]/div[3]/div/div[6]/main/div[1]/div[3]/div[3]/div[1]/section/footer/button').click()
            time.sleep(2)
            con_box = driver.find_element_by_xpath(
                '/html/body/div[4]/div/div/div[1]/div/div[2]/div/div/div[1]/div/input')
            for name in all_names[:97]:
                con_box.click()
                print(name)
                time.sleep(2)
                con_box.send_keys(name)
                time.sleep(2)
                driver.find_element_by_class_name("org-typeahead-input__typeahead-results-inner").click()
                # driver.find_element_by_xpath(
                #     '/html/body/div[4]/div/div/div[1]/div/div[2]/div/div/div[2]').click()
            time.sleep(15)
            driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/div/button').click()
        else:
            if li_count == 10:
                try:
                    if len(all_names) < 15:
                        driver.find_element_by_xpath(
                            '/html/body/div[8]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[2]/div/button[2]/span').click()
                    else:
                        driver.find_element_by_xpath('/html/body/div[8]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[1]/div/button[2]/span').click()
                    li_count = 1
                    time.sleep(2)
                except Exception:
                    print('no more pages')
                    driver.switch_to.window(main_window)

bot()
