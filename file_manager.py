#updated for python 3 usage
import time
from time import sleep, localtime, strftime
import sys
import os
from parse import * #pip install parse
#functionality bucket list:
    #run this on a schedule
    #automatically upload to google drive by reading password from a document on computer not on github, also use webcrawler gmail
    #insert fillers into daily files in case of missing data


def upLogFile(lastRun):
    f=open('datedCSV/filemanlog', "w")
    f.write("lastRun: " + str(lastRun) + ";\r\n")
    f.close()


#init
# lastRun, when files were last managed in seconds
if not os.path.exists('datedCSV/filemanlog'): #file does not yet exist
    lastRun = 0
    upLogFile(lastRun)
else:
    #read log for variables
    logFile=open("datedCSV/filemanlog", "r")
    logFileCont =logFile.read()
    lastRun = float(parse("lastRun: {};", logFileCont)[0])
    logFile.close()


#main loop
while True:
    #look for kill command
    endProc=open("kill_process", "r")
    endProcCont =endProc.read()
    if endProcCont[:4] == "true":
        exit()
    endProc.close()

    #update log file
    lastRun = time.time()
    upLogFile(lastRun)

    #concatenate hourly files into daily files
    #make list of days and generate appropriate for loop, running earliest first
        #if current day is earlier than lastRun
            #create file/header for that day and start filling with each hour (if it exists)




    #exit
    exit()
