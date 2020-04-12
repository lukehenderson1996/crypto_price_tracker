#init algorith 0.1
sumChange = 0.0
print("Cumulative gain/loss: " + bcolors.OKGREEN + str(sumChange)[:5] + '%' + bcolors.ENDC)
verifyContracts(0)
#now contracts==0



#loop algorith 0.1
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
