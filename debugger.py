#updated for python 3 usage
import requests, json
import time
from time import sleep, localtime, strftime
import sys
import os
import logging


if not os.path.exists('csv/dated' + strftime("%Y-%m-%d_%H", localtime())):
    os.mkdir('csv/dated' + strftime("%Y-%m-%d_%H", localtime()))

f=open('csv/dated/BTC.csv', "a+")
f.write("Time,Kraken,Bitstamp,Bitfinex,Bitflyer,Itbit\r\n")

print(strftime("%Y-%m-%d_%H", localtime()))
