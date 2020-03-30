#getBitfinex(): #GENERATING KEY ERRORS bc rate
1, "https://api.bitfinex.com/v1/pubticker/btcusd", 'last_price'

#getKraken():
"https://api.kraken.com/0/public/Ticker?pair=XBTUSD"
['result']['XXBTZUSD']['c'][0]

#getBitflyer():
1, "https://api.bitflyer.com/v1/ticker?product_code=BTC_USD", 'ltp'

#getItbit():
1, "https://api.itbit.com/v1/markets/XBTUSD/ticker",'lastPrice'

#getBitso():
MXN_USD, "https://api.bitso.com/v3/ticker?book=btc_mxn", 'payload','last'

#getCoinMetro():
EUR_USD, "https://exchange.coinmetro.com/open/prices/BTCEUR", 'latestPrices', 0, 'price'





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

