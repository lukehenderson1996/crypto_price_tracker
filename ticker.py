#Luke Henderson
#Version 1.0
import requests, json
import time
from time import sleep, localtime, strftime
import sys
import os


CSV_HEADER = "Time,Kraken,Bitstamp,Bitfinex,Bitflyer\r\n"

MXN_USD = 1/23.5818
EUR_USD = 6238.80/6019.56

def getLastPrice(*args): #num of args will be 3 to 6 -> 0:currMult, 1:URL, 2:Key0, 3:[Key1], 4:[Key2], 5:[Key3]
    URL = args[1]
    try:
        r = requests.get(URL)
        if len(args) == 3:
            priceFloat = float(json.loads(r.text)[args[2]])*args[0]
        elif len(args) == 4:
            priceFloat = float(json.loads(r.text)[args[2]][args[3]])*args[0]
        elif len(args) == 5:
            priceFloat = float(json.loads(r.text)[args[2]][args[3]][args[4]])*args[0]
        else:
            priceFloat = float(json.loads(r.text)[args[2]][args[3]][args[4]][args[5]])*args[0]
        return str(priceFloat)
    except KeyboardInterrupt:
        exit()
    except: # requests.ConnectionError:
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
            f.write(CSV_HEADER)
            f.close()

        #fetch and log code
        try:


            #run fetching calls----------------------------------------------------------------------------------------------------------------------------------------
            lastBitstamp = getLastPrice(1, 'https://www.bitstamp.net/api/ticker/', 'last') #bitstamp
            if time.time()-lastFinexFetch > 6: #4 seconds caused errors on 03-17 4PM
                try:
                    lastBitfinex = getLastPrice(1, "https://api.bitfinex.com/v1/pubticker/btcusd", 'last_price') #getBitfinex(): #GENERATING KEY ERRORS bc rate
                    lastFinexFetch = time.time()
                except KeyboardInterrupt:
                    exit()
                except:
                    lastBitfinex = "str() error"
            else:
                lastBitfinex = "       "
            lastKraken = getLastPrice(1, "https://api.kraken.com/0/public/Ticker?pair=XBTUSD", 'result','XXBTZUSD','c',0) #getKraken():
            lastBitflyer = getLastPrice(1, "https://api.bitflyer.com/v1/ticker?product_code=BTC_USD", 'ltp') #getBitflyer():
            # lastItbit = getLastPrice(1, "https://api.itbit.com/v1/markets/XBTUSD/ticker",'lastPrice') #getItbit():
            # lastBitso = getLastPrice(MXN_USD, "https://api.bitso.com/v3/ticker?book=btc_mxn", 'payload','last') #getBitso():
            # lastCoinMetro = getLastPrice(EUR_USD, "https://exchange.coinmetro.com/open/prices/BTCEUR", 'latestPrices', 0, 'price') #getCoinMetro():


            print("\r\n" + strftime("%Y-%m-%d %H:%M:%S", fetchTime))
            #update print to be a function eventually with more currencies
            print("Bitstamp: $" + lastBitstamp.ljust(7, '0')[:7] + "    Kraken: $" + lastKraken.ljust(7, '0')[:7] + "    Bitfinex: $" + lastBitfinex.ljust(7, '0')[:7])
            #file handling
            if not os.path.exists('datedCSV/' + strftime("%Y-%m-%d", fetchTime)):
                os.mkdir('datedCSV/' + strftime("%Y-%m-%d", fetchTime))
            f=open('datedCSV/' + strftime("%Y-%m-%d", fetchTime) + '/BTC_' + strftime("%H", fetchTime) + '.csv', "a+")
            f.write(strftime("%Y-%m-%d %H:%M:%S", fetchTime) + " , " + lastKraken + " , " + lastBitstamp + " , " + lastBitfinex + " , " + lastBitflyer + "\r\n")
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
