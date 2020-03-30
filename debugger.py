#updated for python 3 usage
import requests, json
import time
from time import sleep, localtime, strftime
import sys
import os
import logging
from parse import *

# def myFnc(a):
#     print("1")
#
# def myFnc(a,b):
#     print("2")
#
# def myFnc(a,b,c):
#     print("3")



def myFnc(*args):
    if len(args) == 0:
        print("Number of args = 0")
    elif len(args) == 1:
        print("Number of args = 1")
    else:
        print("Number of args >= 2")









myFnc(2,2)

print("done")
