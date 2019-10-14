import requests
import autocomplete

# response = requests.post('https://httpbin.org/post', data={'key': 'value'})
# print(response.text)
# response = requests.put('https://httpbin.org/put', data={'key': 'alpha'})
# print(response.text)

autocomplete.load()
x = autocomplete.split_predict('this is the end')
print(x)