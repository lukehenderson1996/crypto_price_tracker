import requests

url = "https://api.itbit.com/v1/markets/XBTUSD/ticker"

response = requests.request("GET", url)

print(response.text)



#use lastPrice
