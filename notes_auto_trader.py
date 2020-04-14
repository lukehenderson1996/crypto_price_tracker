# todo:make logV parser with input('what file to parse?') and input('what tag to parse?') and input('what value to parse?'), but save the whole entry if it includes that tag/value
#      and then make a version where the output doesnt include that specific tag/value?




#error handling convention:
try:
    pass
except KeyboardInterrupt:
    exit() #add this in outer layer if you run into trouble: except SystemExit: exit()
except:
    print(bcolors.FAIL  + "------------------ERROR------------------" + bcolors.ENDC)
    print(bcolors.FAIL  + "Error handler functionName not comprehensive" + bcolors.ENDC)
    exc_type, exc_value, exc_traceback = sys.exc_info()
    logDataObj.error_msg = str(traceback.format_exception(exc_type, exc_value, exc_traceback))
    traceback.print_exc()
    print(bcolors.FAIL  + "//////////////////ERROR//////////////////" + bcolors.ENDC)
    logDataObj.error = True
    logDataObj.error_functionName = True
    upLogs(logDataObj) #which layer are you in?
    exit() #if error handler is not comprehensive
    return logDataObj





#algorithm prints
print(bcolors.OKBLUE  + side + " order executed" + bcolors.ENDC)
print(bcolors.OKBLUE  + "Cash balance: " + str(logDataObj.cash_balance) + bcolors.ENDC)
print(bcolors.OKBLUE  + "Number of contracts: " + str(logDataObj.positionContracts) + bcolors.ENDC)


#logDataObj handling
logDataObj = logData()
logDataObj.request_type = "request_type"
logDataObj.timestamp = time.time()
upLogs(logDataObj)
return logDataObj





#examples:

#function with error verification
logDataObj = logDataErrVfctn()
while hasattr(logDataObj, 'error'):
    pass #function

#wait until order get filled
logDataObj = waitUntilOrderFill(id) #example: '5c55eeea-959a-4bcd-0005-fcbf01ba8a44'
#gives logDataObj.excPrice (price or None)

#makes trigger order
def verifyTriggerOrderUSDT():
#gives logDataObj.orderID

#makes limit order
def verifyOrderUSDT(size, side, price): #C_TO_TRD, "BUY", 1000
#gives logDataObj.orderID

#get last price
logDataObj = getLastPrice()
#gives logDataObj.lastBaseFEX and logDataObj.highestBidBaseFEX

#get cash balance
logDataObj = getCashBalances('BTC') #'BTC', 'USDT'
#gives logDataObj.cash_balance

#get num of contracts
logDataObj = getPositionContracts('USDT', 'BTCUSDT') #'BTC', 'BTCUSD' or 'USDT', 'BTCUSDT'
#gives logDataObj.positionContracts

#place order
logDataObj = placeOrderBTC(size, type, side) #example: 10, "MARKET", "BUY"
#gives nothing
logDataObj = placeOrderUSDT(size, type, side, price, trigPrice) #example: 1, "MARKET", "SELL", None, None      or      1, "LIMIT", "BUY", 1000, None
#produces logDataObj.orderID

#verifyContracts
verifyContracts(num)
#gives nothing

#get active order list
logDataObj = getActiveOrderList(symbol) #symbol: BTCUSD, BTCUSDT
#gives logDataObj.activeOrderIDs (list of ID's)

#check specific order
logDataObj = checkOrder(id) #example: '5c55eeea-959a-4bcd-0005-fcbf01ba8a44'
#gives logDataObj.filled, logDataObj.excPrice (execution price)






#extended notes:

#place market order
placeOrderBTC(size, type, side) #example: 10, "MARKET", "BUY"
    data = {
        "size": 5,
        "symbol": "BTCUSD",
        "type": "MARKET",
        "side": "BUY"
        }










#comprehensive test without placing orders 04 13 5PM
logDataObj = getCashBalances('BTC') #'BTC', 'USDT'
print(logDataObj.cash_balance)
logDataObj = getCashBalances('USDT') #'BTC', 'USDT'
print(logDataObj.cash_balance)
logDataObj = getLastPrice()
print(logDataObj.lastBaseFEX)
print(logDataObj.highestBidBaseFEX)
sleep(1)
logDataObj = getPositionContracts('BTC', 'BTCUSD') #'BTC', 'BTCUSD' or 'USDT', 'BTCUSDT'
print(logDataObj.positionContracts)
logDataObj = getPositionContracts('USDT', 'BTCUSDT') #'BTC', 'BTCUSD' or 'USDT', 'BTCUSDT'
print(logDataObj.positionContracts)
logDataObj = getActiveOrderList('BTCUSD') #symbol: BTCUSD, BTCUSDT
sleep(1)
logDataObj = getActiveOrderList('BTCUSDT') #symbol: BTCUSD, BTCUSDT
logDataObj = checkOrder('5c55eeea-959a-4bcd-0005-fcbf01ba8a44') #example: '5c55eeea-959a-4bcd-0005-fcbf01ba8a44'
print(logDataObj.filled)
print(logDataObj.excPrice)
exit()


























# #static debugging example
# apiKey = '5afd4095-f1fb-41d0-0005-1a0048ffe468'            # id of api key example from baseFEX
# apiSecret = 'OJJFq6qugIyvLBOyvg8WBPriSs0Dfw7Mi3QjLYin8is=' # api secret example from baseFEX
# http_method = 'GET'
# path = '/accounts'
# url = 'https://api.basefex.com' + path
# timestamp = 1586032143
# expires  = 1586032148
# data = ''
# Computed_HMAC_sig_correct = "5335b2cca857776937b857effc9523fdb1d37336ea93c935971436574f085746"

# #GET with current time
# http_method = 'GET'
# path = '/accounts'
# # path = '/orders?symbol=BTCUSD' #not sure what this is for
# url = 'https://api.basefex.com' + path
# timestamp = time.time()
# expires = int(round(timestamp) + 5)
# data = '' # empty request body
# # parsedJSON = json.loads(response.text)[0]['positions'][4] #BTC position

# #POST
# http_method = 'POST'
# path = '/orders'
# url = 'https://api.basefex.com' + path
# timestamp = time.time()
# expires = int(round(timestamp) + 5)
# data = {
#     "size": 5,
#     "symbol": "BTCUSD",
#     "type": "MARKET",
#     "side": "BUY"
#     }
# #optional options:
# "price": 3750.5,
# "reduceOnly": False,
# "conditional": {
#     "type": "REACH",
#     "price": 6882.0,
#     "priceType": "MARKET_PRICE"
#}
#---------------ORDER PARAMS--------------------------------------------------------------------------------------------------------------------------
# size	REQUIRED           	number	Contract amount
# symbol	REQUIRED           	string	Contract types, includes BTCUSD, ETHXBT, XRPXBT, BCHXBT, LTCXBT, EOSXBT, ADAXBT, TRXXBT, BNBXBT, HTXBT, OKBXBT, GTXBT, ATOMXBT, BTCUSDT
# type	REQUIRED           	string	Order type, includes LIMIT, MARKET, IOC, FOK, POST_ONLY
# side	REQUIRED           	string	BUY or SELL
# price		                number	Order price
# reduceOnly		            boolean	A Reduce Only Order will only reduce your position, not increase it. If this order would increase your position, it is amended down or canceled such that it does not.
# conditional	            	object	currently conditional type only have one option REACH, price types includes MARK_PRICE,INDEX_PRICE,MARKET_PRICE
