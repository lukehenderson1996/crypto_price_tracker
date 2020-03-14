#updated for python 3 usage
import requests, json
from time import sleep, localtime, strftime
import sys

import logging

# create logger, set header for excel
f=open('csv/BTC.csv', "a+")
f.write("Time,Kraken,Bitstamp,Bitfinex,Bitflyer,Itbit\r\n")



def getBitstamp():
    URL = 'https://www.bitstamp.net/api/ticker/'
    try:
        r = requests.get(URL)
        priceFloat = float(json.loads(r.text)['last'])
        return priceFloat
    except requests.ConnectionError:
        print("Error querying Bitstamp API")

def getBitfinex(): #GENERATING KEY ERRORS
    URL = "https://api.bitfinex.com/v1/pubticker/btcusd"
    try:
        r = requests.get(URL)
        priceFloat = float(json.loads(r.text)['last_price'])
        return priceFloat
    except requests.ConnectionError:
        print("Error querying Bitfinex API")

def getKraken():
    URL = "https://api.kraken.com/0/public/Ticker?pair=XBTUSD"
    try:
        r = requests.get(URL)
        priceFloat = float(json.loads(r.text)['result']['XXBTZUSD']['c'][0])
        return priceFloat
    except requests.ConnectionError:
        print("Error querying Kraken API")

def getBitflyer():
    URL = "https://api.bitflyer.com/v1/ticker?product_code=BTC_USD"
    try:
        r = requests.get(URL)
        priceFloat = float(json.loads(r.text)['ltp'])
        return priceFloat
    except requests.ConnectionError:
        print("Error querying Bitflyer API")

def getItbit():
    URL = "https://api.itbit.com/v1/markets/XBTUSD/ticker"
    try:
        r = requests.get(URL)
        priceFloat = float(json.loads(r.text)['lastPrice'])
        return priceFloat
    except requests.ConnectionError:
        print("Error querying Itbit API")


while True:
    sleep(2)
    try:
        lastBitstamp = str(getBitstamp())
        lastBitfinex = "rate errors :(" #str(getBitfinex()) #"rate errors :(" #
        lastKraken = str(getKraken())
        lastBitflyer = str(getBitflyer())
        lastItbit = str(getItbit())
        print("\r\n" + strftime("%Y-%m-%d %H:%M:%S", localtime()))
        #update print to be a function eventually with more currencies
        print("Bitstamp: $" + lastBitstamp.ljust(7, '0')[:7] + "    Itbit: $" + lastItbit.ljust(7, '0')[:7] + "    Kraken: $" + lastKraken.ljust(7, '0')[:7] + "    Bitflyer: $" + lastBitflyer.ljust(7, '0')[:7])
        f.write(strftime("%Y-%m-%d %H:%M:%S", localtime()) + " , " + lastKraken + " , " + lastBitstamp + " , " + lastBitfinex + " , " + lastBitflyer + " , " + lastItbit + "\r\n")
        f.close()
        f=open('csv/BTC.csv', "a+")
    except:
        print("------------------ERROR------------------")
        print(sys.exc_info())
        f.write(strftime("%Y-%m-%d %H:%M:%S", localtime()) + " , " + "ERROR" + " , " + "ERROR" + " , " + "ERROR" + " , " + str(sys.exc_info()) + "\r\n")
        f.close()
        f=open('csv/BTC.csv', "a+")
