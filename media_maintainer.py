import datetime
import os
import shutil
import subprocess
import sys
import win32api
import logging


from pathlib import Path

class Status():
    def __init__(self,loggingDir):
        tds = datetime.datetime.now()
        logFile = tds.strftime("%Y%m%d_%H%M%S")
        fullLogPath = f"{loggingDir}{os.sep}{logFile}.log"
        self.logger = logging.getLogger('mylogger')
        self.logger.setLevel(logging.INFO) #set logger level
        handler = logging.FileHandler(fullLogPath)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')# create a logging format
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.info(f"Conversion run started for {MAX_NOS} files of type {convertTo} in {hardCodedPath}")

    def record(self,message,logAsWell=True):

        ct = datetime.datetime.now()

        if logAsWell:
            self.logger.info(message)

        print(ct,message)


class Direction():
    def __init__(self,debug=False):
        self.states = ['off','down','up']
        self.state = self.states[0]
        self._nos_states = len(self.states)
        self.debug = debug

    def transfer(self):
        return self.state
    
    def local(self): # Startign start for local file conversion
        self.state = 'down'

    def next(self):

        posIndex = self.states.index(self.state)
        currentState = self.state

        if posIndex == self._nos_states -1:
            self.state = self.states[0]
        else:
            self.state = self.states[posIndex+1]

        newState = self.state
        if self.debug:
            print(f"Moved from {currentState} to {newState}")

searchExt = ".ts"
convertTo = ".mp4"
hardCodedPath = os.sep.join([r"Z:\Movies"])
workingDir = os.sep.join([r"D:\Video\working"])
loggingDir = workingDir
localConver = True
MAX_NOS = 8
debugFlag = False
fileDirection = Direction(debugFlag)
shutDownAfter = False

def checkConversionRequired(convertedFilePath):

    result = True

    if os.path.exists(convertedFilePath):
        print(f"Converted version of {convertedFilePath} already exists")
        result = False 

    # check if exists in base folder
    namePart = os.path.basename(convertedFilePath)
    altName = f"{hardCodedPath}{os.sep}{namePart}"

    if os.path.exists(altName):
        print(f"Converted version of {altName} already exists")
        result = False

    return result

def preRunCleanUp():

    if sys.platform.startswith('linux'):
        os.system('clear')
    elif sys.platform.startswith('win32'):
        os.system('cls')

    ct = datetime.datetime.now()
    sysStatus.record("Run started")

def cleanEmptyDir():

    for dir in next(os.walk(hardCodedPath))[1]:

        fullDir = f"{hardCodedPath}{os.sep}{dir}"
        if not os.listdir(fullDir):
            os.rmdir(fullDir)
            sysStatus.record(f"Removing -{fullDir}")
        else:
            sysStatus.record(f"NOT EMPTY -{fullDir}")
            for f in os.listdir(fullDir):
                sysStatus.record(f"\t{f}")

def moveFile(sourceFile):

    moveRequired = True
    fileName = os.path.basename(sourceFile)
    if debugFlag:
        sysStatus.record(f"Receiving {sourceFile} with direction of {fileDirection.transfer()}")

    direction = fileDirection.transfer()

    if direction == "down": # hardCodedPath -> Working
        toFile = f"{workingDir}{os.sep}{fileName}"

    if direction == "up": # hardCodedPath -> Working
        toFile = f"{hardCodedPath}{os.sep}{fileName}"

    if direction== "off":
        moveRequired = False
        toFile = sourceFile

    if moveRequired:
        try:
            sysStatus.record(f"Download to {toFile} in progress")
            shutil.move(sourceFile,toFile)
            if debugFlag:
                sysStatus.record(f"{sourceFile} moved to {toFile}")
        except Exception as error:
            print(f"Error occurred in moveFile function: {error}\n {sourceFile} to {toFile}")

    return toFile



    # if countFolderDepth(filePath) > countFolderDepth(hardCodedPath):
    #     fileName = os.path.basename(filePath)
    #     newLocation = f"{hardCodedPath}{os.sep}{fileName}"
    #     print(f"moving {filePath} to {newLocation}")
        #

def countFolderDepth(filePath):
    return str(filePath).count(os.sep)
 
def getConversionName(originalFullFilePath):
    # received the full path
    # Return the name of the file resulting from the conversion
    convertedFile = originalFullFilePath.replace(searchExt,convertTo)
    return convertedFile

def getFilePathsByType(extension = searchExt):
    """Returns a list of all files matching (a specified file type"""

    filter = f"*{searchExt}"

    if debugFlag:

        for path in Path(hardCodedPath).rglob(filter):
            print(f"Found {path}")

    all_files = [str(x) for x in Path(hardCodedPath).rglob(filter)]

    return all_files

def prepareConversion(fullFilePath):
    # Assume that the paths are always the same, separate out the
    # logic that the files are moved prior to conversion
    # if it needs local copy down then do that first
    # checknew file does already exists
    # check if converted file already exists in current location
    # check if converted file already exists in working location

    fromFile = fullFilePath
    
    if localConver: 
        fromFile = moveFile(fullFilePath)
    
    toFile = getConversionName(fromFile)

    sysStatus.record(f"Will attempt to convert {fromFile} to {toFile}")
    conversion(fromFile,toFile)

    finalFile = toFile

    if localConver: 
        fileDirection.next()
        finalFile = moveFile(toFile)
        fileDirection.next()

    sysStatus.record(f"Conversion resulted in {finalFile}")

def conversion(sourceFile,to):

    proceed=True

    if os.path.exists(to):
        print(f"Conversion not required as {to} already exist")
        proceed=False
        exit(1)


    if localConver:
        # if local have to check converted file does n't already exist at remote location
        remoteFileCheck = f"{hardCodedPath}{os.sep}{os.path.basename(to)}"
        if os.path.exists(remoteFileCheck):
            print(f"Conversion not required as {remoteFileCheck} already exists")
            proceed=False

    if proceed:
        
        subprocess.run(['ffmpeg','-i',sourceFile,to])

if __name__ == "__main__":
  
    sysStatus = Status(workingDir)
    preRunCleanUp()
    #cleanEmptyDir()

    results = getFilePathsByType(searchExt)
    sysStatus.record(f"Only {len(results)} match the search, with the batch limit set to {MAX_NOS}")

    if  len(results) > 0:
        times = 0
        for f in results:
            
            if times < MAX_NOS:
                if localConver:
                    fileDirection.local()

                prepareConversion(f)
                times += 1

    #os.system("shutdown /s /t 1")
    #TODO logic needs to be tested for a batch run
    #TODO check free space before each run
    #TODO Check file BEFORE conversion
    #TODO Write logging to a web page ?
    #TODO Add biggest files first /sort by size
    #TODO specific file processing

    sysStatus.record("Run complete")

    if shutDownAfter:
        os.system('shutdown -s')
    

