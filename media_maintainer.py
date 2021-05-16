import os
import shutil
import subprocess
from pathlib import Path

searchExt = ".ts"
convertTo = ".mp4"
hardCodedPath = os.sep.join([r"Z:\Movies"])
workingDir = os.sep.join([r"C:\Users\braid\Downloads\working"])
localConver = False
softDelete = True

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
            print(path)
            #moveFile(path)

    all_files = [str(x) for x in Path(hardCodedPath).rglob(filter)]

    return all_files

def convertFile(orginalFormat,newFormat):

    origDir, origExt = os.path.splitext(orginalFormat)
    newDir, newExt = os.path.splitext(newFormat)

    if origExt == newExt:
        print(f"Nothing to do: {newFormat}")
    elif origDir != newDir:
         print("need to move file first")
    else:
        print("conversion needed")
        if localConver:
            print("need to copy down first")
        #subprocess.run(['ffmpeg','-i',original,converted])

if __name__ == "__main__":

    result = getFilePathsByType(searchExt,True)

    if  len(result) > 0:
        print(f"First one is: {result[1]}")
        original,converted = getFilePairs(result[1])
        convertFile(original,converted)


    print(f"Complete for {len(result)} files")