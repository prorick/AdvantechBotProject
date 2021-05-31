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
        idsVal = 'booz allen'
    # IDS = [idsVal]
    
    # criteria for downlaoding a resouce attachement
        criteria = ['Industry Day Attendees list', 'Vendors List', 'Event', 'Contractors List',
                    'Interested Parties List', 'Registration List', 'Participants Lists', 'Attendees Lists', 'Attendee',
                    'Interested Companies', 'Bidders List', 'Industry', 'Roster', 'Awardees List', 'Engineering']

    # loop through all given op id numbers
    # for c in criteria:
    #    directory = op
        parent_dir = 'C:\Bots\downloads' # specify your download directory
        
        # set download path
        path = os.path.join(parent_dir)
        os.rmdir(idsVal)
        os.mkdir(idsVal)

        # DRIVER WITH SET DOWNLOAD LOCATION
        options = Options()
        options.add_argument('--incognito')
        options.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
        prefs = {'download.default_directory': str(path)}
        options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        driver.maximize_window()

        # initialize into govwin
        #try:
        driver.get('https://vendornxg.seaport.navy.mil/1/Authentication/Login?ReturnUrl=%2f')
        time.sleep(1)

        driver.find_element_by_xpath('/html/body/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/form/div[1]/label/input').click()

        # login
        email = driver.find_element_by_xpath('/html/body/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/form/div[2]/input') #finds and sends key to email field
        email.send_keys('EMAIL') # update with user credentials

        pswd = driver.find_element_by_xpath('/html/body/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/form/div[3]/input')
        pswd.send_keys('PASSWORD') # update for user credentials 

        driver.find_element_by_xpath('').click()
        time.sleep(1)
        
        opp_count = 2
        
        while True:
            try: # naviagte to your opportunites, and start iterating through them, then execute the same checks as the nonsaved ops bot
                opp = driver.find_element_by_xpath('').click()
            
                time.sleep(3)
                try:
                    driver.find_element_by_link_text("Resources").click()
                    time.sleep(3)
                except Exception:
                    driver.execute_script("window.history.go(-1)")
                    break

                table_count = 1
                page_count = 2
                while True:
                    try:
                        row = driver.find_element_by_xpath('')
                        row_text = str(row.text) 
                        row_text = row_text.split(' ')
                        print(row_text)
                        table_count += 1
                        for row_piece in row_text:
                            if (row_piece in c for c in criteria):
                                row.click()
                                print('found something')
                                time.sleep(5)
                                break
                    except Exception:
                        print('out of opp resources links')
                        break
                driver.execute_script("window.history.go(-2)")
                opp_count += 1
                time.sleep(12)
            except Exception:

                opp_count += 1
                break
        
        
bot()