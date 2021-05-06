# necessary imports
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import os
import schedule

# Function definition for entire bot process
def bot():
    
    # These need to be set to potentially a list of ids or search criteria we are looking for BEFORE ran
    idsVal = input('enter company name: ') 
    IDS = [idsVal]
    
    # criteria for downlaoding a resouce attachement
    criteria = ['Industry Day Attendees list', 'Vendors List', 'Event', 'Contractors List',
                'Interested Parties List', 'Registration List', 'Participants Lists', 'Attendees Lists', 'Attendee',
                'Interested Companies', 'Bidders List', 'Industry Day Procurement List', 'Roster', 'Awardees List']

    # loop through all given op id numbers
    for op in IDS:
        directory = op
        parent_dir = 'C:\Bots\downloads' # specify your download directory
        
        # set download path
        path = os.path.join(parent_dir, directory)
        # os.mkdir(path)
        # path = path.replace('/', '\\')
        # print(path)

        # DRIVER WITH SET DOWNLOAD LOCATION
        options = Options()
        options.add_argument('--incognito')
        options.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
        prefs = {'download.default_directory': str(path)}
        options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        driver.maximize_window()

        # initialize into govwin
        try:
            driver.get('https://iq.govwin.com/cas/login?service=https://iq.govwin.com/neo/myGovwin')
            time.sleep(1)

            # login
            email = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/form/div/div/input')
            email.send_keys('eramond@advantechglobal.org') # update with user credentials

            driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/form/div/span/input[1]').click()
            time.sleep(1)

            pswd = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/form/div/div[2]/input')
            pswd.send_keys('Advantech1973!') # update for user credentials 

            driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/form/div/span/input[1]').click()
            time.sleep(2)

            # search op id in quicksearch field, then click on the corresponding op
            # search = driver.find_element_by_xpath('/html/body/div[1]/header/div[2]/div[2]/div[1]/form/div/input') #updated
            # search.send_keys(op)
            # time.sleep(2)
            driver.find_element_by_xpath('/html/body/div[1]/header/div[2]/div[2]/div[1]/form/a[2]').click() #/html/body/div[1]/header/div[2]/div[2]/div[1]/form/a[1] is the old path
            time.sleep(2)

            #on search results page
            # try: #we are try
            #     driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[1]/div/div[5]/div[2]/div/div[3]/div/div[2]/table/tbody/tr[1]/td[4]/a').click() #/html/body/div[4]/div[3]/div[1]/div/div[4]/div[5]/div/div/h3/a (old path, might be wrong)
            #     time.sleep(2)
            # except:
            #     time.sleep(10)
            #     driver.close()
            #     break

            # we are clicking --- here
            driver.find_element_by_xpath('/html/body/div[4]/div[3]/form/div[4]/div[3]/div/div[1]/div[1]/div/div[2]/select/option[76]').click() #checks Navy as a venor
            time.sleep(2)
            driver.find_element_by_xpath('/html/body/div[4]/div[3]/form/div[9]/a').click() #opens options for existing contracts
            time.sleep(2)
            incumbent = driver.find_element_by_xpath('/html/body/div[4]/div[3]/form/div[10]/div[3]/div/div[2]/div[2]/span/span[1]/span/ul/li/input')  #enters input field of incumbent
            time.sleep(2)
            incumbent.send_keys(idsVal) # update with company preference
            time.sleep(2)
            driver.find_element_by_name("Value").send_keys(Keys.RETURN)
            time.sleep(2)
            driver.find_element_by_xpath('/html/body/div[4]/div[3]/form/input[5]').click()

            table_count = 1
        except Exception:
            driver.close()
            continue

        while True: # if the script could find the resources tab and it has documents in it, it will check to see if their titles match any fo the criteria (very general)
            try:

                #this all checks if the opportunites meet the criteria that we w
                months_out = 18
                opp_seller = 'Navy'
                current_month = 5
                current_year = 2021

                month_finder = driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[1]/div/div[5]/div[2]/div/div[3]/div/div[2]/table/tbody/tr[' + str(table_count) + ']/td[9]')
                year_finder = month_finder[3:6]
                month_finder = month_finder[0:1]
                opp_seller_finder = driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[1]/div/div[5]/div[2]/div/div[3]/div/div[2]/table/tbody/tr[' + str(table_count) + ']/td[5]/span')
                opp_seller_finder = opp_seller_finder[0:3]

                month_finder = (12 * (year_finder - current_year)) + (month_finder - current_month)

                if ((months_out >= month_finder)and (opp_seller == opp_seller_finder)) :
                    row = driver.find_element_by_xpath( 
                        '/html/body/div[4]/div[4]/div/div[8]/div/div/div[3]/div/div/div[2]/div[1]/div[3]/table/tbody/tr[' + str(table_count) +']/td[1]/a') #/html/body/div[4]/div[4]/div/div[8]/div/div/div[3]/div/div/div[2]/div[1]/div[3]/table/tbody/tr[' + str(
                        #table_count) + ']/td[2]/a
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
        time.sleep(5)
        
bot()
