#Luke Henderson
#Version info on auto_trader.py
#Solely for BaseFEX use
import time
from time import sleep, localtime, strftime
import sys
import os
from parse import * #pip install parse (or pip3 install parse)
import timeit


def createLog(path):
    f=open(path, "w")
    f.write('THIS IS THE FIRST LINE\r\n')
    f.close()


def apToFile(file,writeString):
    file.write(writeString + "\r\n")


    # apToFile(verboseLog, "<" + str(0) + ">")
    # apToFile(verboseLog, "  <request_type>" + "some long text here~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" + "</request_type>")
    # apToFile(verboseLog, "  <request_type>" + "some long text here~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" + "</request_type>")
    # apToFile(verboseLog, "  <request_type>" + "some long text here~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" + "</request_type>")
    # apToFile(verboseLog, "  <request_type>" + "some long text here~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" + "</request_type>")
    # apToFile(verboseLog, "  <request_type>" + "some long text here~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" + "</request_type>")
    # apToFile(verboseLog, "</" + str(0) + ">")
    # apToFile(verboseLog, "\n\n")







# code snippet to be executed only once
mysetup = '''
import time
from time import sleep, localtime, strftime
import sys
import os
import timeit

file=open("auto_logs/timer_file", "a+")
    '''

# code snippet whose execution time is to be measured
mycode = '''
file.write("123555555555555555555555555555555555555555\\r\\n")
    '''

# timeit statement
tryNum = 0
while True:
    print(str(tryNum) + ": " + str(timeit.timeit(setup = mysetup, stmt = mycode, number = 100000)))
    tryNum += 1
    sleep(0.1)

#my timeit code
# print(timeit.timeit(stmt='apendLotsOfData()', number=10000))
# # timeit.timeit(apendLotsOfData(), number=1)












# verboseLog.close()
