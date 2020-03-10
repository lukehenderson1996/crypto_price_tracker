#updated for python 3 usage
import requests, json
from time import sleep, localtime, strftime

import logging

# create logger, set header for excel
f=open('csv/BTC.csv', "a+")
f.write("Time,Kraken,Bitstamp,Bitfinex,Bitflyer\r\n")



def getBitstamp():
    URL = 'https://www.bitstamp.net/api/ticker/'
    try:
        r = requests.get(URL)
        priceFloat = float(json.loads(r.text)['last'])
        return priceFloat
    except requests.ConnectionError:
        print "Error querying Bitstamp API"

def getBitfinex():
    URL = "https://api.bitfinex.com/v1/pubticker/btcusd"
    try:
        r = requests.get(URL)
        priceFloat = float(json.loads(r.text)['last_price'])
        return priceFloat
    except requests.ConnectionError:
        print "Error querying Bitfinex API"

def getKraken():
    URL = "https://api.kraken.com/0/public/Ticker?pair=XBTUSD"
    try:
        r = requests.get(URL)
        priceFloat = float(json.loads(r.text)['result']['XXBTZUSD']['c'][0])
        return priceFloat
    except requests.ConnectionError:
        print "Error querying Bitfinex API"

def getBitflyer():
    URL = "https://api.bitflyer.com/v1/ticker?product_code=BTC_USD"
    try:
        r = requests.get(URL)
        priceFloat = float(json.loads(r.text)['ltp'])
        return priceFloat
    except requests.ConnectionError:
        print "Error querying Bitfinex API"


while True:
    sleep(4)
    try:
        lastBitstamp = str(getBitstamp())
        lastBitfinex = str(getBitfinex())
        lastKraken = str(getKraken())
        lastBitflyer = str(getBitflyer())
        print "\r\n" + strftime("%Y-%m-%d %H:%M:%S", localtime())
        print "Bitstamp: $" + lastBitstamp.ljust(7, '0')[:7] + "    Bitfinex: $" + lastBitfinex.ljust(7, '0')[:7] + "    Kraken: $" + lastKraken.ljust(7, '0')[:7] + "    Bitflyer: $" + lastBitflyer.ljust(7, '0')[:7]
        f.write(strftime("%Y-%m-%d %H:%M:%S", localtime()) + " , " + lastKraken + " , " + lastBitstamp + " , " + lastBitfinex + " , " + lastBitflyer + "\r\n")
        f.close()
        f=open('csv/BTC.csv', "a+")
    except:
        print "------------------ERROR------------------"
        f.write(strftime("%Y-%m-%d %H:%M:%S", localtime()) + " , " + "ERROR" + " , " + "ERROR" + " , " + "ERROR" + " , " + "ERROR" + "\r\n")
        f.close()
        f=open('csv/BTC.csv', "a+")
