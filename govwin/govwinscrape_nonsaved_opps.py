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
    #IDS = range(198687, 201682, 1)
    IDS = ['192252']
    print(len(IDS))
    
    # criteria for downlaoding a resouce attachement
    criteria = ['Industry Day Attendees list', 'Vendors List', 'Event', 'Contractors List',
                'Interested Parties List', 'Registration List', 'Participants Lists', 'Attendees Lists', 'Attendee',
                'Interested Companies', 'Bidders List', 'Industry Day Procurement List', 'Roster', 'Awardees List']

    # loop through all given op id numbers
    for op in IDS:
        directory = str(op)
        #parent_dir = 'C:\Bots\downloads' # specify your download directory
        parent_dir = '/Users/prothit/Desktop/advantech' # specify your download directory (MAC)
        
        # set download path
        path = os.path.join(parent_dir, directory)
        # os.mkdir(path)
        # path = path.replace('/', '\\')
        # print(path)

        # DRIVER WITH SET DOWNLOAD LOCATION
        options = Options()
        options.add_argument('--incognito')
        #options.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe' #for windows
        options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' #for macs

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

            try:
                driver.find_element_by_xpath('/html/body/div[12]/div/button').click()
            except Exception:
                print('No welcome message')
            
            # search op id in quicksearch field, then click on the corresponding op
            search = driver.find_element_by_xpath('/html/body/div[1]/header/div[2]/div[2]/div[1]/form/div/input') 
            search.send_keys(op)
            time.sleep(2)
            driver.find_element_by_xpath('/html/body/div[1]/header/div[2]/div[2]/div[1]/form/a[1]').click()
            time.sleep(2)
            try:
                driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[1]/div/div[5]/div[5]/div/div/h3/a').click()
                time.sleep(2)
            except:
                time.sleep(10)
                driver.close()
                break

            driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[1]/ul/li[6]/a').click()
            time.sleep(10)
            driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[8]/div/div/div[1]/ul/li[3]/a').click()
            time.sleep(5)

            table_count = 1
        except Exception:
            driver.close()
            continue

        while True: # if the script could find the resources tab and it has documents in it, it will check to see if their titles match any fo the criteria (very general)
            try:
                print('made it to the resource tab begin')
                #row = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[8]/div/div/div[3]/div/div/div[2]/div[1]/div[3]/table/tbody/tr['+ str(table_count) +']/td[1]/a')
                row = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[8]/div/div/div[5]/div/div/div[2]/div[1]/div[3]/table/tbody/tr['+ str(table_count) +']/td[3]/a')

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
                print('made it to the resource tab end')
            except Exception:
                print('out of opp resources links')
                break
        driver.close()
        time.sleep(5)
        
bot()