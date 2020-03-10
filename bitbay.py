#DOESNT WORK



import requests

url = "https://bitbay.net/API/Public/BTCUSD/trades.json"

response = requests.request("GET", url)

print(response.text)



#use last
