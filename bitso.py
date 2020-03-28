import requests, json
import time
from time import sleep

url = "https://api.bitso.com/v3/ticker?book=btc_mxn"

MXN_USD = 1/23.5818

while True:
    sleep(0) #1 or less is right number
    response = requests.request("GET", url)
    print(response.text)

    # #test keying
    # r = requests.get(url)
    # priceFloat = float(json.loads(r.text)['payload']['last'])*MXN_USD
    # print(priceFloat)
    # sleep(20)




#use last, is in mxn mexican pesos
