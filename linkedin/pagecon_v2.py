from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
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

    driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
    time.sleep(1)

    # enter login info
    user = driver.find_element_by_xpath('/html/body/div/main/div[2]/form/div[1]/input')
    user.send_keys('toro@thenext-step.com')
    pswd = driver.find_element_by_xpath('/html/body/div/main/div[2]/form/div[2]/input')
    pswd.send_keys('GpYE1998**!')

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

#    driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div/aside[1]/div[2]/section/div[2]/div/a[2]/div').click()
    driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div/aside[1]/div[2]/section/div/div[3]/div/a/div').click()
    time.sleep(2)

    main_window = driver.current_window_handle

    driver.execute_script('''window.open("https://www.linkedin.com/mynetwork/?lipi=urn%3Ali%3Apage%3Ad_flagship3_feed%3BNGEpzm4cQvOwXtNhBJIMqA%3D%3D&licu=urn%3Ali%3Acontrol%3Ad_flagship3_feed-nav.mynetwork","_blank");''')

    driver.switch_to.window(driver.window_handles[1])

    time.sleep(2)
    # CONNECTIONS BUTTON
    driver.find_element_by_xpath('/html/body/div[8]/div[3]/div/div/div/div/div/aside/div/div/div[1]/section/div/div[1]/a/div/div[1]/li-icon').click()
    time.sleep(2)
    # SEARCH WITH FILTERS
    driver.find_element_by_xpath('/html/body/div[8]/div[3]/div/div/div/div/div/div/div/div/section/div/div[2]/a').click()
    time.sleep(2)
    # # CURRENT COMPANIES
    # driver.find_element_by_xpath('/html/body/div[8]/div[3]/div/div[1]/header/div/div/div[2]/div/div/div[2]/ul/li[2]/form/button').click()
    # time.sleep(2)

    # driver.find_element_by_xpath(
    #     '/html/body/div[8]/div[3]/div/div[1]/header/div/div/div[2]/div/div/div[2]/ul/li[2]/form/div/fieldset/div/ul/li[2]/label/p/span').click()
    # time.sleep(2)

    driver.find_element_by_xpath('/html/body/div[8]/div[3]/div/div[1]/header/div/div/div[2]/div/div/div[2]/ul/li[3]/form/button').click()
    time.sleep(2)

    driver.find_element_by_xpath('/html/body/div[8]/div[3]/div/div[1]/header/div/div/div[2]/div/div/div[2]/ul/li[3]/form/div/fieldset/ul/li[5]/label/p/span').click()
    time.sleep(2)

    driver.find_element_by_xpath('/html/body/div[8]/div[3]/div/div[1]/header/div/div/div[2]/div/div/div[2]/ul/li[3]/form/div/fieldset/div[2]/button[2]').click()
    time.sleep(2)

    all_names = []

    #NOT SURE WHY I CANNOT GRAB THEIR NAMES.......

    require = ['cyber', 'IA', 'information assurance', 'info assurance', 'info security', 'information security', 'AI', 'artificial intelligence', 'machine learning', 'program manager']
    li_count = 1
    max_names = 96
    page_count = 1
    while True:
        li_window = driver.current_window_handle
        if li_count == 7:
            print('scrolling')
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        if page_count == 1:
            temp = driver.find_element_by_xpath(
                '/html/body/div[8]/div[3]/div/div[2]/div/div[2]/div/div/div[2]/ul/li[' + str(li_count) + ']/div/div/div[2]/a')
        else:
            temp = driver.find_element_by_xpath('/html/body/div[8]/div[3]/div/div[2]/div/div[2]/div/div/div/ul/li[' + str(li_count) + ']/div/div/div[2]/a')
        name = temp.text
        temp.send_keys(Keys.CONTROL + Keys.RETURN)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(.5)
        # NOW WE ARE VIEWING INDV PROFILES
        try:
            driver.find_element_by_xpath(
                '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[3]/section/p/span[3]/span/a').click()
        except Exception:
            print()
        try:
            about = driver.find_element_by_xpath(
                '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[3]/section/p/span[1]')
            about = str(about.text)
        except Exception:
            about = ""

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
                try:
                    title = driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[1]/h2')
                    title = title.text
                except Exception:
                    title = ""

        try:
            driver.find_element_by_xpath(
                '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[1]/section/ul/li[1]/section/div/div/div/p/span/button').click()
        except Exception:
            print()
        try:
            experience = driver.find_element_by_xpath(
                '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[1]/section/ul/li[1]/section/ul/li[1]/div/div/div/div/div')
            experience = experience.text
        except Exception:
            experience = ""
        time.sleep(1)
        for r in require:
            if r in about or r in experience or r in title:
                name = str(name)
                name = name.split('\n')[0]
                print(name)
                all_names.append(name)
                break
        driver.close()
        driver.switch_to.window(li_window)

        li_count += 1

        if len(all_names) > 96 or page_count == 30:
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
                    if page_count == 1:
                        driver.find_element_by_xpath(
                            '/html/body/div[8]/div[3]/div/div[2]/div/div[2]/div/div/div[2]/div[2]/div/button[2]').click()
                    else:
                        driver.find_element_by_xpath('/html/body/div[8]/div[3]/div/div[2]/div/div[2]/div/div/div/div[1]/div/button[2]').click()
                    li_count = 1
                    page_count += 1
                    time.sleep(2)
                except Exception:
                    print('no more pages')
                    driver.switch_to.window(main_window)
                    driver.find_element_by_xpath(
                        '/html/body/div[7]/div[3]/div/div[6]/main/div[1]/div[3]/div[3]/div[1]/section/footer/button').click()
                    con_box = driver.find_element_by_xpath(
                        '/html/body/div[4]/div/div/div[1]/div/div[2]/div/div/div[1]/div/input')
                    for name in all_names:
                        print(name)
                        con_box.send_keys(name)
                        driver.find_element_by_xpath(
                            '/html/body/div[4]/div/div/div[1]/div/div[2]/div/div/div[2]').click()
                    time.sleep(15)
                    driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/div/button').click()

bot()
