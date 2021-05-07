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
 
    driver.get('https://www.bgov.com/next/opportunity_search#/') #get bloomberg url
    time.sleep(1)
 
    #login
    #email = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[2]/div/div[2]/form/div[1]/div[2]/input')
    email = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[2]/div/div[2]/form/div[1]/div[2]/input')
 
    email.send_keys('ptoro@advantechglobal.org') # replace with user credentials
 
    #not needed as username and password are on same page
    #driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[2]/div/div[2]/form/div[2]/div[2]/input').click()
    time.sleep(1)
 
    #pswd = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[2]/div/div[2]/form/div[2]/div[2]/input')
    pswd = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[2]/div/div[2]/form/div[2]/div[2]/input')
 
    pswd.send_keys('PASSWORD') # replace with user credentials
 
    driver.find_element_by_xpath('').click() #change this?
    time.sleep(2)
 
    #this must be done with access to bloomberg
    #try: # need to check this
    #    driver.find_element_by_xpath("/html/body/div[@id='app']/div/div[@class='content-wrapper']/div[@class='grid-wrapper']/div[@class='over-grid-content']/div[@class='content-area']/div[@class='content-area']/form/button[@class='button--primary sign-in-button ft-button-2Pla ft-buttonBlock-311V']").click()
    #except Exception:
    #    print('No welcome message')

    pswd = driver.find_element_by_xpath("").click()

    driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[2]/div/div[2]/form/div[2]/div[2]/input').click()
    time.sleep(3)
    driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[4]/div/div[2]/div/div[5]/div[2]/svg/path').click()
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[4]/div/div[2]/div/div[7]/div[4]/svg/path').click()
    time.sleep(1)
    keywords = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[1]/div/div/div/div[2]/div/textarea')
    keywords.send_keys('navy parsons')
    time.sleep(2)
    driver.find_elements_by_xpath('/html/body/div[2]/div/div[2]/div/div[1]/div/div/button').click()
    time.sleep(4)
    driver.find_elements_by_xpath('/html/body/div[2]/div/div[2]/div/div[4]/span/div[1]/div/div/div[1]/div[3]/a').click()

    opp_count = 1
    # interested criteria list
    criteria = ['Industry Day', 'Industry Day attendees list', 'Vendors List', 'Event Attachments', 'Contractors List',
                'Interested Parties List', 'Registration List', 'Participants Lists', 'Attendees Lists', 'Attendee',
                'Interested Companies', 'Bidders List', 'Industry Day Procurement List'] #will likely change for Bloomberg

    main_window = driver.current_window_handle
    
    while True:
        try: # navigate to your opportunites, and start iterating through them, then execute the same checks as the nonsaved ops bot

            industryDay = driver.find_element_by_name('')

            opp = driver.find_element_by_xpath('' + str(opp_count) + '')
            opp.send_keys(Keys.CONTROL + Keys.RETURN)
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(3)

            driver.find_element_by_xpath('').click()
            time.sleep(3)

            table_count = 1
            while True:
                try:
                    row = driver.find_element_by_xpath('' + str(table_count) + '')
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

