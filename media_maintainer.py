import datetime
import os
import shutil
import subprocess
import sys
from pathlib import Path

searchExt = ".vob"
convertTo = ".mp4"
hardCodedPath = os.sep.join([r"Z:\Movies"])
workingDir = os.sep.join([r"C:\Users\braid\Downloads\working"])
localConver = False
softDelete = True

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
            os.rmdir(fullDir)
            print(f"Removing -{fullDir}")
        else:
            print(f"NOT EMPTY -{fullDir}")
            for f in os.listdir(fullDir):
                print(f"\t{f}")

def moveFile(filePath):

    if countFolderDepth(filePath) > countFolderDepth(hardCodedPath):
        fileName = os.path.basename(filePath)
        newLocation = f"{hardCodedPath}{os.sep}{fileName}"
        print(f"moving {filePath} to {newLocation}")
        #shutil.move(filePath,newLocation)

def countFolderDepth(filePath):
    #os_independent_path = os.sep.join([filePath])
    #print(os_independent_path)
    return str(filePath).count(os.sep)
 
def getFilePairs(originalFullFilePath):

    origFileName, _ = os.path.splitext(originalFullFilePath)
    converted_file = origFileName + convertTo

    return [originalFullFilePath,converted_file]

def getFilePathsByType(extension = searchExt,displayResults = True):
    """Returns a list of all files matching (a specified file type"""

    filter = f"*{searchExt}"

    if displayResults:

        for path in Path(hardCodedPath).rglob(filter):
            print(f"Found {path}")
            #moveFile(path)

    all_files = [str(x) for x in Path(hardCodedPath).rglob(filter)]

    return all_files

def convertFile(originalFormat,newFormat):

    origDir, origExt = os.path.splitext(originalFormat)
    newDir, newExt = os.path.splitext(newFormat)

    if origExt == newExt:
        print(f"Nothing to do: {newFormat}")
    elif origDir != newDir:
         print("need to move file first")
    else:
        print(f"Conversion needed {originalFormat} to {newFormat}")
        if localConver:
            print("need to copy down first")
            #subprocess.run(['ffmpeg','-i',original,converted])

if __name__ == "__main__":

    preRunCleanUp()
    cleanEmptyDir()

    results = getFilePathsByType(searchExt,True)

    if  len(results) > 0:

        for f in results:
            original,converted = getFilePairs(f)
            convertFile(original,converted)

    #os.system("shutdown /s /t 1")
    #TODO copy file to working directory then copy back
    #TODO clean up after conversion
    #TODO limit nos of conversions
    #TODO check converted fiels does n't already exist
    print("Run complete")

