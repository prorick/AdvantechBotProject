"""
"""
import requests
from pprint import pprint
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
import csv

# required variables
API_KEY = "3sX5w6MJhUWz2ks5lbCKqjk7X4c1xspeGr6xASfz"
LIMIT = 5 # number of search results, we have a limit of 1000 requests per day
# posted dates - Date ranges must be 1 year apart (1 year maximum)
FROM_DATE = (datetime.now() - relativedelta(months=3)).strftime("%m/%d/%Y")
TO_DATE = (datetime.now() + relativedelta(months=7)).strftime("%m/%d/%Y")

# response deadlines 
AWARD_NAME = "Lockheed Martin"

# SET_ASIDE_TYPE

# https://api.sam.gov/prod/opportunities/v1/search?limit=1&api_key={User’s Public API Key}&postedFrom=01/01/2018&postedTo=05/10/2018&ptype=a&deptname=general

# creating request url
response_link = ('https://api.sam.gov/prod/opportunities/v1/search?'
    + 'limit=' + str(LIMIT)
    + '&api_key=' + API_KEY 
    + '&postedFrom=' + FROM_DATE 
    + '&postedTo=' + TO_DATE)

# using dictionary for optional variables
optional = {
    "ptype": 'a',
    "deptname": "general",
    "ncode": '541330',
    "rdlto": TO_DATE,
}

keys_list = list(optional)
for i in range(len(optional)):
    response_link += "&" + keys_list[i] + "=" + str(optional[keys_list[i]])

"""
workflow
- get a bunch of requests
- format the responses by "award date"
response parameters to check
setAside
setAsideDescription
responseDeadLine
active
data.award.amount
data.award.date
"""

print(response_link)

# get request
response = requests.get(response_link)
# if (response == 200): # 200 - approved status code
#     print("good to go")
# else:
#     print('oops')

# checking response parameters
# can change this to only get opportunities for this company
response_params = {
    "data.award.awardee.name": "Lockheed Martin"
}

response_params_keys = list(response_params)
for i in range(LIMIT):

    # storing/cleaning response
    oppy_data = response.json()['opportunitiesData']

    data_file = open('output.csv', 'w', newline='')
    csv_writer = csv.writer(data_file)

    # writing out opportunities to csv file
count = 0
for data in oppy_data:

    #if statement needed here to check for appropriate incumbents

    if count == 0:
        header = data.keys()
        csv_writer.writerow(header)
        count += 1
    csv_writer.writerow(data.values())

data_file.close()