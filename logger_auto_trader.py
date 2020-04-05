#Luke Henderson
#Version info on ticker.py
#Solely for BaseFEX use
import time
from time import sleep, localtime, strftime
import sys
import os
from parse import * #pip install parse (or pip3 install parse)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



#init loggers
def initLogs():
    if not os.path.exists('auto_logs/log_auto_trader.xml'): #file does not yet exist
        createLog('auto_logs/log_auto_trader.xml')
    if not os.path.exists('auto_logs/logV_auto_trader.xml'): #file does not yet exist
        createLog('auto_logs/logV_auto_trader.xml')
def createLog(path):
    f=open(path, "w")
    f.write('<?xml version="1.0" encoding="UTF-8"?>\r\n')
    f.close()

#update logger
#all strings except: timestamp (int), sequence(int)
def upLogs(timestamp, request_type, string, signature, server_response_simplified, server_response):
    verboseLog=open('auto_logs/logV_auto_trader.xml', "a+")
    apToFile(verboseLog, '<' + str(timestamp) + '>')

    apToFile(verboseLog, '  <time>' + strftime("%Y-%m-%d %H:%M:%S", localtime(timestamp)) + '</time>')
    apToFile(verboseLog, '  <request_type>' + request_type + '</request_type>')
    apToFile(verboseLog, '  <string>' + string + '</string>')
    apToFile(verboseLog, '  <signature>' + signature + '</signature>')
    apToFile(verboseLog, '  <server_response_simplified>' + server_response_simplified + '</server_response_simplified>')
    apToFile(verboseLog, '  <server_response>' + server_response + '</server_response>')

    apToFile(verboseLog, '</' + str(timestamp) + '>')
    apToFile(verboseLog, '\n\n')
    verboseLog.close()



    simpLog=open('auto_logs/log_auto_trader.xml', "a+")
    apToFile(simpLog, '<' + str(timestamp) + '>')

    apToFile(simpLog, '  <time>' + strftime("%Y-%m-%d %H:%M:%S", localtime(timestamp)) + '</time>')
    apToFile(simpLog, '  <request_type>' + request_type + '</request_type>')
    apToFile(simpLog, '  <string>' + string + '</string>')
    apToFile(simpLog, '  <signature>' + signature + '</signature>')
    apToFile(simpLog, '  <server_response_simplified>' + server_response_simplified + '</server_response_simplified>')

    apToFile(simpLog, '</' + str(timestamp) + '>')
    apToFile(simpLog, '\n\n')
    simpLog.close()


# Verbose format:
# <entry_timestamp>
#   <time>2020-03-31 00:01:52</time>
#   <error>True</error>
#   <error_msg>err_msg_here</error_msg>
#   <request_type>priceFetch/contractFetch/buy/sell</request_type>
#   <string>GET/accounts1586059192</string>
#   <signature>004cae60b45dd87f068142114c44262cc672718b128a555db01e0b34a99aa45e</signature>
#   <server_response_simplified>price/contracts/order details/etc</server_response_simplified>
#   <server_response>long response</server_response>
# </entry_timestamp>

def apToFile(file,writeString):
    file.write(writeString + "\r\n")
