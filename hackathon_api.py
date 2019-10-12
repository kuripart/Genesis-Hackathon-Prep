#Authors: Nithin Prasad and Partha Sarathy Kuri
#Date Created: 12 October, 2019
#Program Name: hackathon_api.py
#Program Description: This program contains API calls and algorthms to handle and
# test the calls, to be implemented in the final hackthon project.

#import requests

# importing the requests library 
import requests 

##GET REQUEST SAMPLE
# api-endpoint 
URL = "http://httpbin.org/get"
  
# location given here 
location = "delhi technological university"
  
# defining a params dict for the parameters to be sent to the API 
PARAMS = {'address':location} 
  
# sending get request and saving the response as response object 
r = requests.get(url = URL, params = PARAMS) 
  
# extracting data in json format 
data = r.json() 

print(data)

print("*******************************************************")

##POST REQUEST SAMPLE
# defining the api-endpoint  
API_ENDPOINT = "http://httpbin.org/post"
  
# your API key here 
API_KEY = "XXXXXXXXXXXXXXXXX"
  
# your source code here 
source_code = ''' 
print("Hello, world!") 
a = 1 
b = 2 
print(a + b) 
'''
  
# data to be sent to api 
data = {'api_dev_key':API_KEY, 
        'api_option':'paste', 
        'api_paste_code':source_code, 
        'api_paste_format':'python'} 
  
# sending post request and saving response as response object 
r = requests.post(url = API_ENDPOINT, data = data) 
  
# extracting response text  
pastebin_url = r.text 
print("The pastebin URL is:%s"%pastebin_url) 
