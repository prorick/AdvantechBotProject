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
    # idsVal = 'booz allen'
    # IDS = [idsVal]
    
    # criteria for downlaoding a resouce attachement
        criteria = ['Industry Day Attendees list', 'Vendors List', 'Event', 'Contractors List',
                    'Interested Parties List', 'Registration List', 'Participants Lists', 'Attendees Lists', 'Attendee',
                    'Interested Companies', 'Bidders List', 'Industry Day Procurement List', 'Roster', 'Awardees List']

    # loop through all given op id numbers
    # for c in criteria:
    #    directory = op
        parent_dir = 'C:\Bots\downloads' # specify your download directory
        
        # set download path
        path = os.path.join(parent_dir)

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
        time.sleep(1)

        driver.find_element_by_xpath('/html/body/div[1]/header/div[2]/div[2]/div[1]/form/a[2]').click() #/html/body/div[1]/header/div[2]/div[2]/div[1]/form/a[1] is the old path
        time.sleep(1)
  
        driver.find_element_by_xpath('/html/body/div[4]/div[3]/form/div[4]/div[3]/div/div[1]/div[1]/div/div[2]/select/option[76]').click() #checks Navy as a vendor
        time.sleep(1)

        driver.find_element_by_id('panelMileStonesHead').click()
        time.sleep(1)    

        driver.find_element_by_class_name('select2-selection__rendered').click()
        time.sleep(1)

        driver.find_element_by_xpath('/html/body/div[4]/div[3]/form/input[5]').click()
        
        # table_count = 1
        # except Exception:
        #     driver.close()
        #     continue
        table_count = 2
        while True: # if the script could find the resources tab and it has documents in it, it will check to see if their titles match any fo the criteria (very general)
            try:
                
                opportunities = driver.find_elements_by_class_name('rowListView')

                for x in opportunities:

                    driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[1]/div/div[5]/div[5]/div/div[' + str(table_count) +']/h3/a').click()

                    table_count = table_count + 1

                    driver.find_element_by_link_text('Resources').click()

                    row_text = driver.find_elements_by_class_name('sorting_2')
                
                    for r in row_text:
                        if any(r for c in criteria):
                            print('found something')
                            driver.find_elements_by_partial_link_text('industry day').click()
                            #must click on file to download it

                    driver.execute_script("window.history.go(-2)")
                    #must go back to original website here
                            
            
            except Exception:
                print('out of opp resources links')
                break
        driver.close()
        
bot()
