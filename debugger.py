#updated for python 3 usage
import requests, json
import time
from time import sleep, localtime, strftime
import sys
import os
import logging
from parse import *

#make text look unique
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# print(bcolors.FAIL)
# print(DEBUG_TOOL)
# print(bcolors.ENDC)

# print(bcolors.WARNING + "Success!" + bcolors.ENDC)
# exit()

class Obj:
    pass

data = {
        "asks": {
            "6694": 279,
            "6697": 199,
            "6699.5": 259,
            "6701.5": 513,
            "6702": 1493,
            "6702.5": 1493,
            "6703.5": 1493,
            "6704": 1493,
            "6707": 5,
            "6707.5": 4340,
            "6708.5": 717,
            "6709.5": 116,
            "6710": 1491,
            "6713": 2346,
            "6713.5": 531,
            "6714": 1,
            "6715": 3896,
            "6715.5": 2477,
            "6717": 1449,
            "6717.5": 894,
            "6720": 110,
            "6721": 50,
            "6721.5": 47,
            "6722.5": 24
        },
        "bestPrices": {
            "ask": 6694,
            "bid": None
        },
        "bids": {},
        "from": 0,
        "lastPrice": 6712.0,
        "to": 155251581
    }

obj1 = Obj()
obj1.text = json.dumps(data)

priceText = json.loads(obj1.text)['bestPrices']['bid']
print(priceText)
print('text done')
priceFloat = float(priceText)
print (priceFloat)

print("done")
























#end
