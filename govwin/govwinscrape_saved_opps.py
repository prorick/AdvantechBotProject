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
    email.send_keys('EMAIL') # replace with user credentials

    driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/form/div/span/input[1]').click()
    time.sleep(1)

    pswd = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/form/div/div[2]/input')
    pswd.send_keys('PASSWORD') # replace with user credentials

    driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/form/div/span/input[1]').click()
    time.sleep(2)

    driver.find_element_by_xpath('/html/body/div[4]/div[2]/div[4]/ul/li[6]/a').click() #clicks on my opportunities

    
    opp_count = int(input())
    table_count = int(input())
    months_out = 18
    opp_seller = 'Navy'
    current_month = 5
    current_year = 2021
    
    # interested criteria list
    criteria = ['Industry Day', 'Industry Day attendees list', 'Vendors List', 'Event Attachments', 'Contractors List',
                'Interested Parties List', 'Registration List', 'Participants Lists', 'Attendees Lists', 'Attendee',
                'Interested Companies', 'Bidders List', 'Industry Day Procurement List']

    main_window = driver.current_window_handle

    while True:#might want to consider using another loop besides this
        try:#navigate to your opportunites, and start iterating through them, then execute the same checks as the nonsaved ops bot

            #this all checks if the opportunites meet the criteria that we want:

            month_finder = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[3]/div/div/div[4]/form/div/div/div[3]/div/div[2]/table/tbody/tr[' + str(opp_count) + ']/td[10]')
            year_finder = month_finder[3:6]
            month_finder = month_finder[0:1]
            opp_seller_finder = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[3]/div/div/div[4]/form/div/div/div[3]/div/div[2]/table/tbody/tr[' + str(opp_count) + ']/td[7]')
            opp_seller_finder = opp_seller_finder[0:3]

            month_finder = (12 * (year_finder - current_year)) + (month_finder - current_month)
        
        
        if ((months_out >= month_finder) && (opp_seller == opp_seller_finder)) {

            opp = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[3]/div/div/div[4]/form/div/div/div[3]/div/div[2]/table/tbody/tr[' + str(opp_count) + ']/td[6]/a') #/html/body/div[4]/div[4]/div/div[3]/div/div/div[3]/form/div/div/div[3]/div/div[2]/table/tbody/tr[' + str(opp_count) + ']/td[6]/a (old path, new one might be wrong)
            #updated tab
            opp.send_keys(Keys.CONTROL + Keys.RETURN)
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(3)

            driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[1]/ul/li[6]/a').click() #/html/body/div[4]/div[4]/div/div[1]/ul/li[6]/a (old path)
            time.sleep(3)

            
            while True: # might want to consider using another loop besides this
                try:
                    row = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[8]/div/div/div[3]/div/div/div[2]/div[1]/div[3]/table/tbody/tr[' + str(table_count) + ']/td[1]/a') #/html/body/div[4]/div[4]/div/div[8]/div/div/div[3]/div/div/div[2]/div[1]/div[3]/table/tbody/tr[' + str(table_count) + ']/td[2]/a (old path)
                    #updated
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

        }

        except Exception:
            print('out of opps')
            break
bot()

