#updated for python 3 usage
import requests, json
import time
from time import sleep, localtime, strftime
import sys
import os
import logging
from parse import *


#Learned:
# parsedFile = parse("startChar{}endChar", currWorkFileCont) #uses last matching endChar instead of first
# parsedFile = search("Time,{}\n", currWorkFileCont) #search finds the first matching endChar





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




logFile=open("datedCSV/filemanlog", "r")
logFileCont = logFile.read()
parsedString = parse("lastRun: {}", logFileCont)
print(bcolors.FAIL)
print(parsedString)
print(bcolors.ENDC)
if not parsedString is None:
    lastRun = "Prefix" + parsedString[0]
    print(lastRun)
else:
    print("Error: Parsing of header(s) failed")
logFile.close()


print("done")
