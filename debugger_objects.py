#updated for python 3 usage
import requests, json
import time
from time import sleep, localtime, strftime
import sys
import os
import logging
from parse import *

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

class logData: #timestamp, request_type, string, signature, server_response_simplified, server_response
  pass

# print(bcolors.FAIL)
# print(DEBUG_TOOL)
# print(bcolors.ENDC)

# print(bcolors.WARNING + "Success!" + bcolors.ENDC)
# exit()



expObject = logData()

expObject.timestamp = 2
expObject.test = 'Stringggyyyy'
print(expObject.__dict__)
expObject = logData()
# expObject.test = 'str2'
if expObject.__dict__:
    print(expObject.__dict__)
else:
    print("Empty")





print("done")
























#end
