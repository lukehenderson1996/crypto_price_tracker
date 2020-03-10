import requests

url = "https://api.exchangeratesapi.io/latest?symbols=USD,GBP HTTP/1.1"

response = requests.request("GET", url)

print(response.text)

https://exchangeratesapi.io/

https://medium.com/@MicroPyramid/free-foreign-currency-exchange-rates-api-2a93195649fb

#use last
