# necessary imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Function definition for entire bot process
def bot():
    # set paths for webdriver + initialize
    options = Options()
    options.add_argument('--incognito')
    options.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.maximize_window()

    driver.get('https://iq.govwin.com/cas/login?service=https://iq.govwin.com/neo/myGovwin')
    time.sleep(1)

    #login
    email = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/form/div/div/input')
    email.send_keys('') # replace with user credentials

    driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/form/div/span/input[1]').click()
    time.sleep(1)

    pswd = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/form/div/div[2]/input')
    pswd.send_keys('') # replace with user credentials

    driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/form/div/span/input[1]').click()
    time.sleep(2)

    try:
        driver.find_element_by_xpath('/html/body/div[12]/div/button').click()
    except Exception:
        print('No welcome message')

    driver.find_element_by_xpath('/html/body/div[4]/div[2]/div[4]/ul/li[6]/a').click()

    # driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[3]/div/div/div[3]/form/div/div/div[2]/div[1]/div/div/label/select').click()
    # time.sleep(1)
    # driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[3]/div/div/div[3]/form/div/div/div[2]/div[1]/div/div/label/select/option[5]').click()
    # time.sleep(1)

    opp_count = 1
    # interested criteria list
    criteria = ['Industry Day', 'Industry Day attendees list', 'Vendors List', 'Event Attachments', 'Contractors List',
                'Interested Parties List', 'Registration List', 'Participants Lists', 'Attendees Lists', 'Attendee',
                'Interested Companies', 'Bidders List', 'Industry Day Procurement List']

    main_window = driver.current_window_handle

    while True:
        try: # naviagte to your opportunites, and start iterating through them, then execute the same checks as the nonsaved ops bot
            opp = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[3]/div/div/div[4]/form/div/div/div[3]/div/div[2]/table/tbody/tr[' + str(opp_count) +']/td[6]/a')
            opp.send_keys(Keys.CONTROL + Keys.RETURN)
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(3)

            driver.find_element_by_link_text("Resources").click()
            time.sleep(3)

            table_count = 1
            while True:
                try:
                    row = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[8]/div/div/div[3]/div/div/div[2]/div[1]/div[3]/table/tbody/tr[' + str(table_count) + ']/td[2]/a')
                    row_text = str(row.text)
                    row_text = row_text.split(' ')
                    print(row_text)
                    table_count += 1
                    for row_piece in row_text:
                        if any(row_piece in c for c in criteria):
                            row.click()
                            print('found something')
                            time.sleep(5)
                            break
                except Exception:
                    print('out of opp resources links')
                    break
            driver.close()
            driver.switch_to.window(main_window)
            opp_count += 1
        except Exception:
            print('out of opps')
            break
bot()
