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
