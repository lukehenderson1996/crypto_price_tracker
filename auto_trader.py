#Luke Henderson
#Version 1.0
#Solely for BaseFEX use
import requests, json
import time
from time import sleep, localtime, strftime
import sys, traceback
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
#for logging
from logger_auto_trader import *

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



def getActiveOrderList(symbol): #symbol: BTCUSD, BTCUSDT
    http_method = 'GET'
    #path helper: https://api.basefex.com/orders?symbol=BTCUSD&type=LIMIT&side=BUY&status=NEW&limit=30
    path = '/orders/opening?symbol=' + symbol
    url = 'https://api.basefex.com' + path
    timestamp = time.time()
    expires = int(round(timestamp) + 30)
    data = '' # empty request body
    logDataObj = logData()
    logDataObj.request_type = "getActiveOrderList"
    logDataObj.symbol = symbol
    logDataObj = execute_request(http_method, url, path, expires, data, logDataObj)
    upLogs(logDataObj)
    return logDataObj


def checkOrder(id): #Get order information by order id
    http_method = 'GET'
    #path helper: https://api.basefex.com/orders?symbol=BTCUSD&type=LIMIT&side=BUY&status=NEW&limit=30
    path = '/orders/' + id
    url = 'https://api.basefex.com' + path
    timestamp = time.time()
    expires = int(round(timestamp) + 30)
    data = '' # empty request body
    logDataObj = logData()
    logDataObj.request_type = "checkOrder"
    logDataObj.id = id
    logDataObj = execute_request(http_method, url, path, expires, data, logDataObj)
    logDataObj.filled = json.loads(logDataObj.serverResponseJSON.text)['filled']
    if logDataObj.filled!=0:
        logDataObj.excPrice = json.loads(logDataObj.serverResponseJSON.text)['avgPrice']
    else:
        logDataObj.excPrice = None
    upLogs(logDataObj)
    return logDataObj


#POST USDT order buy/sell
def placeOrderUSDT(size, type, side, price):
    try:
        http_method = 'POST'
        path = '/orders'
        url = 'https://api.basefex.com' + path
        timestamp = time.time()
        expires = int(round(timestamp) + 30)
        if price == None:
            data = {
                "size": size,
                "symbol": "BTCUSDT",
                "type": type,
                "side": side,
                }
        else:
            data = {
                "size": size,
                "symbol": "BTCUSDT",
                "type": type,
                "side": side,
                "price": price
                }

        logDataObj = logData()
        logDataObj.request_type = "placeOrderUSDT-" + side
        logDataObj = execute_request(http_method, url, path, expires, data, logDataObj)
        if not hasattr(logDataObj, 'error'):
            logDataObj.orderID = None#json.loads(logDataObj.serverResponseJSON.text)['id']
        else:
            logDataObj.orderID == None
        print(bcolors.OKBLUE  + side + " order executed" + bcolors.ENDC)
        upLogs(logDataObj)
        return logDataObj
    except KeyboardInterrupt:
        exit() #add this in outer layer if you run into trouble: except SystemExit: exit()
    except:
        print(bcolors.FAIL  + "------------------ERROR------------------" + bcolors.ENDC)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logDataObj.error_msg = str(traceback.format_exception(exc_type, exc_value, exc_traceback))
        traceback.print_exc()
        print(bcolors.FAIL  + "//////////////////ERROR//////////////////" + bcolors.ENDC)
        logDataObj.error = True
        logDataObj.error_placeOrderUSDT = True
        logDataObj.request_type = "placeOrderUSDT-" + side
        logDataObj.orderID == None
        upLogs(logDataObj)
        return logDataObj



#POST BTC order buy/sell
def placeOrderBTC(size, type, side):
    http_method = 'POST'
    path = '/orders'
    url = 'https://api.basefex.com' + path
    timestamp = time.time()
    expires = int(round(timestamp) + 30)
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
    logDataObj = logData()
    logDataObj.request_type = "placeOrderBTC-" + side
    logDataObj = execute_request(http_method, url, path, expires, data, logDataObj)
    print(bcolors.OKBLUE  + side + " order executed" + bcolors.ENDC)
    upLogs(logDataObj)
    return logDataObj


def verifyContracts(num):
    contractsGoalMet = False
    while contractsGoalMet==False:
        logDataObj = getPositionContracts('BTC', 'BTCUSD')
        if not hasattr(logDataObj, 'error'):
            positionContracts = logDataObj.positionContracts
            if not positionContracts == None:
                if positionContracts==num:
                    contractsGoalMet = True
                elif positionContracts != num:
                    if positionContracts > num:
                        logDataObj = placeOrderBTC(positionContracts-num, "MARKET", "SELL")
                    elif positionContracts < num:
                        logDataObj = placeOrderBTC(num-positionContracts, "MARKET", "BUY")
                    sleep(3)
            else:
                sleep(2)
        else:
            sleep(2)





#GET last price,
def getLastPrice():
    http_method = 'GET'
    path = '/depth@BTCUSD/snapshot'
    url = 'https://api.basefex.com' + path
    timestamp = time.time()
    expires = int(round(timestamp) + 30)
    data = '' # empty request body
    logDataObj = logData()
    logDataObj.request_type = "getLastPrice"
    logDataObj = execute_request(http_method, url, path, expires, data, logDataObj)
    if not hasattr(logDataObj, 'error'):
        logDataObj.lastBaseFEX = getPriceFloat(logDataObj.serverResponseJSON, 'lastPrice')
        logDataObj.highestBidBaseFEX = getPriceFloat(logDataObj.serverResponseJSON, 'bestPrices', 'bid')
        # print(bcolors.ENDC  + "Last price: " + str(logDataObj.lastBaseFEX) + bcolors.ENDC)
    else:
        logDataObj.lastBaseFEX = None
        logDataObj.highestBidBaseFEX = None
    upLogs(logDataObj)
    return logDataObj

#GET account value, currency= 'BTC', 'USDT'
def getCashBalances(currency):
    http_method = 'GET'
    path = '/accounts'
    url = 'https://api.basefex.com' + path
    timestamp = time.time()
    expires = int(round(timestamp) + 30)
    data = '' # empty request body
    logDataObj = logData()
    logDataObj.request_type = "getCashBalances"
    logDataObj = execute_request(http_method, url, path, expires, data, logDataObj)
    try:
        serverResponseDict = json.loads(logDataObj.serverResponseJSON.text)
        for i in range(len(serverResponseDict)):
            if serverResponseDict[i]['cash']['currency']==currency:
                currencyKey = i
        logDataObj.cash_balance = json.loads(logDataObj.serverResponseJSON.text)[currencyKey]['cash']['balances']
    except KeyboardInterrupt:
        exit()
    except:
        logDataObj.cash_balance = None
    print(bcolors.OKBLUE  + "Cash balance: " + str(logDataObj.cash_balance) + bcolors.ENDC)
    upLogs(logDataObj)
    return logDataObj

#GET num of contracts, currency: 'BTC', 'USDT', symbol: 'BTCUSD', 'BTCUSDT'
def getPositionContracts(currency, symbol):
    http_method = 'GET'
    path = '/accounts'
    url = 'https://api.basefex.com' + path
    timestamp = time.time()
    expires = int(round(timestamp) + 30)
    data = '' # empty request body
    logDataObj = logData()
    logDataObj.request_type = "getPositionContracts"
    logDataObj = execute_request(http_method, url, path, expires, data, logDataObj)
    try:
        serverResponseDict = json.loads(logDataObj.serverResponseJSON.text)
        for i in range(len(serverResponseDict)):
            if serverResponseDict[i]['cash']['currency']==currency:
                currencyKey = i
        positionsDict = json.loads(logDataObj.serverResponseJSON.text)[currencyKey]['positions']
        for i in range(len(positionsDict)):
            if positionsDict[i]['symbol']==symbol:
                symKey = i
        logDataObj.positionContracts = json.loads(logDataObj.serverResponseJSON.text)[currencyKey]['positions'][symKey]['size'] #BTC or USDT position
    except KeyboardInterrupt:
        exit()
    except:
        logDataObj.positionContracts = None
    print(bcolors.OKBLUE  + "Number of contracts: " + str(logDataObj.positionContracts) + bcolors.ENDC)
    upLogs(logDataObj)
    return logDataObj

#assumes static apiSecret, apiKey
def execute_request(http_method, url, path, expires, data, logDataObj):
    try:
        # raise requests.ConnectionError
        #condition data
        if len(data) != 0:
            strData = json.dumps(data)
        else:
            strData = ''

        #create signature
        tokenString = http_method + path + str(expires) + strData
        signature = generate_signature(apiSecret, http_method, path, expires, strData)
        auth_token = signature
        # print("String: " + tokenString)
        # print("signature: " + signature)
        #create header
        hed = {'api-expires':str(expires),'api-key':apiKey,'api-signature':str(auth_token)}

        logDataObj.timestamp = time.time()
        logDataObj.string = tokenString
        logDataObj.signature = signature

        #fulfill server request
        if http_method == 'GET':
            response = requests.get(url, headers=hed, timeout=5)
        elif http_method == 'POST':
            response = requests.post(url, headers=hed, json=data, timeout=5)

        # print(bcolors.OKBLUE  + "Server response: " + bcolors.ENDC)
        # print(response.__dict__)
        # # print(json.dumps(parsedJSON, indent=4, sort_keys=True))
        # print(bcolors.OKBLUE  + "//Server response//" + bcolors.ENDC)

        logDataObj.response_status_code = response.status_code
        logDataObj.serverResponseJSON = response
        parsedJSON = json.loads(response.text) #whole JSON object
        logDataObj.server_response = json.dumps(parsedJSON, indent=4, sort_keys=True)
        if not response.status_code == 200:
            raise requests.HTTPError
        logDataObj.RateLimit_Remaining = response.headers['X-RateLimit-Remaining']

        return logDataObj
    except KeyboardInterrupt:
        exit() #add this in outer layer if you run into trouble: except SystemExit: exit()
    except:
        print(bcolors.FAIL  + "------------------ERROR------------------" + bcolors.ENDC)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logDataObj.error_msg = str(traceback.format_exception(exc_type, exc_value, exc_traceback))
        traceback.print_exc()
        print(bcolors.FAIL  + "//////////////////ERROR//////////////////" + bcolors.ENDC)
        logDataObj.timestamp = time.time()
        logDataObj.http_method = http_method
        logDataObj.url = url
        logDataObj.path = path
        logDataObj.expires = expires
        logDataObj.data = data
        logDataObj.error = True
        logDataObj.error_execute_request = True
        return logDataObj



# The algorithm is: hex(HMAC_SHA256(secret, http_method + path + expires + data))
# Upper-cased http_method, relative request path, unix timestamp expires.
# data is json string
def generate_signature(apiSecret, http_method, path, expires, strData):
    message = bytes(http_method + path + str(expires) + strData, 'utf-8')
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
        return priceFloat
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
    exit()

initLogs()

# #init algorith 0.2 (use with USDT)
# sumChangeExp = 0.0
# sumChangeAct = 0.0
# print("Expected cumulative gain/loss: " + bcolors.OKGREEN + str(sumChangeExp)[:5] + '%' + bcolors.ENDC)
# print("Actual gain/loss: " + bcolors.OKGREEN + str(sumChangeAct)[:5] + '%' + bcolors.ENDC)





#main loop
while True:

    try:



        #loop algorith 0.2




        # logDataObj = placeOrderUSDT(1, "LIMIT", "BUY", 1000)
        logDataObj = getActiveOrderList('BTCUSDT')
        serverResponseDict = json.loads(logDataObj.serverResponseJSON.text)
        print(len(serverResponseDict))
        # print(logDataObj.server_response)
        exit()



        # run test
        # todo:placeOrderUSDT now has error control, put that in every function next!
        # todo:make logV parser with input('what file to parse?') and input('what tag to parse?') and input('what value to parse?'), but save the whole entry if it includes that tag/value
        #      and then make a version where it doesnt include the tag/value?
        # verify contracts: if an order doesnt get filled, what to do?
        #then, after all is filled and gone as planned, check that there are no active orders AND that the number of contracts is what was expected (if not, adjust and go back to step one)
        orderPlaced = False
        while orderPlaced == False:
            logDataObj = placeOrderUSDT(1, "LIMIT", "BUY", 1000) #example: 1, "MARKET", "SELL", None      or      1, "LIMIT", "BUY", 8000
            if not logDataObj.orderID == None:
                orderPlaced = True
            else:
                #wait a second and check on active orders, to see if it went through
                #UPDATE THIS: if the order did go through, it's probably already filled, so check position contracts.
                sleep(10)
                # logDataObj = logDataErrVfctn()
                # while hasattr(logDataObj, 'error'):
                #     logDataObj = getActiveOrderList('BTCUSDT')
                # #if the order did not go through
                # serverResponseDict = json.loads(logDataObj.serverResponseJSON.text)
                # print(len(serverResponseDict))
                # if len(serverResponseDict)==0:
                #     pass
                # #if the order did go through
                # elif len(serverResponseDict)==1:
                #     #save order id
                #     orderPlaced = True
                # #if the program lost track of how many orders, or an order was doubled
                # else:
                #     print(bcolors.FAIL  + "Error: Number of orders = " + str(len(serverResponseDict)) + bcolors.ENDC)
                #     exit()

        #check to see if it's filled
        logDataObj = checkOrder(logDataObj.orderID) #example: '5c55eeea-959a-4bcd-0005-fcbf01ba8a44'
        #produces logDataObj.filled, logDataObj.excPrice (execution price)

        #...




        print(logDataObj.server_response)
        # print(bcolors.OKBLUE + str(json.loads(logDataObj.serverResponseJSON.text)['filled']) + bcolors.ENDC)
        # print(logDataObj.filled)


        #examples:

        # #get last price
        # logDataObj = getLastPrice() #gives logDataObj.lastBaseFEX and logDataObj.highestBidBaseFEX

        # #get cash balance
        # logDataObj = getCashBalances('BTC') #'BTC', 'USDT'

        # #get num of contracts
        # logDataObj = getPositionContracts('USDT', 'BTCUSDT') #'BTC', 'BTCUSD' or 'USDT', 'BTCUSDT'

        # #place order
        # logDataObj = placeOrderBTC(size, type, side) #example: 10, "MARKET", "BUY"
        # logDataObj = placeOrderUSDT(1, "LIMIT", "BUY", 1000) #example: 1, "MARKET", "SELL", None      or      1, "LIMIT", "BUY", 8000
        # #produces logDataObj.orderID

        # #verifyContracts
        # verifyContracts(num)

        # #get active order list
        # logDataObj = getActiveOrderList(symbol) #symbol: BTCUSD, BTCUSDT

        # #check specific order
        # logDataObj = checkOrder(id) #example: '5c55eeea-959a-4bcd-0005-fcbf01ba8a44'
        # #produces logDataObj.filled, logDataObj.excPrice (execution price)




        exit()

    #outer error handling:
    except KeyboardInterrupt:
        exit()
    except SystemExit:
        # print(bcolors.WARNING  + " Reached outer 'except SystemExit:'")
        exit()
    except:
        print(bcolors.FAIL  + "------------------ERROR(outer layer)------------------" + bcolors.ENDC)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exc()
        print(bcolors.FAIL  + "//////////////////ERROR(outer layer)//////////////////" + bcolors.ENDC)
        exit()
















#end
