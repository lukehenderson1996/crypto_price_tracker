import requests, json
from time import sleep

import logging

# create logger
lgr = logging.getLogger('BTC PRICE')
lgr.setLevel(logging.DEBUG) # log all escalated at and above DEBUG
# add a file handler
fh = logging.FileHandler('csv/BTC.csv')
fh.setLevel(logging.DEBUG) # ensure all messages are logged to file

# create a formatter and set the formatter for the handler.
frmt = logging.Formatter('%(asctime)s,%(name)s,%(levelname)s,%(message)s')
#frmt = logging.Formatter('%(asctime)s,%(message)s',)
fh.setFormatter(frmt)

# add the Handler to the logger
lgr.addHandler(fh)

# You can now start issuing logging statements in your code
#lgr.debug('a debug message')
#lgr.info('an info message')
#lgr.warn('A Checkout this warning.')
#lgr.error('An error writen here.')
#lgr.critical('Something very critical happened.')



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

while True:
        lastBitstamp = str(getBitstamp())
        lastBitfinex = str(getBitfinex())
        lastKraken = str(getKraken())
	print "Bitstamp: $" + lastBitstamp + "    Bitfinex: $" + lastBitfinex + "    Kraken: $" + lastKraken
        #print "Bitfinex last price: $" + lastBitfinex + "/BTC"
        #print "Kraken last price: $" + lastKraken + "/BTC"
        
        lgr.info(lastBitstamp)
        lgr.info(lastBitfinex)
        lgr.info(lastKraken)
        sleep(4) 
