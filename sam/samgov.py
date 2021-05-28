import requests
from pprint import pprint
from datetime import datetime
from dateutil.relativedelta import relativedelta

# variables
API_KEY = ""
LIMIT = 100 # number of search results, we have a limit of 1000 requests per day
FROM_DATE = datetime.now().strftime("%m/%d/%Y")
TO_DATE = (datetime.now() + relativedelta(months=12)).strftime("%m/%d/%Y")

# get request
response = requests.get('https://api.sam.gov/prod/opportunities/v1/search?' 
    + 'limit=' + str(LIMIT)
    + '&api_key=' + API_KEY 
    + '&postedFrom=' + FROM_DATE 
    + '&postedTo=' + TO_DATE)
if (response == 200):
    print(response.json())

pprint(response.json())

# storing/cleaning response
    

print(FROM_DATE)
print(TO_DATE)
