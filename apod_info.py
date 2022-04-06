import requests
from sys import argv
import json

def main():
     
    apod_info_dict = get_apod_info()

    print(apod_info_dict)

    print(apod_info_dict['url'])


def get_apod_info():
    
    URL = 'https://api.nasa.gov/planetary/apod'

    API_KEY = '4JxrLgSaoFPKS9Xd8lXugyeMjYAN7aOOyfH0EQ5I'
    params={
             'api_key':API_KEY,
                'date':'2020-07-18'
            }
    response = requests.get(URL,params=params)
    
    return response.json()

main()