#updated for python 3 usage
import requests, json
import time
from time import sleep, localtime, strftime
import sys
import os
import logging

# create logger, set header for excel
# fetchTime = localtime()
# if not os.path.exists('datedCSV/' + strftime("%Y-%m-%d", fetchTime)):
#     os.mkdir('datedCSV/' + strftime("%Y-%m-%d", fetchTime))
# f=open('datedCSV/' + strftime("%Y-%m-%d", fetchTime) + '/BTC_' + strftime("%H", fetchTime) + '.csv', "a+")
#no header for individual hour files
#f.write("Time,Kraken,Bitstamp,Bitfinex,Bitflyer,Itbit\r\n")
# f.close()

MXN_USD = 1/23.5818
EUR_USD = 6238.80/6019.56

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

def getBitso():
    URL = "https://api.bitso.com/v3/ticker?book=btc_mxn"
    try:
        r = requests.get(URL)
        priceFloat = float(json.loads(r.text)['payload']['last'])*MXN_USD
        return priceFloat
    except KeyboardInterrupt:
        exit()
    except: #requests.ConnectionError:
        return "get error"

def getCoinMetro():
    URL = "https://exchange.coinmetro.com/open/prices/BTCEUR"
    try:
        r = requests.get(URL)
        priceFloat = float(json.loads(r.text)['latestPrices'][0]['price'])*EUR_USD
        return priceFloat
    except KeyboardInterrupt:
        exit()
    except: #requests.ConnectionError:
        return "get error"

progStart = time.time()
lastFinexFetch = time.time()

while True:
    fetchTime = localtime()
    iterTime = time.time()
    #look for kill command
    endProc=open("kill_process", "r")
    endProcCont =endProc.read()
    if endProcCont[:4] == "true":
        exit()
    endProc.close()
    if True: #int(strftime("%M", fetchTime)) % 10 == 0: #minute is a multiple of 10
        #create folder and header
        if not os.path.exists('datedCSV/' + strftime("%Y-%m-%d", fetchTime)):
            os.mkdir('datedCSV/' + strftime("%Y-%m-%d", fetchTime))
        if not os.path.exists('datedCSV/' + strftime("%Y-%m-%d", fetchTime) + '/BTC_' + strftime("%H", fetchTime) + '.csv'): #file does not yet exist
            f=open('datedCSV/' + strftime("%Y-%m-%d", fetchTime) + '/BTC_' + strftime("%H", fetchTime) + '.csv', "a+")
            f.write("Time,Kraken,Bitstamp,Bitfinex,Bitflyer,Itbit,Bitso,CoinMetro\r\n")
            f.close()

        #fetch and log code
        try:
            #run fetching calls
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
            lastBitso = str(getBitso())
            lastCoinMetro = str(getCoinMetro())
            print("\r\n" + strftime("%Y-%m-%d %H:%M:%S", fetchTime))
            #update print to be a function eventually with more currencies
            print("Bitstamp: $" + lastBitstamp.ljust(7, '0')[:7] + "    Itbit: $" + lastItbit.ljust(7, '0')[:7] + "    Kraken: $" + lastKraken.ljust(7, '0')[:7] + "    Bitfinex: $" + lastBitfinex.ljust(7, '0')[:7])
            #file handling
            if not os.path.exists('datedCSV/' + strftime("%Y-%m-%d", fetchTime)):
                os.mkdir('datedCSV/' + strftime("%Y-%m-%d", fetchTime))
            f=open('datedCSV/' + strftime("%Y-%m-%d", fetchTime) + '/BTC_' + strftime("%H", fetchTime) + '.csv', "a+")
            f.write(strftime("%Y-%m-%d %H:%M:%S", fetchTime) + " , " + lastKraken + " , " + lastBitstamp + " , " + lastBitfinex + " , " + lastBitflyer + " , " + lastItbit + " , " + lastBitso + " , " + lastCoinMetro + "\r\n")
            f.close()
        except KeyboardInterrupt:
            exit()
        except SystemExit:
            exit()
        except:
            print("------------------ERROR------------------")
            print(sys.exc_info())
            if not os.path.exists('datedCSV/' + strftime("%Y-%m-%d", localtime())):
                os.mkdir('datedCSV/' + strftime("%Y-%m-%d", localtime()))
            f=open('datedCSV/' + strftime("%Y-%m-%d", localtime()) + '/BTC_' + strftime("%H", localtime()) + '.csv', "a+")
            f.write(strftime("%Y-%m-%d %H:%M:%S", localtime()) + " , " + "ERROR" + " , " + "ERROR" + " , " + "ERROR" + " , " + str(sys.exc_info()) + "\r\n")
            f.close()
    else:
        #sleep and wait
        sleep(2)
