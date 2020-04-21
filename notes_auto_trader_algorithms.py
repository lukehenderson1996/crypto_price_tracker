#init algorithm 0.1
sumChange = 0.0
print("Cumulative gain/loss: " + bcolors.OKGREEN + str(sumChange)[:5] + '%' + bcolors.ENDC)
verifyContracts(0)
#now contracts==0



#loop algorithm 0.1
sleep(3)
logDataObj = getLastPrice()
buyPrice = logDataObj.lastBaseFEX
logDataObj = placeOrder(10, "MARKET", "BUY")
sleep(3)
verifyContracts(10)

trigger = False
while trigger==False:
    sleep(2)
    logDataObj = getLastPrice()
    lastPrice = logDataObj.lastBaseFEX
    if lastPrice/buyPrice > 100.70/100:
        trigger = True
        print("lastPrice/buyPrice:   " + bcolors.OKGREEN + str(lastPrice/buyPrice*100-100)[:5] + '%' + bcolors.ENDC)
        logDataObj = logData()
        logDataObj.timestamp = time.time()
        logDataObj.request_type = "nonrequest, trigger"
        logDataObj.trigger = "greater"
        logDataObj.last_over_buy_ratio = str(lastPrice/buyPrice*100-100) + '%'
        sumChange += lastPrice/buyPrice*100-100-0.08
        print("Cumulative gain/loss: " + str(sumChange)[:5] + '%')
        upLogs(logDataObj)
    if lastPrice/buyPrice < 99.80/100:
        trigger = True
        print("lastPrice/buyPrice:   " + bcolors.FAIL + str(lastPrice/buyPrice*100-100)[:5] + '%' + bcolors.ENDC)
        logDataObj = logData()
        logDataObj.timestamp = time.time()
        logDataObj.request_type = "nonrequest, trigger"
        logDataObj.trigger = "lesser"
        logDataObj.last_over_buy_ratio = str(lastPrice/buyPrice*100-100) + '%'
        sumChange += lastPrice/buyPrice*100-100-0.08
        print("Cumulative gain/loss: " + str(sumChange)[:5] + '%')
        upLogs(logDataObj)


logDataObj = placeOrder(10, "MARKET", "SELL")
sleep(3)
verifyContracts(0)


sleep(60)






















#init algorithm 0.2 (use with USDT)
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






#loop algorithm 0.2 (use with USDT)
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






























#init algorithm 0.3 (Switched 0.2) (use with USDT)
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


#buy to start
#loop algorith 0.2 (use with USDT)
buyTrigger = False
while buyTrigger==False:
    #conditions in which it becomes desirable to buy, set buyTrigger
    logDataObj = logDataErrVfctn()
    while hasattr(logDataObj, 'error'):
        logDataObj = getLastPrice()
    askOverBid = logDataObj.lowestAskBaseFEX/logDataObj.highestBidBaseFEX
    #veryify that there's no huge discrepency between ask and bid
    #at $7000, .035% more is 7002.45
    if askOverBid < 100.035/100:
        buyTrigger = True
    else: #assuming it's always favorable to buy
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








#loop algorithm 0.3 (Switched 0.2) (use with USDT)
sellTrigger = False
while sellTrigger==False:
    #conditions in which it becomes desirable to sell, set sellTrigger
    logDataObj = logDataErrVfctn()
    while hasattr(logDataObj, 'error'):
        logDataObj = getLastPrice()
    askOverBid = logDataObj.lowestAskBaseFEX/logDataObj.highestBidBaseFEX
    #veryify that there's no huge discrepency between ask and bid
    #at $7000, .035% more is 7002.45
    if askOverBid < 100.035/100:
        sellTrigger = True


    #extra code to prevent bugs:
    logDataObj = logDataErrVfctn()
    while hasattr(logDataObj, 'error'):
        logDataObj = getLastPrice()
    highestBidBaseFEX = logDataObj.highestBidBaseFEX

#execute the sell-----------------------------------------------------------
tryPrice = round(highestBidBaseFEX*0.98*2)/2
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



buyTrigger = False
while buyTrigger==False:
    #conditions in which it becomes desirable to buy, set buyTrigger
    logDataObj = logDataErrVfctn()
    while hasattr(logDataObj, 'error'):
        logDataObj = getLastPrice()
    bidOverBuy = logDataObj.highestBidBaseFEX/bidDuringBuy
    if bidOverBuy > 100.70/100:
        print(bcolors.OKBLUE  + '+0.7% expected' + bcolors.ENDC)
        buyTrigger = True
    elif bidOverBuy < 99.80/100:
        print(bcolors.OKBLUE  + '-0.2% expected' + bcolors.ENDC)
        buyTrigger = True
    highestBidBaseFEX = logDataObj.highestBidBaseFEX



    #extra code to prevent bugs:
    logDataObj = logDataErrVfctn()
    while hasattr(logDataObj, 'error'):
        logDataObj = getLastPrice()
    askOverBid = logDataObj.lowestAskBaseFEX/logDataObj.highestBidBaseFEX


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
