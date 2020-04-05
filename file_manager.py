#Luke Henderson
import time
from time import sleep, localtime, strftime
import sys
import os
from parse import * #pip install parse (or pip3 install parse)
#functionality bucket list:
    #run this on a schedule
    #automatically upload to google drive by reading password from a document on computer not on github, also use webcrawler gmail
    #insert fillers into daily files in case of missing data

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

#update the log file (lastRun: time in seconds that it was run last)
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


    #display lastRun
    print(bcolors.OKBLUE  + "Last Run: " + bcolors.ENDC + strftime("%Y-%m-%d %H:%M:%S", time.localtime(lastRun)))
    print(bcolors.OKBLUE  + "Directories detected: " + bcolors.ENDC)

    #display directory structure in datedCSV
    for root, dirs, files in os.walk("datedCSV", topdown=False):
        # for name in files:
        #     print(os.path.join(root, name))
        for name in dirs:
            print(os.path.join(root, name))
    print("\r\n")

    #prompt for what folder to concatenate
    inputValidated = False
    while not inputValidated:
        workDirPartial = input("Enter the day you would like to aggregate: ")
        # workDirPartial = "2020-04-01" #used for quick debugging
        workDirComplete = "datedCSV/" + workDirPartial
        if os.path.exists(workDirComplete):
            if input("Aggregate " + workDirComplete + "? (y/n) ") == "y":
                # print("Aggregate " + workDirComplete + "? (y/n) ") #used for quick debugging
                inputValidated = True
        else:
            print("Directory doesn't exist")
    print(bcolors.WARNING  + "Aggregating..." + bcolors.ENDC)





    #get CSV_HEADER
    #get list of files to check
    workFiles = os.walk(workDirComplete, topdown=False)
    # print("getting CSV header")
    #analyze workFiles
    fileList = []
    for root, dirs, files in workFiles: #datedCSV/2020-04-01/BTC_18.csv for example
        for name in files:
            if os.path.join(root, name)[20:24] == "BTC_":
                if len(fileList)>0:
                    fileList.append(os.path.join(root, name))
                else:
                    fileList = [os.path.join(root, name)]
    if len(fileList)==0:
        print(bcolors.FAIL  + "Error: No data files in directory" + bcolors.ENDC)
        exit()
    fileList.sort() #make it alphabetical order
    #obtain CSV_HEADER of initial file and check congruency
    for i in range(len(fileList)):
        # print("checking " + fileList[i])
        currWorkFile = open(fileList[i], "r")
        currWorkFileCont =currWorkFile.read()
        parsedFile = search("Time,{}\n", currWorkFileCont)
        if not parsedFile is None: #if the parse returned some information
            if i==0: #initial run:
                CSV_HEADER = "Time," + parsedFile[0]
                print("Using header: " + CSV_HEADER)
            else: #additional runs:
                additHeader = "Time," + parsedFile[0]
                if not additHeader == CSV_HEADER: #header matches CSV_HEADER
                    print(bcolors.FAIL  + "Error: Incongruent header(s)" + bcolors.ENDC)
                    exit()
        else:
            print(bcolors.FAIL  + "Error: Parsing of header(s) failed" + bcolors.ENDC)
            exit()
        currWorkFile.close()







    #create folder/file/header for that day and start filling with each hour (if it exists)
    outputFile = 'datedCSV/_' + workDirPartial[:7] + "/BTC_A_" + workDirPartial[-2:] + ".csv" #datedCSV/_YYYY-MM/BTC_A_DD.csv
    if not os.path.exists(outputFile[:17]): #dir does not yet exist
        os.mkdir(outputFile[:17])
    if not os.path.exists(outputFile): #file does not yet exist
        outputFile = open(outputFile, "a+")
        outputFile.write(CSV_HEADER)
        # outputFile.close() #file needs to still be open
    else:
        #display error
        print(bcolors.FAIL  + "Error: Output file already exists" + bcolors.ENDC)
        exit()
    #begin filling with each hour
    for i in range(len(fileList)):
        print("adding " + fileList[i])
        currWorkFile = open(fileList[i], "r")
        currWorkFileCont =currWorkFile.read()
        parsedFile = parse(CSV_HEADER + "{}", currWorkFileCont)
        if not parsedFile is None: #if the parse returned some information
            fileString = parsedFile[0].rstrip()
            outputFile.write(fileString)
    outputFile.close()

    print(bcolors.WARNING  + "Success!" + bcolors.ENDC)



    # this is an automation scheme:
    # # concatenate hourly files into daily files
    # # make list of days and generate appropriate for loop, running earliest first
    # #     if current day is earlier than lastRun
    # #         create folder/file/header for that day and start filling with each hour (if it exists)

    #update log file
    lastRun = time.time()
    upLogFile(lastRun)

    #exit
    exit()
