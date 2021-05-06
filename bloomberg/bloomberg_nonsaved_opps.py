import schedule

# Function definition for entire bot process
def bot():
    
    # These need to be set to potentially a list of ids or search criteria we are looking for BEFORE ran
    IDS = []
    print(len(IDS))
    
    # criteria for downloading a resouce attachement
    criteria = ['Industry Day Attendees list', 'Vendors List', 'Event', 'Contractors List',
                'Interested Parties List', 'Registration List', 'Participants Lists', 'Attendees Lists', 'Attendee',
                'Interested Companies', 'Bidders List', 'Industry Day Procurement List', 'Roster', 'Awardees List']

    # loop through all given op id numbers
    for op in IDS:
        directory = op
        parent_dir = 'C:\Bots\downloads' # specify your download directory
        
        # set download path
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)
        path = path.replace('/', '\\')
        print(path)

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
            driver.get('https://www.bgov.com/auth/sign_in')
            time.sleep(1)

            #login
            email = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[2]/div/div[2]/form/div[1]/div[2]/input')
            email.send_keys('EMAIL') # replace with user credentials

            driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[2]/div/div[2]/form/div[2]/div[2]/input').click()
            time.sleep(1)

            pswd = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[2]/div/div[2]/form/div[2]/div[2]/input')
            pswd.send_keys('PASSWORD') # replace with user credentials

            driver.find_element_by_xpath('').click() #change this?
            time.sleep(2)


            try:
                driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[2]/div/div[2]/form/button').click()#needs to be filled
            except Exception:
                print('No welcome message')
            
            #this must be done with access to bloomberg
            # search op id in quicksearch field, then click on the corresponding op
            search = driver.find_element_by_xpath('')#needs to be filled
            search.send_keys(op)
            time.sleep(2)
            driver.find_element_by_xpath('').click()#needs to be filled
            time.sleep(2)
            try:
                driver.find_element_by_xpath('').click()#needs to be filled
                time.sleep(2)
            except:
                time.sleep(10)
                driver.close()
                break

            driver.find_element_by_xpath('').click()#needs to be filled
            time.sleep(10)

            table_count = 1
        except Exception:
            driver.close()
            continue

        while True: # if the script could find the resources tab and it has documents in it, it will check to see if their titles match any fo the criteria (very general)
            try:
                row = driver.find_element_by_xpath(
                    '#needs to be filled' + str(
                        table_count) + ']/td[2]/a') #needs fixing
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
