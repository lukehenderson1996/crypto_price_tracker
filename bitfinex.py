import requests

url = "https://api.bitfinex.com/v1/pubticker/btcusd"

response = requests.request("GET", url)

print(response.text)
