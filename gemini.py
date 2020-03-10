import requests

url = "https://api.gemini.com/v1/pubticker/btcusd"

response = requests.request("GET", url)

print(response.text)



#use last
