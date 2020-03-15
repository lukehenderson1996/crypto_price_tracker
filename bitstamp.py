import requests
import time
from time import sleep

url = "https://www.bitstamp.net/api/ticker/"

while True:
    sleep(0) #1 or less is right number
    response = requests.request("GET", url)
    print(response.text)



#use lastPrice
