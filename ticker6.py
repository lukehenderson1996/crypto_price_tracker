#updated for python 3 usage
import requests, json
import time
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
    except KeyboardInterrupt:
        exit()
    except: # requests.ConnectionError:
        return "get error"

def getBitfinex(): #GENERATING KEY ERRORS bc rate
    URL = "https://api.bitfinex.com/v1/pubticker/btcusd"
    try:
        r = requests.get(URL)
        priceFloat = float(json.loads(r.text)['last_price'])
        return priceFloat
    except KeyboardInterrupt:
        exit()
    except: # requests.ConnectionError:
        return "get error"

def getKraken():
    URL = "https://api.kraken.com/0/public/Ticker?pair=XBTUSD"
    try:
        r = requests.get(URL)
        priceFloat = float(json.loads(r.text)['result']['XXBTZUSD']['c'][0])
        return priceFloat
    except KeyboardInterrupt:
        exit()
    except: # requests.ConnectionError:
        return "get error"

def getBitflyer():
    URL = "https://api.bitflyer.com/v1/ticker?product_code=BTC_USD"
    try:
        r = requests.get(URL)
        priceFloat = float(json.loads(r.text)['ltp'])
        return priceFloat
    except KeyboardInterrupt:
        exit()
    except: # requests.ConnectionError:
        return "get error"

def getItbit():
    URL = "https://api.itbit.com/v1/markets/XBTUSD/ticker"
    try:
        r = requests.get(URL)
        priceFloat = float(json.loads(r.text)['lastPrice'])
        return priceFloat
    except KeyboardInterrupt:
        exit()
    except: #requests.ConnectionError:
        return "get error"

progStart = time.time()
lastFinexFetch = time.time()

while True:
    iterTime = time.time()
    try:
        lastBitstamp = str(getBitstamp())
        if time.time()-lastFinexFetch > 6: #4 seconds caused errors on 03-17 4PM
            try:
                lastBitfinex = str(getBitfinex()) #"rate errors :("
                lastFinexFetch = time.time()
            except KeyboardInterrupt:
                exit()
            except:
                lastBitfinex = "str() error"
        else:
            lastBitfinex = "       "
        lastKraken = str(getKraken())
        lastBitflyer = str(getBitflyer())
        lastItbit = str(getItbit())
        print("\r\n" + strftime("%Y-%m-%d %H:%M:%S", localtime()))
        #update print to be a function eventually with more currencies
        print("Bitstamp: $" + lastBitstamp.ljust(7, '0')[:7] + "    Itbit: $" + lastItbit.ljust(7, '0')[:7] + "    Kraken: $" + lastKraken.ljust(7, '0')[:7] + "    Bitfinex: $" + lastBitfinex.ljust(7, '0')[:7])
        f.write(strftime("%Y-%m-%d %H:%M:%S", localtime()) + " , " + lastKraken + " , " + lastBitstamp + " , " + lastBitfinex + " , " + lastBitflyer + " , " + lastItbit + "\r\n")
        f.close()
        f=open('csv/BTC.csv', "a+")
    except KeyboardInterrupt:
        exit()
    except SystemExit:
        exit()
    except:
        print("------------------ERROR------------------")
        print(sys.exc_info())
        f.write(strftime("%Y-%m-%d %H:%M:%S", localtime()) + " , " + "ERROR" + " , " + "ERROR" + " , " + "ERROR" + " , " + str(sys.exc_info()) + "\r\n")
        f.close()
        f=open('csv/BTC.csv', "a+")
