import requests

url = "https://api.bitflyer.com/v1/ticker?product_code=BTC_USD"

response = requests.request("GET", url)

print(response.text)




