import requests


response = requests.post('https://httpbin.org/post', data={'key': 'value'})
print(response.text)
response = requests.put('https://httpbin.org/put', data={'key': 'alpha'})
print(response.text)