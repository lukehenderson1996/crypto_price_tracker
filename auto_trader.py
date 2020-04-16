#Luke Henderson
#Version 2.0
#Solely for BaseFEX use
import requests, json
import time
from time import sleep, localtime, strftime
import sys, traceback
import os
from parse import * #pip install parse (or pip3 install parse)
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


C_TO_TRD = 1 #contracts to trade with constant
RATE_LIMIT_SLEEP = 0.38 #180 per minute -> 1 call per 0.33 secondsy


#wait until order get filled
def waitUntilOrderFill(id): #example: '5c55eeea-959a-4bcd-0005-fcbf01ba8a44'
    orderFilledFlag = False
    while orderFilledFlag == False:
        if not id == 'unknown': #if it is unknown, the order is already filled
            logDataObj = logDataErrVfctn()
            while hasattr(logDataObj, 'error'):
                logDataObj = checkOrder(id)
            if logDataObj.filled == C_TO_TRD:
                # excPrice = logDataObj.excPrice #not needed because check order is the only API call in here
                orderFilledFlag = True
            elif logDataObj.orderStatus=='REJECTED':
                logDataObj.error = True
                logDataObj.error_waitUntilOrderFill = True
                logDataObj.error_msg = 'Internal error: orderStatus is REJECTED '
                return logDataObj
            elif logDataObj.filled == 0:
                pass
            else:
                print(bcolors.FAIL  + "Error: Number of contracts to trade with = " + str(C_TO_TRD) + bcolors.ENDC)
                print(bcolors.FAIL  + "       Number of filled orders           = " + str(logDataObj.filled) + bcolors.ENDC)
                exit()
        else: #if the orderID is unknown, the order is filled at an unknown price
            logDataObj = logData()
            logDataObj.request_type = "waitUntilOrderFill"
            logDataObj.timestamp = time.time()
            logDataObj.excPrice = None
            logDataObj.orderID = id
            logDataObj.error = True
            logDataObj.error_waitUntilOrderFill = True
            upLogs(logDataObj)
            orderFilledFlag = True
    return logDataObj


#makes limit order (verified to have excecuted), gives logDataObj.orderID
def verifyOrderUSDT(size, side, price): #example C_TO_TRD, "BUY", 1000
    orderPlaced = False
    while orderPlaced == False:
        logDataObj = placeOrderUSDT(size, "LIMIT", side, price, None)
        orderID = logDataObj.orderID
        if not orderID == None:
            orderPlaced = True
        else:
            #wait a second and check on active orders and position contracts
            sleep(5)
            logDataObj = logDataErrVfctn()
            while hasattr(logDataObj, 'error'):
                logDataObj = getActiveOrderList('BTCUSDT')
            activeOrderIDs = logDataObj.activeOrderIDs

            logDataObj = logDataErrVfctn()
            while hasattr(logDataObj, 'error'):
                logDataObj = getPositionContracts('USDT', 'BTCUSDT')
            positionContracts = logDataObj.positionContracts

            if side=='BUY': #buy
                expectedContracts = C_TO_TRD
                prevContracts = 0
            elif side=='SELL': #sell
                expectedContracts = 0
                prevContracts = C_TO_TRD

            if positionContracts==expectedContracts or len(activeOrderIDs)==1:
                orderPlaced = True
                orderID = 'unknown'
            elif positionContracts==prevContracts and len(activeOrderIDs)==0:
                pass
            else:
                print(bcolors.FAIL  + "Error: Number of expectedContracts = " + str(C_TO_TRD) + bcolors.ENDC)
                print(bcolors.FAIL  + "       Number of prevContracts     = " + str(C_TO_TRD) + bcolors.ENDC)
                print(bcolors.FAIL  + "       Number of positionContracts = " + str(positionContracts) + bcolors.ENDC)
                print(bcolors.FAIL  + "       Number of activeOrderIDs    = " + str(len(activeOrderIDs)) + bcolors.ENDC)
                exit()
    #handle logDataObj
    logDataObj = logData()
    logDataObj.request_type = "verifyOrderUSDT"
    logDataObj.timestamp = time.time()
    logDataObj.orderID = orderID
    return logDataObj

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#INNER API FILE BOUNDARY--------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

def getActiveOrderList(symbol): #symbol: BTCUSD, BTCUSDT
    try:
        sleep(RATE_LIMIT_SLEEP)
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
        serverResponseDict = json.loads(logDataObj.serverResponseJSON.text)
        logDataObj.activeOrderIDs = []
        for i in range(len(serverResponseDict)):
            logDataObj.activeOrderIDs.append(serverResponseDict[i]['id'])
        upLogs(logDataObj)
        return logDataObj
    except KeyboardInterrupt:
        exit()
    except:
        print(bcolors.FAIL  + "------------------ERROR------------------" + bcolors.ENDC)
        print(bcolors.FAIL  + "Error handler getActiveOrderList not comprehensive" + bcolors.ENDC)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logDataObj.error_msg = str(traceback.format_exception(exc_type, exc_value, exc_traceback))
        traceback.print_exc()
        print(bcolors.FAIL  + "//////////////////ERROR//////////////////" + bcolors.ENDC)
        logDataObj.error = True
        logDataObj.error_getActiveOrderList = True
        upLogs(logDataObj)
        exit() #if error handler is not comprehensive
        return logDataObj




def checkOrder(id): #Get order information by order id
    try:
        sleep(RATE_LIMIT_SLEEP)
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
        logDataObj.orderStatus = json.loads(logDataObj.serverResponseJSON.text)['status']
        if logDataObj.filled!=0:
            logDataObj.excPrice = json.loads(logDataObj.serverResponseJSON.text)['avgPrice']
        else:
            logDataObj.excPrice = None
        upLogs(logDataObj)
        return logDataObj
    except KeyboardInterrupt:
        exit() #add this in outer layer if you run into trouble: except SystemExit: exit()
    except:
        print(bcolors.FAIL  + "------------------ERROR------------------" + bcolors.ENDC)
        print(bcolors.FAIL  + "Error handler checkOrder not comprehensive" + bcolors.ENDC)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logDataObj.error_msg = str(traceback.format_exception(exc_type, exc_value, exc_traceback))
        traceback.print_exc()
        print(bcolors.FAIL  + "//////////////////ERROR//////////////////" + bcolors.ENDC)
        logDataObj.error = True
        logDataObj.error_checkOrder = True
        upLogs(logDataObj)
        exit() #if error handler is not comprehensive
        return logDataObj



#POST USDT order buy/sell
def placeOrderUSDT(size, type, side, price, trigPrice):
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
                "side": side
                }
        elif trigPrice==None:
            data = {
                "size": size,
                "symbol": "BTCUSDT",
                "type": type,
                "side": side,
                "price": price
                }
        else:
            data = {
                "size": size,
                "symbol": "BTCUSDT",
                "type": type,
                "side": side,
                "price": price,
                "conditional": {
                    "type": "REACH",
                    "price": trigPrice,
                    "priceType": "MARKET_PRICE"
                }
                }


        logDataObj = logData()
        logDataObj.request_type = "placeOrderUSDT-" + side
        logDataObj = execute_request(http_method, url, path, expires, data, logDataObj)
        if not hasattr(logDataObj, 'error'):
            logDataObj.orderID = json.loads(logDataObj.serverResponseJSON.text)['id']
        else:
            logDataObj.orderID == None
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
    try:
        http_method = 'POST'
        path = '/orders'
        url = 'https://api.basefex.com' + path
        timestamp = time.time()
        expires = int(round(timestamp) + 30)
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
    except KeyboardInterrupt:
        exit() #add this in outer layer if you run into trouble: except SystemExit: exit()
    except:
        print(bcolors.FAIL  + "------------------ERROR------------------" + bcolors.ENDC)
        print(bcolors.FAIL  + "Error handler placeOrderBTC not comprehensive" + bcolors.ENDC)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logDataObj.error_msg = str(traceback.format_exception(exc_type, exc_value, exc_traceback))
        traceback.print_exc()
        print(bcolors.FAIL  + "//////////////////ERROR//////////////////" + bcolors.ENDC)
        logDataObj.error = True
        logDataObj.error_placeOrderBTC = True
        upLogs(logDataObj)
        exit() #if error handler is not comprehensive
        return logDataObj



def verifyContracts(num):
    try:
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
    except KeyboardInterrupt:
        exit() #add this in outer layer if you run into trouble: except SystemExit: exit()
    except:
        print(bcolors.FAIL  + "------------------ERROR------------------" + bcolors.ENDC)
        print(bcolors.FAIL  + "Error handler verifyContracts not comprehensive" + bcolors.ENDC)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logDataObj.error_msg = str(traceback.format_exception(exc_type, exc_value, exc_traceback))
        traceback.print_exc()
        print(bcolors.FAIL  + "//////////////////ERROR//////////////////" + bcolors.ENDC)
        logDataObj.error = True
        logDataObj.error_verifyContracts = True
        upLogs(logDataObj) #if error handler is not comprehensive
        exit() #if error handler is not comprehensive
        return logDataObj







#GET last price,
def getLastPrice():
    try:
        sleep(RATE_LIMIT_SLEEP)
        http_method = 'GET'
        path = '/depth@BTCUSDT/snapshot'
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
            logDataObj.lowestAskBaseFEX = getPriceFloat(logDataObj.serverResponseJSON, 'bestPrices', 'ask')
            # print(bcolors.ENDC  + "Last price: " + str(logDataObj.lastBaseFEX) + bcolors.ENDC)
        else:
            logDataObj.lastBaseFEX = None
            logDataObj.highestBidBaseFEX = None
            logDataObj.lowestAskBaseFEX = None
        if logDataObj.lastBaseFEX==None or logDataObj.highestBidBaseFEX==None or logDataObj.lowestAskBaseFEX==None:
            logDataObj.error = True
            logDataObj.error_getLastPrice = True
            logDataObj.error_msg = 'Internal error: One or more prices was of NoneType'
        upLogs(logDataObj)
        return logDataObj
    except KeyboardInterrupt:
        exit() #add this in outer layer if you run into trouble: except SystemExit: exit()
    except:
        print(bcolors.FAIL  + "------------------ERROR------------------" + bcolors.ENDC)
        print(bcolors.FAIL  + "Error handler getLastPrice not comprehensive" + bcolors.ENDC)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logDataObj.error_msg = str(traceback.format_exception(exc_type, exc_value, exc_traceback))
        traceback.print_exc()
        print(bcolors.FAIL  + "//////////////////ERROR//////////////////" + bcolors.ENDC)
        logDataObj.error = True
        logDataObj.error_getLastPrice = True
        upLogs(logDataObj)
        exit() #if error handler is not comprehensive
        return logDataObj


#GET account value, currency= 'BTC', 'USDT'
def getCashBalances(currency):
    try:
        sleep(RATE_LIMIT_SLEEP)
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
        upLogs(logDataObj)
        return logDataObj
    except KeyboardInterrupt:
        exit() #add this in outer layer if you run into trouble: except SystemExit: exit()
    except:
        print(bcolors.FAIL  + "------------------ERROR------------------" + bcolors.ENDC)
        print(bcolors.FAIL  + "Error handler getCashBalances not comprehensive" + bcolors.ENDC)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logDataObj.error_msg = str(traceback.format_exception(exc_type, exc_value, exc_traceback))
        traceback.print_exc()
        print(bcolors.FAIL  + "//////////////////ERROR//////////////////" + bcolors.ENDC)
        logDataObj.error = True
        logDataObj.error_functionName = True
        upLogs(logDataObj)
        exit() #if error handler is not comprehensive
        return logDataObj


#GET num of contracts, currency: 'BTC', 'USDT', symbol: 'BTCUSD', 'BTCUSDT'
def getPositionContracts(currency, symbol):
    try:
        sleep(RATE_LIMIT_SLEEP)
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
        upLogs(logDataObj)
        return logDataObj
    except KeyboardInterrupt:
        exit() #add this in outer layer if you run into trouble: except SystemExit: exit()
    except:
        print(bcolors.FAIL  + "------------------ERROR------------------" + bcolors.ENDC)
        print(bcolors.FAIL  + "Error handler getPositionContracts not comprehensive" + bcolors.ENDC)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logDataObj.error_msg = str(traceback.format_exception(exc_type, exc_value, exc_traceback))
        traceback.print_exc()
        print(bcolors.FAIL  + "//////////////////ERROR//////////////////" + bcolors.ENDC)
        logDataObj.error = True
        logDataObj.error_getPositionContracts = True
        upLogs(logDataObj)
        exit() #if error handler is not comprehensive
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
            logDataObj.http_method = http_method
            logDataObj.url = url
            logDataObj.path = path
            logDataObj.expires = expires
            logDataObj.data = data
            logDataObj.error = True
            logDataObj.error_execute_request = True
            logDataObj.error_raise_requests_HTTPError = True
            upLogs(logDataObj)
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
            priceText = json.loads(args[0].text)[args[1]]
        elif len(args) == 3:
            priceText = json.loads(args[0].text)[args[1]][args[2]]
        elif len(args) == 4:
            priceText = json.loads(args[0].text)[args[1]][args[2]][args[3]]
        else:
            priceText = json.loads(args[0].text)[args[1]][args[2]][args[3]][args[4]]
        if not priceText == None:
            return float(priceText)
        else:
            return None
    except KeyboardInterrupt:
        exit() #add this in outer layer if you run into trouble: except SystemExit: exit()
    except:
        print(bcolors.FAIL  + "------------------ERROR------------------" + bcolors.ENDC)
        print(bcolors.FAIL  + "Error handler getPriceFloat not comprehensive" + bcolors.ENDC)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_msg = str(traceback.format_exception(exc_type, exc_value, exc_traceback))
        traceback.print_exc()
        print(bcolors.FAIL  + "//////////////////ERROR//////////////////" + bcolors.ENDC)
        exit() #if error handler is not comprehensive





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

#init algorith 0.2 (use with USDT)
logDataObj = logDataErrVfctn()
while hasattr(logDataObj, 'error'):
    logDataObj = getPositionContracts('USDT', 'BTCUSDT')
positionContracts = logDataObj.positionContracts
if positionContracts != 0:
    print('Number of contracts currently equals ' + str(positionContracts))
    if input('Would you like to correct? (y/n) ') == 'y':
        if logDataObj.positionContracts > 0: #need to sell
            logDataObj = logDataErrVfctn()
            while hasattr(logDataObj, 'error'):
                logDataObj = getLastPrice()
            tryPrice = round(logDataObj.highestBidBaseFEX*0.98*2)/2
            logDataObj = verifyOrderUSDT(positionContracts, "SELL", tryPrice)
        else: #need to buy
            # logDataObj = logDataErrVfctn()
            # while hasattr(logDataObj, 'error'):
            #     logDataObj = getLastPrice()
            # buyPrice = round(logDataObj.highestBidBaseFEX*1.02*2)/2
            # logDataObj = verifyOrderUSDT(abs(positionContracts), "BUY", buyPrice)
            print("Can't correct. Change risk limit to cross and correct manually")
            exit()
        print('Corrected. Please run again')
        exit()
    exit()
#now contracts==0

sumChangeAct = 0.0 #sum change actual
print("Cumulative gain/loss:     " + bcolors.OKGREEN + str(sumChangeAct)[:5] + '%' + bcolors.ENDC)
logDataObj = logDataErrVfctn()
while hasattr(logDataObj, 'error'):
    logDataObj = getCashBalances('USDT')
print(bcolors.OKBLUE  + "Starting cash balance: $" + str(logDataObj.cash_balance) + bcolors.ENDC)





#main loop
while True:

    try:



        #loop algorith 0.2 (use with USDT)
        buyTrigger = False
        while buyTrigger==False:
            #conditions if which it becomes desirable to buy, set buyTrigger
            logDataObj = logDataErrVfctn()
            while hasattr(logDataObj, 'error'):
                logDataObj = getLastPrice()
            askOverBid = logDataObj.lowestAskBaseFEX/logDataObj.highestBidBaseFEX
            #veryify that there's no huge discrepency between ask and bid
            #at $7000, .035% more is 7002.45
            if askOverBid < 100.035/100:
                buyTrigger = True
        #exeute the buy-------------------------------------------------------------
        logDataObj = logDataErrVfctn()
        while hasattr(logDataObj, 'error'):
            logDataObj = getLastPrice()
        tryPrice = round(logDataObj.highestBidBaseFEX*1.02*2)/2
        #ORDER STATUS
        orderStatusFilled = False
        while orderStatusFilled==False:
            logDataObj = verifyOrderUSDT(C_TO_TRD, "BUY", tryPrice)
            logDataObj = waitUntilOrderFill(logDataObj.orderID)
            if logDataObj.orderStatus=='REJECTED':
                pass
            else:
                orderStatusFilled = True
        excPrice = logDataObj.excPrice
        if not excPrice==None:
            buyPrice = excPrice
        else:
            print('buy price was None, estimating')
            logDataObj = logDataErrVfctn()
            while hasattr(logDataObj, 'error'):
                logDataObj = getLastPrice()
            buyPrice = logDataObj.highestBidBaseFEX
        print(bcolors.OKBLUE  + "Buy  order executed at $" + str(buyPrice) + bcolors.ENDC)
        #get meta
        logDataObj = logDataErrVfctn()
        while hasattr(logDataObj, 'error'):
            logDataObj = getLastPrice()
        bidDuringBuy = logDataObj.highestBidBaseFEX
        #now we have bought it at price buyPrice and gotten bidDuringBuy, no errors



        sellTrigger = False
        while sellTrigger==False:
            #conditions if which it becomes desirable to sell, set sellTrigger
            logDataObj = logDataErrVfctn()
            while hasattr(logDataObj, 'error'):
                logDataObj = getLastPrice()
            bidOverBuy = logDataObj.highestBidBaseFEX/bidDuringBuy
            if bidOverBuy > 100.70/100:
                print(bcolors.OKBLUE  + '+0.7% expected' + bcolors.ENDC)
                sellTrigger = True
            elif bidOverBuy < 99.80/100:
                print(bcolors.OKBLUE  + '-0.2% expected' + bcolors.ENDC)
                sellTrigger = True
        #execute the sell-----------------------------------------------------------
        tryPrice = round(logDataObj.highestBidBaseFEX*0.98*2)/2
        #ORDER STATUS
        orderStatusFilled = False
        while orderStatusFilled==False:
            logDataObj = verifyOrderUSDT(C_TO_TRD, "SELL", tryPrice)
            logDataObj = waitUntilOrderFill(logDataObj.orderID)
            if logDataObj.orderStatus=='REJECTED':
                pass
            else:
                orderStatusFilled = True
        excPrice = logDataObj.excPrice
        if not excPrice==None:
            sellPrice = excPrice
        else:
            print('sell price was None, estimating')
            logDataObj = logDataErrVfctn()
            while hasattr(logDataObj, 'error'):
                logDataObj = getLastPrice()
            sellPrice = logDataObj.highestBidBaseFEX
        print(bcolors.OKBLUE  + "Sell order executed at $" + str(sellPrice) + bcolors.ENDC)
        #now we have sold it at price sellPrice, no errors


        #analyze results
        logDataObj = logDataErrVfctn()
        while hasattr(logDataObj, 'error'):
            logDataObj = getCashBalances('USDT')
        print(bcolors.OKBLUE  + "Cash balance: $" + str(logDataObj.cash_balance) + bcolors.ENDC)

        logDataObj = logData()
        logDataObj.timestamp = time.time()
        logDataObj.request_type = "sell_trigger"
        lastOverBuy = sellPrice/buyPrice*100-100
        logDataObj.sell_over_buy_ratio = str(lastOverBuy) + '%'
        sumChangeAct += lastOverBuy-0.08
        logDataObj.cumulative_change_actual = str(sumChangeAct) + '%'
        if lastOverBuy > 0:
            print("Sell price / buy price:   " + bcolors.OKGREEN + str(lastOverBuy)[:5] + '%' + bcolors.ENDC)
            logDataObj.trigger = "greater"
        else:
            print("Sell price / buy price:   " + bcolors.FAIL + str(lastOverBuy)[:5] + '%' + bcolors.ENDC)
            logDataObj.trigger = "lesser"


        print("Cumulative gain/loss:     " + str(sumChangeAct)[:5] + '%')
        upLogs(logDataObj)



        #rinse and repeat
        sleep(60)









        # #run test
        #
        # #check specific order
        # logDataObj = checkOrder('5c60286f-96b8-4e29-0005-8887213b34b3') #example: '5c55eeea-959a-4bcd-0005-fcbf01ba8a44'
        # #gives logDataObj.filled, logDataObj.excPrice (execution price)
        #
        #
        # #print(logDataObj.server_response)
        # #print(bcolors.OKBLUE + str(json.loads(logDataObj.serverResponseJSON.text)['filled']) + bcolors.ENDC)
        # print(logDataObj.status)
        # exit()

    #outer error handling:
    except KeyboardInterrupt:
        exit()
    except SystemExit:
        # print(bcolors.WARNING  + " Reached outer 'except SystemExit:'")
        exit()
    except:
        try:
            logDataObj
        except:
            logDataObj = logData()
        try:
            logDataObj.timestamp
        except:
            logDataObj.timestamp = time.time()
        print(bcolors.FAIL  + "------------------ERROR(outer layer)------------------" + bcolors.ENDC)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logDataObj.error_msg = str(traceback.format_exception(exc_type, exc_value, exc_traceback))
        traceback.print_exc()
        print(bcolors.FAIL  + "//////////////////ERROR(outer layer)//////////////////" + bcolors.ENDC)
        logDataObj.error = True
        logDataObj.error_outer_layer = True
        upLogs(logDataObj)
        exit()




















#end
