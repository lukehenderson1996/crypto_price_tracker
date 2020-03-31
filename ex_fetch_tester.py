#PrimeBit
#not added yet, 2.5-4s for call, might need coroutines
import requests, json
import time
from time import sleep, localtime, strftime

URL = "https://app.primebit.com/api/v1/trading/market_data/ticker/live"
# URL = "https://app.primebit.com/api/v1/trading/market_data/summary/live" #this one has the same info for some reason?

while True:
    # #test get
    # response = requests.request("GET", URL)
    # print(response.text)
    # sleep(20) #1 or less is right number


    #test keying
    currTime = time.time()
    r = requests.get(URL)
    priceFloat = float(json.loads(r.text)['BTCUSD']['last_price'])
    print(str(priceFloat) + "      " + str(time.time()-currTime))
    # sleep(0)















# #template
# import requests, json
# import time
# from time import sleep
#
# URL = ""
#
# while True:
#     #test get
#     response = requests.request("GET", URL)
#     print(response.text)
#     sleep(4) # or less is right number
#
#
#     # #test keying
#     # currTime = time.time()
#     # r = requests.get(URL)
#     # priceFloat = float(json.loads(r.text)[''])
#     # print(str(priceFloat) + "      " + str(time.time()-currTime))
#     # sleep(1)










# #Gemini
# import requests, json
# import time
# from time import sleep
#
# URL = "https://api.gemini.com/v1/pubticker/btcusd"
#
# while True:
#     # #test get
#     # response = requests.request("GET", URL)
#     # print(response.text)
#     # sleep(4) #1 or less is right number
#
#
#     #test keying
#     r = requests.get(URL)
#     priceFloat = float(json.loads(r.text)['last'])
#     print(priceFloat)
#     sleep(1)








# #bitbay
# import requests, json
# import time
# from time import sleep
#
# URL = "https://bitbay.net/API/Public/BTCUSD/ticker.json"
#
#
# while True:
#     # #test get
#     # response = requests.request("GET", URL)
#     # print(response.text)
#     # sleep(4) #1 or less is right number
#
#
#     #test keying
#     r = requests.get(URL)
#     priceFloat = float(json.loads(r.text)['last'])
#     print(priceFloat)
#     sleep(1)






# #LUNO
# import requests, json
# import time
# from time import sleep
#
# URL = "https://api.mybitx.com/api/1/ticker?pair=XBTEUR"
#
#
# while True:
#     # #test get
#     # response = requests.request("GET", URL)
#     # print(response.text)
#     # sleep(4) #1 or less is right number
#
#
#     #test keying
#     r = requests.get(URL)
#     priceFloat = float(json.loads(r.text)['last_trade'])
#     print(priceFloat)
#     sleep(1)











#
#
# #BaseFEX
# import requests, json
# import time
# from time import sleep
#
# URL = "https://api.basefex.com/depth@BTCUSD/snapshot"
#
#
# while True:
#     # response = requests.request("GET", URL)
#     # print(response.text)
#     # sleep(4) #1 or less is right number
#
#
#     #test keying
#     r = requests.get(URL)
#     priceFloat = float(json.loads(r.text)['lastPrice'])
#     print(priceFloat)
#     sleep(0)
#
#
# #
# # https://api.basefex.com/instruments/prices
# # 'lastPrice'
# # {
# # "to":189858295,"bestPrices":
# # {"ask":6548,"bid":6545.5},
# # "lastPrice":6547.0,"bids":
# # {"6531.5":12378,"5670.5":100,"6540.5":3704,"5470.5":100,"6544":5109,"6538.5":4012,"3300":3300,"6543":3419,"6537":10542,"6545":8362,"6534.5":9725,"6534":13424,"6541.5":7113,"6535.5":8974,"4000":1000,"6542.5":10014,"4160":300,"4554":200,"6540":4014,"6538":9726,"6544.5":4714,"6545.5":3702,"6532.5":11422},
# # "asks":{"6559":14887,"6550.5":5230,"6560.5":16135,"6548.5":3791,"6551.5":6143,"6563":16126,"6553.5":7819,"9999":175,"6557":10786,"6554":8474,"6555":11693,"16666":150,"6548":5664,"6549":9183,"6552.5":9183,"14545":100,"6558":11690,"6549.5":4453,"6561.5":14880,"6551":5668,"6552":11694,"6550":9953,"6556":12674},
# # "from":0
# # }





s















# #coinmetro
# import requests, json
# import time
# from time import sleep
#
# url = "https://exchange.coinmetro.com/open/prices/BTCEUR"
#
# EUR_USD = 6238.80/6019.56
#
# while True:
#     response = requests.request("GET", url)
#     # print(response.text)
#
#     #this block demonstrates that the data can be hours old
#     print(time.time())
#     print(json.loads(response.text)['latestPrices'][0]['timestamp'])
#     print("")
#
#     sleep(4) #1 or less is right number
#
#
#     # #test keying
#     # r = requests.get(url)
#     # priceFloat = float(json.loads(r.text)['latestPrices'][0]['price'])*EUR_USD
#     # print(priceFloat)
#     # sleep(20)
#
#
#
#
# #use ['latestPrices'][0]['price']
#
#
#
# #
# # {"latestPrices":[{"pair":"XCMEUR","price":0.019489,"qty":135158.592,"timestamp":1585357560229,"seqNum":146903176,"ask":0.019597,"bid":0.019597},{"pair":"BTCEUR","price":6019.56,"qty":1.10088389,"timestamp":1585357560184,"seqNum":146903070,"ask":5628.77,"bid":5628.77},{"pair":"XCMBTC","price":0.00000316,"qty":500,"timestamp":1585088966371,"seqNum":146558493,"ask":0.00000348,"bid":0.00000348},{"pair":"LTCEUR","price":34.6694,"qty":57.541264,"timestamp":1585357560191,"seqNum":146903144,"ask":33.7120,"bid":33.7120},{"pair":"LTCBTC","price":0.006016,"qty":48.276368,"timestamp":1585357560497,"seqNum":146903364,"ask":0.005989,"bid":0.005989},{"pair":"ETHEUR","price":123.3513,"qty":16.787868,"timestamp":1585357560185,"seqNum":146903096,"ask":116.2745,"bid":116.2745},{"pair":"XCMETH","price":0.0001547,"qty":6464.428703418539,"timestamp":1584538998390,"seqNum":0,"ask":0.0001685,"bid":0.0001685},{"pair":"ETHBTC","price":0.020519,"qty":16.199956,"timestamp":1585340355897,"seqNum":146880499,"ask":0.020657,"bid":0.020657},{"pair":"BCHEUR","price":196.607,"qty":11.614441,"timestamp":1585357560192,"seqNum":146903170,"ask":188.820,"bid":188.820},{"pair":"XRPEUR","price":0.15876,"qty":102682.297,"timestamp":1585357560276,"seqNum":146903204,"ask":0.154315,"bid":0.154315},{"pair":"XRPBTC","price":0.00002726,"qty":69686.162,"timestamp":1585357560498,"seqNum":146903376,"ask":0.00002742,"bid":0.00002742},{"pair":"XLMEUR","price":0.037221,"qty":12063.878,"timestamp":1585357560277,"seqNum":146903230,"ask":0.036127,"bid":0.036127},{"pair":"OMGEUR","price":0.46291,"qty":1351.5859,"timestamp":1585357560278,"seqNum":146903254,"ask":0.44259,"bid":0.44259},{"pair":"LINKEUR","price":2.04959,"qty":1344.9511,"timestamp":1585357560279,"seqNum":146903276,"ask":1.88986,"bid":1.88986},{"pair":"ENJEUR","price":0.077869,"qty":1270.3978,"timestamp":1585357560280,"seqNum":146903308,"ask":0.071710,"bid":0.071710},{"pair":"BATEUR","price":0.132614,"qty":839.3934,"timestamp":1585357560342,"seqNum":146903316,"ask":0.124002,"bid":0.124002},{"pair":"QNTEUR","price":3.025,"qty":823.4805,"timestamp":1585357560623,"seqNum":146903472,"ask":2.99242,"bid":2.99242},{"pair":"LIBRAEUR","price":0.903,"qty":3791.606,"timestamp":1585340355845,"seqNum":146880475,"ask":0.8973,"bid":0.8973},{"pair":"PRQEUR","price":0.025,"qty":40,"timestamp":1584538998396,"seqNum":0,"ask":0.025000,"bid":0.025000},{"pair":"2A8Bf455253545D7Abd9F0Bbad3C13B9IGN","price":0.25,"qty":4,"timestamp":1585232246911,"seqNum":0,"ask":0,"bid":0},{"pair":"583F1F7FD57C4B1D9E31F298592E66A9IGN","price":0.25,"qty":4,"timestamp":1584538998391,"seqNum":0,"ask":0,"bid":0},{"pair":"5De94B2B19C84Ace8789446Fcddad69DIGN","price":0.25,"qty":4,"timestamp":1585302330428,"seqNum":0,"ask":0,"bid":0},{"pair":"741610569Fbe4524931409028D319B76IGN","price":0.25,"qty":4,"timestamp":1585241786564,"seqNum":0,"ask":0,"bid":0},{"pair":"B204F81DC26D49E59Cd9418E088587B7IGN","price":0.25,"qty":4,"timestamp":1585298369264,"seqNum":0,"ask":0,"bid":0},{"pair":"B2Fb11E497B54DdbB413B6Ed9B7B3B59IGN","price":0.25,"qty":4,"timestamp":1584538998392,"seqNum":0,"ask":0,"bid":0},{"pair":"E0CebedaC1724F48AefdEa8579D89212IGN","price":0.25,"qty":4,"timestamp":1584971419516,"seqNum":0,"ask":0,"bid":0},{"pair":"RealBondIGN","price":0.25,"qty":4,"timestamp":1584538998392,"seqNum":0,"ask":0,"bid":0},{"pair":"SpecialAssetIGN","price":0.25,"qty":4,"timestamp":1584949341744,"seqNum":0,"ask":0,"bid":0},{"pair":"9970218171Dc42B383A0110702E3C240IGN","price":0.25,"qty":4,"timestamp":1585308692030,"seqNum":0,"ask":0,"bid":0},{"pair":"D72228A441014305B4E979D6D3E715C4IGN","price":0.25,"qty":4,"timestamp":1585312229929,"seqNum":0,"ask":0,"bid":0},{"pair":"6Ea55Bab58B74CaeA1C747C5Fbe67897IGN","price":0.25,"qty":4,"timestamp":1585322553904,"seqNum":0,"ask":0,"bid":0},{"pair":"4C747Fbe8C2A414BAbb033892A04963AIGN","price":0.25,"qty":4,"timestamp":1585323274461,"seqNum":0,"ask":0,"bid":0},{"pair":"11F7987F9D324C64A48ADb4De6A21E81IGN","price":0.25,"qty":4,"timestamp":1585326932557,"seqNum":0,"ask":0,"bid":0},{"pair":"4C1A5A784Cbd4B83A2C5Cfc4920223E5IGN","price":0.25,"qty":4,"timestamp":1585327895271,"seqNum":0,"ask":0,"bid":0}],"24hInfo":[{"delta":0.17915221707731854,"h":0.020368,"l":0.015295,"v":27795901.557025254,"pair":"XCMEUR"},{"delta":0.25064795453244004,"h":6256.36,"l":4568.83,"v":320.0053986511269,"pair":"BTCEUR"},{"delta":-0.15281501340482573,"h":0.00000424,"l":0.00000268,"v":176496699.92314622,"pair":"XCMBTC"},{"delta":0.13252429563086987,"h":37.7132,"l":29.5705,"v":14555.120849002815,"pair":"LTCEUR"},{"delta":-0.023852020120071482,"h":0.006722,"l":0.005881,"v":29070.711302305444,"pair":"LTCBTC"},{"delta":0.14423863202139842,"h":131.8276,"l":100.425,"v":6110.7244750026275,"pair":"ETHEUR"},{"delta":-0.23377909856364543,"h":0.0002093,"l":0.0001537,"v":6900199.067018086,"pair":"XCMETH"},{"delta":-0.14379303150427714,"h":0.023965,"l":0.020295,"v":10668.869543412018,"pair":"ETHBTC"},{"delta":0.20363035293397402,"h":211.229,"l":155.505,"v":5292.902873002818,"pair":"BCHEUR"},{"delta":0.1657164013328396,"h":0.162073,"l":0.1287,"v":25306952.83877905,"pair":"XRPEUR"},{"delta":-0.035044247787610616,"h":0.00002864,"l":0.00002421,"v":34253100.06797071,"pair":"XRPBTC"},{"delta":-0.04129854651915943,"h":0.038704,"l":0.031441,"v":6069579.513706474,"pair":"XLMEUR"},{"delta":-0.24299788171211456,"h":0.59482,"l":0.39294,"v":588655.7740539153,"pair":"OMGEUR"},{"delta":-0.30949459742070407,"h":2.869,"l":1.61775,"v":618103.7335000001,"pair":"LINKEUR"},{"delta":0.16512329144536442,"h":0.081776,"l":0.043024,"v":668963.0054190229,"pair":"ENJEUR"},{"delta":-0.13790739869632407,"h":0.14881,"l":0.102688,"v":616500.963737902,"pair":"BATEUR"},{"delta":0.4104536765048725,"h":3.025,"l":1.6409,"v":649695.9023999997,"pair":"QNTEUR"},{"delta":-0.00022256843979517882,"h":0.9353,"l":0.874,"v":1109772.0851900002,"pair":"LIBRAEUR"},{"delta":0,"h":0.025,"l":0.025,"v":55080,"pair":"PRQEUR"},{"delta":0,"h":0.25,"l":0.25,"v":4,"pair":"2A8Bf455253545D7Abd9F0Bbad3C13B9IGN"},{"delta":0,"h":0.25,"l":0.25,"v":256,"pair":"583F1F7FD57C4B1D9E31F298592E66A9IGN"},{"delta":0,"h":0.25,"l":0.25,"v":4,"pair":"5De94B2B19C84Ace8789446Fcddad69DIGN"},{"delta":0,"h":0.25,"l":0.25,"v":4,"pair":"741610569Fbe4524931409028D319B76IGN"},{"delta":0,"h":0.25,"l":0.25,"v":4,"pair":"B204F81DC26D49E59Cd9418E088587B7IGN"},{"delta":0,"h":0.25,"l":0.25,"v":256,"pair":"B2Fb11E497B54DdbB413B6Ed9B7B3B59IGN"},{"delta":0,"h":0.25,"l":0.25,"v":4,"pair":"E0CebedaC1724F48AefdEa8579D89212IGN"},{"delta":0,"h":0.25,"l":0.25,"v":5488,"pair":"RealBondIGN"},{"delta":0,"h":0.25,"l":0.25,"v":4,"pair":"SpecialAssetIGN"},{"delta":0,"h":0.25,"l":0.25,"v":4,"pair":"9970218171Dc42B383A0110702E3C240IGN"},{"delta":0,"h":0.25,"l":0.25,"v":4,"pair":"D72228A441014305B4E979D6D3E715C4IGN"},{"delta":0,"h":0.25,"l":0.25,"v":4,"pair":"6Ea55Bab58B74CaeA1C747C5Fbe67897IGN"},{"delta":0,"h":0.25,"l":0.25,"v":4,"pair":"4C747Fbe8C2A414BAbb033892A04963AIGN"},{"delta":0,"h":0.25,"l":0.25,"v":4,"pair":"11F7987F9D324C64A48ADb4De6A21E81IGN"},{"delta":0,"h":0.25,"l":0.25,"v":4,"pair":"4C1A5A784Cbd4B83A2C5Cfc4920223E5IGN"}]}






























# #currency rate api
# import requests
#
# url = "https://api.exchangeratesapi.io/latest?symbols=USD,GBP HTTP/1.1"
#
# response = requests.request("GET", url)
#
# print(response.text)
#
# https://exchangeratesapi.io/
#
# https://medium.com/@MicroPyramid/free-foreign-currency-exchange-rates-api-2a93195649fb


























# #bitbay
# #DOESNT WORK
#
# import requests
#
# url = "https://bitbay.net/API/Public/BTCUSD/trades.json"
#
# response = requests.request("GET", url)
#
# print(response.text)





# #Bitfinex
#
# import requests
# import time
# from time import sleep
#
# url = "https://api.bitfinex.com/v1/pubticker/btcusd"
#
# while True:
#     sleep(4) # 4 is the right delay, actually we're trying 6 now
#     response = requests.request("GET", url)
#     print(response.text)





















# #Bitflyer
# import requests
# import time
# from time import sleep
#
# url = "https://api.bitflyer.com/v1/ticker?product_code=BTC_USD"
#
# while True:
#     sleep(0) #1 or less is right number
#     response = requests.request("GET", url)
#     print(response.text)
























# #bitso
# import requests, json
# import time
# from time import sleep
#
# url = "https://api.bitso.com/v3/ticker?book=btc_mxn"
#
# MXN_USD = 1/23.5818
#
# while True:
#     sleep(0) #1 or less is right number
#     response = requests.request("GET", url)
#     print(response.text)
#
#     # #test keying
#     # r = requests.get(url)
#     # priceFloat = float(json.loads(r.text)['payload']['last'])*MXN_USD
#     # print(priceFloat)
#     # sleep(20)
#
#
#
#
# #use last, is in mxn mexican pesos






































# #bitstamp
# import requests
# import time
# from time import sleep
#
# url = "https://www.bitstamp.net/api/ticker/"
#
# while True:
#     sleep(0) #1 or less is right number
#     response = requests.request("GET", url)
#     print(response.text)
#
#
#
# #use lastPrice













































































# #itbit
# import requests
# import time
# from time import sleep
#
# url = "https://api.itbit.com/v1/markets/XBTUSD/ticker"
#
# while True:
#     sleep(0) #1 or less is right number
#     response = requests.request("GET", url)
#     print(response.text)
#
#
#
# #use lastPrice



















# #korbit
# import requests
#
# url = "https://api.korbit.co.kr/v1/ticker"
#
# response = requests.request("GET", url)
#
# print(response.text)






















# #Kraken
# import requests
# import time
# from time import sleep
#
# url = "https://api.kraken.com/0/public/Ticker?pair=XBTUSD"
#
# while True:
#     sleep(0) #1 or less is right number
#     response = requests.request("GET", url)
#     print(response.text)
#
#
#
# #a = ask array(<price>, <whole lot volume>, <lot volume>),
# #    b = bid array(<price>, <whole lot volume>, <lot volume>),
# #    c = last trade closed array(<price>, <lot volume>),
# #    v = volume array(<today>, <last 24 hours>),
# #    p = volume weighted average price array(<today>, <last 24 hours>),
# #    t = number of trades array(<today>, <last 24 hours>),
# #    l = low array(<today>, <last 24 hours>),
# #    h = high array(<today>, <last 24 hours>),
# #    o = today's opening price
