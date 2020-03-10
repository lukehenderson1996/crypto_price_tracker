import requests, json
from time import sleep

import logging

# create logger
lgr = logging.getLogger('BTC PRICE')
lgr.setLevel(logging.DEBUG) # log all escalated at and above DEBUG
# add a file handler
fh = logging.FileHandler('BTC.csv')
fh.setLevel(logging.DEBUG) # ensure all messages are logged to file

# create a formatter and set the formatter for the handler.
frmt = logging.Formatter('%(asctime)s,%(name)s,%(levelname)s,%(message)s')
fh.setFormatter(frmt)

# add the Handler to the logger
lgr.addHandler(fh)

# You can now start issuing logging statements in your code
#lgr.debug('a debug message')
#lgr.info('an info message')
#lgr.warn('A Checkout this warning.')
#lgr.error('An error writen here.')
#lgr.critical('Something very critical happened.')



def getBitcoinPrice():
    URL = 'https://www.bitstamp.net/api/ticker/'
    try:
        r = requests.get(URL)
        priceFloat = float(json.loads(r.text)['last'])
        return priceFloat
    except requests.ConnectionError:
        print "Error querying Bitstamp API"

while True:
        currPrice = str(getBitcoinPrice())
	print "Bitstamp last price: $" + currPrice + "/BTC"
        lgr.info(currPrice)
        sleep(3) 
