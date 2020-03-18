import requests
import time
from time import sleep

url = "https://api.bitfinex.com/v1/pubticker/btcusd"

while True:
    sleep(4) # 4 is the right delay, actually we're trying 6 now
    response = requests.request("GET", url)
    print(response.text)
