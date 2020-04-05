#Luke Henderson
#Version info on auto_trader.py
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

class logData:
  pass
  #timestamp
  #request_type
  #string
  #signature
  #server_response_simplified
  #server_response



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
def upLogs(logDataObj): #timestamp, request_type, string, signature, server_response_simplified, server_response,

    #static XML creation
    # verboseLog=open('auto_logs/logV_auto_trader.xml', "a+")
    # apToFile(verboseLog, '<' + str(timestamp) + '>')
    #
    # apToFile(verboseLog, '  <time>' + strftime("%Y-%m-%d %H:%M:%S", localtime(timestamp)) + '</time>')
    # apToFile(verboseLog, '  <request_type>' + request_type + '</request_type>')
    # apToFile(verboseLog, '  <string>' + string + '</string>')
    # apToFile(verboseLog, '  <signature>' + signature + '</signature>')
    # apToFile(verboseLog, '  <server_response_simplified>' + server_response_simplified + '</server_response_simplified>')
    # apToFile(verboseLog, '  <server_response>' + server_response + '</server_response>')
    #
    # apToFile(verboseLog, '</' + str(timestamp) + '>')
    # apToFile(verboseLog, '\n\n')
    # verboseLog.close()



    #dynamic XML creation
    verboseLog=open('auto_logs/logV_auto_trader.xml', "a+")
    if logDataObj.__dict__:
        if 'timestamp' in logDataObj.__dict__.keys():
            #begin entry
            apToFile(verboseLog, '<' + str(logDataObj.__dict__['timestamp']) + '>')
            apToFile(verboseLog, '  <time>' + strftime("%Y-%m-%d %H:%M:%S", localtime(logDataObj.__dict__['timestamp'])) + '</time>')
            #populate inside of xml entry
            keysList = list(logDataObj.__dict__.keys())
            for i in range(len(keysList)):
                if not keysList[i]=='timestamp':
                    if not keysList[i]=='serverResponseJSON':
                        apToFile(verboseLog, '  <' + keysList[i] + '>' + str(logDataObj.__dict__[keysList[i]]) + '</' + keysList[i] + '>')
            #end entry
            apToFile(verboseLog, '</' + str(logDataObj.__dict__['timestamp']) + '>')
        else:
            apToFile(verboseLog, '<' + str(time.time()) + '>')
            apToFile(verboseLog, '  <time>' + strftime("%Y-%m-%d %H:%M:%S", localtime(time.time())) + '</time>')
            apToFile(verboseLog, '  <error>True<error>\r\n  <error_msg>logDataObj has no timestamp</error_msg>')
            apToFile(verboseLog, '</' + str(timestamp) + '>')
    else:
        apToFile(verboseLog, '<' + str(time.time()) + '>')
        apToFile(verboseLog, '  <time>' + strftime("%Y-%m-%d %H:%M:%S", localtime(time.time())) + '</time>')
        apToFile(verboseLog, '  <error>True<error>\r\n  <error_msg>logDataObj is empty</error_msg>')
        apToFile(verboseLog, '</' + str(timestamp) + '>')
    apToFile(verboseLog, '\n\n')
    verboseLog.close()




    #static XML creation
    # simpLog=open('auto_logs/log_auto_trader.xml', "a+")
    # apToFile(simpLog, '<' + str(timestamp) + '>')
    #
    # apToFile(simpLog, '  <time>' + strftime("%Y-%m-%d %H:%M:%S", localtime(timestamp)) + '</time>')
    # apToFile(simpLog, '  <request_type>' + request_type + '</request_type>')
    # apToFile(simpLog, '  <string>' + string + '</string>')
    # apToFile(simpLog, '  <signature>' + signature + '</signature>')
    # apToFile(simpLog, '  <server_response_simplified>' + server_response_simplified + '</server_response_simplified>')
    #
    # apToFile(simpLog, '</' + str(timestamp) + '>')
    # apToFile(simpLog, '\n\n')
    # simpLog.close()


    #dynamic XML creation
    simpLog=open('auto_logs/log_auto_trader.xml', "a+")
    if logDataObj.__dict__:
        if 'timestamp' in logDataObj.__dict__.keys():
            #begin entry
            apToFile(simpLog, '<' + str(logDataObj.__dict__['timestamp']) + '>')
            apToFile(simpLog, '  <time>' + strftime("%Y-%m-%d %H:%M:%S", localtime(logDataObj.__dict__['timestamp'])) + '</time>')
            #populate inside of xml entry
            keysList = list(logDataObj.__dict__.keys())
            for i in range(len(keysList)):
                if not keysList[i]=='timestamp':
                    if not keysList[i]=='serverResponseJSON':
                        if not keysList[i]=='server_response':
                            apToFile(simpLog, '  <' + keysList[i] + '>' + str(logDataObj.__dict__[keysList[i]]) + '</' + keysList[i] + '>')
            #end entry
            apToFile(simpLog, '</' + str(logDataObj.__dict__['timestamp']) + '>')
        else:
            apToFile(simpLog, '<' + str(time.time()) + '>')
            apToFile(simpLog, '  <time>' + strftime("%Y-%m-%d %H:%M:%S", localtime(time.time())) + '</time>')
            apToFile(simpLog, '  <error>True<error>\r\n  <error_msg>logDataObj has no timestamp</error_msg>')
            apToFile(simpLog, '</' + str(timestamp) + '>')
    else:
        apToFile(simpLog, '<' + str(time.time()) + '>')
        apToFile(simpLog, '  <time>' + strftime("%Y-%m-%d %H:%M:%S", localtime(time.time())) + '</time>')
        apToFile(simpLog, '  <error>True<error>\r\n  <error_msg>logDataObj is empty</error_msg>')
        apToFile(simpLog, '</' + str(timestamp) + '>')
    apToFile(simpLog, '\n\n')
    simpLog.close()



def apToFile(file,writeString):
    file.write(writeString + "\r\n")
