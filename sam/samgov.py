"""
README
- make sure API key is private and not pushed to GitHub
"""
import requests
from pprint import pprint
from datetime import datetime
from dateutil.relativedelta import relativedelta
import webbrowser
import json
import csv

# required variables
API_KEY = "3sX5w6MJhUWz2ks5lbCKqjk7X4c1xspeGr6xASfz" # don't push this!
LIMIT = 100 # number of search results, we have a limit of 1000 requests per day
# posted dates - Date ranges must be 1 year apart (1 year maximum)
FROM_DATE = (datetime.now() - relativedelta(months=3)).strftime("%m/%d/%Y")
TO_DATE = (datetime.now() + relativedelta(months=7)).strftime("%m/%d/%Y")

# optional variables
NAICS = ['541330', '541519', '541611'] # array containing all naics codes
RDL_FROM = (datetime.now() + relativedelta(months=3)).strftime("%m/%d/%Y") # response deadline from (+3 months)
RDL_TO = (datetime.now() + relativedelta(months=23)).strftime("%m/%d/%Y") # response deadline to (+24 months)

# creating request url
req_url = ('https://api.sam.gov/prod/opportunities/v1/search?'
    + 'limit=' + str(LIMIT)
    + '&api_key=' + API_KEY 
    + '&postedFrom=' + FROM_DATE 
    + '&postedTo=' + TO_DATE)

# using dictionary for optional variables
optional = {
    "ptype": 'o',
    "rdlfrom": FROM_DATE,
    "rdlto": TO_DATE
}
keys_list = list(optional)
for i in range(len(optional)):
    req_url += "&" + keys_list[i] + "=" + str(optional[keys_list[i]])

reqs = []
# create a request string for each naics code
for i in range(len(NAICS)):
    reqs.append(req_url + "&ncode" + NAICS[i]) 

# declare csv file to write to
data_file = open("output.csv", "w+", newline='')
data_file.truncate()

# run each request
for i in range(len(reqs)):
    req_url = reqs[i]

    # opens the file in web browser
    # webbrowser.open(req_url)
    response = requests.get(req_url)

    # storing response
    oppy_data = response.json()['opportunitiesData']

    # writing to csv file
    csv_writer = csv.writer(data_file)

    count = 0
    for data in oppy_data:
        if count == 0:
            header = data.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(data.values())


data_file.close()