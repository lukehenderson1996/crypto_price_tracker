#Luke Henderson
#Version info on ticker.py
#Solely for BaseFEX use
import requests, json
import time
from time import sleep, localtime, strftime
import sys
import os
from parse import * #pip install parse (or pip3 install parse)
#from basefex api
# from datetime import datetime # don't use, just use time.time()
# import hashlib
# import hmac
# from urllib.parse import urlparse
# import json
#from https://www.jokecamp.com/blog/examples-of-creating-base64-hashes-using-hmac-sha256-in-different-languages/#python3
import hashlib
import hmac
import base64

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



#POST order buy/sell
def placeOrder(size, type, side):
    http_method = 'POST'
    path = '/orders'
    url = 'https://api.basefex.com' + path
    timestamp = time.time()
    expires = int(round(timestamp) + 5)
    # data = {
    #     "size": 5,
    #     "symbol": "BTCUSD",
    #     "type": "MARKET",
    #     "side": "BUY"
    #     }
    data = {
        "size": size,
        "symbol": "BTCUSD",
        "type": type,
        "side": side
        }
    execute_request(http_method, url, path, expires, data)

#GET last price
def getLastPrice():
    http_method = 'GET'
    path = '/depth@BTCUSD/snapshot'
    url = 'https://api.basefex.com' + path
    timestamp = time.time()
    expires = int(round(timestamp) + 5)
    data = '' # empty request body
    priceResponse = execute_request(http_method, url, path, expires, data)
    lastBaseFEX = getPriceFloat(priceResponse, 'lastPrice')
    return lastBaseFEX

#GET account info
def getAccountInfo():
    http_method = 'GET'
    path = '/accounts'
    url = 'https://api.basefex.com' + path
    timestamp = time.time()
    expires = int(round(timestamp) + 5)
    data = '' # empty request body
    getResponse = execute_request(http_method, url, path, expires, data)
    return getResponse

#assumes static apiSecret, apiKey
def execute_request(http_method, url, path, expires, data):
    print("http_method = " + http_method)
    print("path = " + path)
    print("expires  = " + str(expires))
    print("data = ")
    print(json.dumps(data))

    print("String: " + http_method + path + str(expires) + data)
    print("Secret: " + apiSecret)
    #create signature
    signature = generate_signature(apiSecret, http_method, path, expires, json.dumps(data))
    auth_token = signature
    print("signature: " + signature)
    #create header
    hed = {'api-expires':str(expires),'api-key':apiKey,'api-signature':str(auth_token)}

    #fulfill server request
    if http_method == 'GET':
        response = requests.get(url, headers=hed)
    elif http_method == 'POST':
        response = requests.post(url, headers=hed, json=data)
    else:
        print(bcolors.FAIL  + "Error: invalid HTTP method" + bcolors.ENDC)
        exit()
    print(bcolors.OKBLUE  + "Server response: " + bcolors.ENDC)
    parsedJSON = json.loads(response.text) #whole JSON object
    print(json.dumps(parsedJSON, indent=4, sort_keys=True))
    return response

# The algorithm is: hex(HMAC_SHA256(secret, http_method + path + expires + data))
# Upper-cased http_method, relative request path, unix timestamp expires.
# data is json string
def generate_signature(apiSecret, http_method, path, expires, data):
    message = bytes(http_method + path + str(expires) + data, 'utf-8')
    secret = bytes(apiSecret, 'utf-8')
    signature = hmac.new(secret, message, digestmod=hashlib.sha256).digest().hex()
    return signature


# takes JSON object priceResponse and returns keyed last price
def getPriceFloat(*args): #num of args will be 2 to 5 -> 0:JSON object, 1:Key0, 2:[Key1], 3:[Key2], 4:[Key3]
    try:
        if len(args) == 2:
            priceFloat = float(json.loads(args[0].text)[args[1]])
        elif len(args) == 3:
            priceFloat = float(json.loads(args[0].text)[args[1]][args[2]])
        elif len(args) == 4:
            priceFloat = float(json.loads(args[0].text)[args[1]][args[2]][args[3]])
        else:
            priceFloat = float(json.loads(args[0].text)[args[1]][args[2]][args[3]][args[4]])
        return str(priceFloat)
    except KeyboardInterrupt:
        exit()
    except:
        print(bcolors.FAIL  + "Error: getPriceFloat error" + bcolors.ENDC)
        print(sys.exc_info())
        exit()


#init code
if os.path.exists('keys/keys.xml'): #file exists
    #read file for API keys
    keysFile = open("keys/keys.xml", "r")
    keysFileCont =keysFile.read()
    xmlKeys = search("<keys>{}</keys>", keysFileCont)[0]
    xmlBFKeys = search("<baseFEX>{}</baseFEX>", xmlKeys)[0]
    apiKey = search("<API_key>{}</API_key>", xmlBFKeys)[0] # id of api key
    apiSecret = search("<private_key>{}</private_key>", xmlBFKeys)[0] # api secret
    keysFile.close()
else:
    print(bcolors.FAIL  + "Error: API keys file does not exist" + bcolors.ENDC)




#main loop
while True:


    #GET with current time
    http_method = 'GET'
    path = '/accounts'
    # path = '/orders?symbol=BTCUSD' #not sure what this is for
    url = 'https://api.basefex.com' + path
    timestamp = time.time()
    expires = int(round(timestamp) + 5)
    data = '' # empty request body
    # parsedJSON = json.loads(response.text)[0]['positions'][4] #BTC position



#
# auth_token = generate_signature(secret, "GET", path, expires, data)
# hed = {'api-expires':str(expires),'api-key':key_id,'api-signature':str(auth_token)}
# response = requests.get(url, headers=hed)
# print(response.json())





    #execute request
    print("http_method = " + http_method)
    print("path = " + path)
    print("expires  = " + str(expires))
    print("data = ")
    print(json.dumps(data))

    print("String: " + http_method + path + str(expires) + data)
    print("Secret: " + apiSecret)
    #create signature
    print(bcolors.WARNING)
    print(len(data)==0)
    print(bcolors.ENDC)
    exit()
    signature = generate_signature(apiSecret, http_method, path, expires, json.dumps(data))
    auth_token = signature
    print("signature: " + signature)
    #create header
    hed = {'api-expires':str(expires),'api-key':apiKey,'api-signature':str(auth_token)}

    #fulfill server request
    if http_method == 'GET':
        response = requests.get(url, headers=hed)
    elif http_method == 'POST':
        response = requests.post(url, headers=hed, json=data)
    else:
        print(bcolors.FAIL  + "Error: invalid HTTP method" + bcolors.ENDC)
        exit()
    print(bcolors.OKBLUE  + "Server response: " + bcolors.ENDC)
    parsedJSON = json.loads(response.text) #whole JSON object
    print(json.dumps(parsedJSON, indent=4, sort_keys=True))










    exit()

























#end
