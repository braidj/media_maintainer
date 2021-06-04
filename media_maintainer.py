import datetime
import os
import shutil
import subprocess
import sys
import logging
import pathlib
from pathlib import Path
    #os.system("shutdown /s /t 1")
    #TOOD Unit tests on core functions
    #TODO check free space before each run
    #TODO Check file BEFORE conversion
    #TODO Write logging to a web page ?
    #TODO Add biggest files first /sort by size
    #TODO Write original and new size to the log file

class Search():
    def __init__(self,searchDir,workingDir,searchFor,logger,convertToExt=".mp4",batchSize = 10,localConversion = True, shutDownAfter = False,DebugOn=False):

        self.searchDir = searchDir
        self._workingDir = workingDir
        self._searchFor = searchFor
        self._convertToExt = convertToExt
        self.batchSize = batchSize
        #self.localConversion = localConversion
        self.shutDownAfter = shutDownAfter
        self.log = logger

        if len(self._searchFor) == 3:
            self._convertFromExt = self._searchFor
            self._filterCriteria = f"*{self._convertFromExt}"
        else:
            self._convertFromExt = pathlib.Path(searchFor).suffix
            self._filterCriteria = searchFor

    @property
    def workingDir(self):
        return self._workingDir

    @property
    def convertToExt(self):
        return self._convertToExt

    @property
    def filterCriteria(self):
        return self._filterCriteria

    @filterCriteria.setter
    def filterCriteria(self,value):
        self._filterCriteria = value
    

    def findFiles(self):
        """Returns a list of all files matching (a specified file type)"""

        filter = self.filterCriteria

        if debugFlag:

            for path in Path(searchBy.searchDir).rglob(filter):
                self.log.record(f"Found {path}")

        all_files = [str(x) for x in Path(searchBy.searchDir).rglob(filter)] 

        return all_files

    def _copyDown(self,fullPathFile):
        """Moves the selected movie files to the working directory
        (Assumes we receive a full path)"""
        return self._moveFile(fullPathFile,self.workingDir,"down")
        

    def convertFile(self,originalFile):
        """Convert a specific file, uses the paths already supplied"""

        workingCopy = self._copyDown(originalFile)
        workingCopyConv = workingCopy.replace(f"{self._convertFromExt}",f"{self.convertToExt}")

        try:
            subprocess.run(['ffmpeg','-i',workingCopy,workingCopyConv])
            self.log.record(f"Converted {workingCopy} to {workingCopyConv}")
        except Exception as error:
            self.log.record(f"Error occurred in moveFile function: {error}\n {workingCopy} to {workingCopyConv}")

        _ = self._copyUp(workingCopyConv)


    def _copyUp(self,fullPathFile):
        """Moves the selected movie files from the working directory back to the original dir
        (Assumes we receive a full path)"""
        return self._moveFile(fullPathFile,self.searchDir,"up")

    def _moveFile(self,sourceFile,toPath,direction):

        if direction == "up": # have to change source to be working direction
            alt = sourceFile.replace(f"{self.searchDir}",f"{self.workingDir}")
            sourceFile = alt

        fileName = os.path.basename(sourceFile)
        destinationFile = F"{toPath}{os.sep}{fileName}"

        if sourceFile == destinationFile:
            self.log.record(f"Move not required {sourceFile} to {destinationFile}")
        else:
            try:
                shutil.move(sourceFile,destinationFile)
                self.log.record(f"{sourceFile} copied {direction} to {destinationFile}")
            except Exception as error:
                print(f"Error occurred in moveFile function: {error}\n {sourceFile} to {toPath}")

        return destinationFile


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
        self.logger.info(f"Log file created")

    def record(self,message,logAsWell=True):

        ct = datetime.datetime.now()

        if logAsWell:
            self.logger.info(message)

        print(ct,message)

def preRunCleanUp():

    if sys.platform.startswith('linux'):
        os.system('clear')
    elif sys.platform.startswith('win32'):
        os.system('cls')


    ct = datetime.datetime.now()
    sysStatus.record("Run started")

def cleanEmptyDir():

    for dir in next(os.walk(searchBy.workingDir))[1]:

        fullDir = f"{searchBy.workingDir}{os.sep}{dir}"
        if not os.listdir(fullDir):
            os.rmdir(fullDir)
            sysStatus.record(f"Removing -{fullDir}")
        else:
            sysStatus.record(f"NOT EMPTY -{fullDir}")
            for f in os.listdir(fullDir):
                sysStatus.record(f"\t{f}")

def countFolderDepth(filePath):
    return str(filePath).count(os.sep)
 
if __name__ == "__main__":

    debugFlag = True
    shutDownAfter = False
    workingDir=r"D:\Video\working"
    sysStatus = Status(workingDir)
    searchBy = Search(r"Z:\Movies",workingDir,".ts",sysStatus,batchSize=1)
    
    preRunCleanUp()
    #cleanEmptyDir()
    results = searchBy.findFiles() #getFilePathsByType()
    sysStatus.record(f"Only {len(results)} file(s) match(es) the search. The batch limit set to {searchBy.batchSize}")
    sysStatus.record(f"Conversion run started for files of type {searchBy.filterCriteria} to {searchBy.convertToExt} in {searchBy.searchDir}")
    times = 0
    for f in results:
        if times < searchBy.batchSize:
            searchBy.convertFile(f)
            times += 1

    sysStatus.record("Run complete")

    if shutDownAfter:
        os.system('shutdown -s')

    sys.exit(0)
    

