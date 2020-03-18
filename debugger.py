#updated for python 3 usage
import requests, json
import time
from time import sleep, localtime, strftime
import sys
import os
import logging


fetchTime = localtime()


if not os.path.exists('datedCSV/' + strftime("%Y-%m-%d", fetchTime)):
    os.mkdir('datedCSV/' + strftime("%Y-%m-%d", fetchTime))

f=open('datedCSV/' + strftime("%Y-%m-%d", fetchTime) + '/BTC_' + strftime("%H", fetchTime) + '.csv', "a+")
f.write("This is a test\r\n")

print("done")
