import datetime
import os
import shutil
import subprocess
import sys
import win32api

from pathlib import Path

class Direction():
    def __init__(self,debug=False):
        self.states = ['off','down','up']
        self.state = self.states[0]
        self._nos_states = len(self.states)
        self.debug = debug

    def transfer(self):
        return self.state

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
localConver = True
softDelete = True
execFlag = True
MAX_NOS = 8
debugFlag = False
fileDirection = Direction(debugFlag)
shutDownAfter = True

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
    print(f"Run started @: {ct}")

def cleanEmptyDir():

    for dir in next(os.walk(hardCodedPath))[1]:

        fullDir = f"{hardCodedPath}{os.sep}{dir}"
        if not os.listdir(fullDir):
            if execFlag:
                os.rmdir(fullDir)
            print(f"Removing -{fullDir}")
        else:
            print(f"NOT EMPTY -{fullDir}")
            for f in os.listdir(fullDir):
                print(f"\t{f}")

def moveFile(sourceFile):

    moveRequired = True
    fileName = os.path.basename(sourceFile)
    if debugFlag:
        print(f"Receiving {sourceFile} with direction of {fileDirection.transfer()}")

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
            print(f"Download to {toFile} in progress")
            shutil.move(sourceFile,toFile)
            if debugFlag:
                print(f"{sourceFile} moved to {toFile}")
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

    if localConver: 
        fromFile = moveFile(fullFilePath)
        toFile = getConversionName(fromFile)
        print(f"Will attempt to convert {fromFile} to {toFile}")
        conversion(fromFile,toFile)

        fileDirection.next()
        returnFile = moveFile(toFile)
        fileDirection.next()
        
        print(f"Conversion resulted in {returnFile}")

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
        subprocess.run(['ffmpeg','-i',sourceFile,to,'-c','h264','-preset','ultrafast'])

    #             subprocess.run(['ffmpeg','-i',original,converted])
    #             #subprocess.run(['ffmpeg','-i',original,converted,'-c','h264','-preset','ultrafast'])



if __name__ == "__main__":

    preRunCleanUp()
    #cleanEmptyDir()

    if localConver:
        fileDirection.next()

    results = getFilePathsByType(searchExt)

    if  len(results) > 0:
        times = 1
        for f in results:
            if times < MAX_NOS:
                prepareConversion(f)
                times += 1
                #win32api.MessageBox(0, 'hello', 'Conversion completed', 0x00001000) 
               

    #os.system("shutdown /s /t 1")
    #TODO limit nos of conversions
    #TODO add timer function
    #TODO check free space before each run
    #TODO Handle this type of logic error:
#     Download to Z:\Movies\Amy 2015.mp4 in progress
# Conversion resulted in Z:\Movies\Amy 2015.mp4
# (.venv) PS D:\dev\python\media_maintainer> & d:/dev/python/.venv/Scripts/python.exe d:/dev/python/media_maintainer/media_maintainer.py
# Download to D:\Video\working\Timeline.ts in progress
# Will attempt to convert D:\Video\working\Timeline.ts to D:\Video\working\Timeline.mp4
# Conversion not required as Z:\Movies\Timeline.mp4 already exists
# Download to Z:\Movies\Timeline.mp4 in progress
# Error occurred in moveFile function: [Errno 2] No such file or directory: 'D:\\Video\\working\\Timeline.mp4'
#  D:\Video\working\Timeline.mp4 to Z:\Movies\Timeline.mp4
# Conversion resulted in Z:\Movies\Timeline.mp4
    print("Run complete")
    if shutDownAfter:
        os.system('shutdown -s')
    

