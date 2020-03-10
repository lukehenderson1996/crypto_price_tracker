import requests

url = "https://api.bitso.com/v3/ticker?book=btc_mxn"

response = requests.request("GET", url)

print(response.text)



#use last, is in mxn mexican pesos
