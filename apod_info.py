import requests
from sys import argv
import json

apod_date= '2020-07-18'
URL = 'https://api.nasa.gov/planetary/apod'

API_KEY = '4JxrLgSaoFPKS9Xd8lXugyeMjYAN7aOOyfH0EQ5I'
params={
        'api_key':API_KEY,
        'date':apod_date
    }
response = requests.get(URL,params=params)
    
a = response.json()

print(a)
