import requests
import time
from time import sleep

url = "https://api.itbit.com/v1/markets/XBTUSD/ticker"

while True:
    sleep(0) #1 or less is right number
    response = requests.request("GET", url)
    print(response.text)



#use lastPrice
