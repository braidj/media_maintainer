import re
import os
import sys
import shutil
import inspect
from pathlib import Path

testFiles = ['A Deadly Vendetta-00.04.14.039-00.24.26.359-merged-00.00.20.000-01.20.14.048.mp4',
'Child 44-00.01.33.760-00.18.10.920-merged.mp4',
'Confessions of a Teenage Drama Queen-00.01.11.959-01.21.41.159.mp4',
'Devils\'s Knot-00.05.43.600-00.18.35.960-merged.mp4',
'Eight Below-00.02.25.280-01.51.51.239.mp4',
'Ella Enchanted-00.02.52.000-01.29.45.359.mp4',
'The Chronicles of Narnia The Lion, The Witch And The Wardrobe-00.01.02.000-02.07.06.199.mp4',
'The Damned United-00.03.53.919-01.32.43.039.mp4',
'The Peanut Butter Falcon-00.03.10.746-01.27.58.199.mp4',
'Nothing to change here.ts']


searches = ['-\d{2}\.\d{2}\.\d{2}\.\d{3}','-merged','-cut','-\d{13}','_\d{8}_\d{4}']
uploadDir = r"Z:\Movies"
sourceDir = r"D:\Video\trimming\final"
ADVERTS=r"D:\Video\trimming\adverts"
expectedExts=['ts','mp4']
debug=False

def flagFilmsToSkip(checkFolder):
    """Check files to see if it has already been uploaded
    If they have then rename to .ignore"""

    filmLibrary = getFilmTitles(uploadDir)
    filmsToCheck = getFilmTitles(checkFolder)

    for f in filmsToCheck:
        if f in filmLibrary:
            print(f"Already got {f}")
            for fExt in expectedExts:
                if os.path.exists(f"{checkFolder}{os.sep}{f}.{fExt}"):
                    renameFile(f"{checkFolder}{os.sep}{f}.{fExt}",f"{checkFolder}{os.sep}{f}.{fExt}.ignore")


def getFilmTitles(checkFolder):
    """Returns a list of just the film title, no path, extension etc"""

    files = [str(x) for x in Path(checkFolder).rglob("*")]
    libFilmFiles = list(map(os.path.basename,files)) # Remove the path
    libFilmTitles = [os.path.splitext(x)[0] for x in libFilmFiles]
    return libFilmTitles

def getFiles(folderToProcess,filter):
    """Returns a list of files in target directory matching the desired file format"""

    print(f"Parsing {folderToProcess} for {filter} files")

    if debug:
        for path in Path(folderToProcess).rglob(filter):
            print(f"Found {path}")

    all_files = [str(x) for x in Path(folderToProcess).rglob(filter)] 

    return all_files

def main():

    
    thisFunc = inspect.currentframe().f_code.co_name
    print(f"Running {thisFunc}")

    tidyFileNames(ADVERTS)
    flagFilmsToSkip(ADVERTS)

    sys.exit(0)

    for f in getFiles(sourceDir,"*.mp4"):

        clean = f
        for search in searches:
            clean = replace(clean,search)

        if renameFile(f,clean):
            results = list(map(os.path.basename,[f,clean]))
            print(f"Renamed: {results[0]} -> {results[1]}")

        if moveFile(clean,uploadDir):
            print(f"{results[0]} uploaded to {uploadDir}")

def tidyFileNames(folderToCheck):
    """Renames the file to be just the film name plus the extension"""

    filters = list(map(lambda x: "*." + x, expectedExts))

    for filter in filters:

        for f in getFiles(folderToCheck,filter):

            clean = f
            for search in searches:
                clean = replace(clean,search)

            if renameFile(f,clean):
                results = list(map(os.path.basename,[f,clean]))
                if results[0] != results[1]:
                    print(f"Renamed: {results[0]} -> {results[1]}")


def replace(text,pattern,replace=""):  
    """Replaces the search term"""

    thisFunc = inspect.currentframe().f_code.co_name
    result = re.sub(pattern,replace,text)
    return result

def moveFile(sourceFullPath,targetDir):
    """Move the file to destination"""

    thisFunc = inspect.currentframe().f_code.co_name
    try:
        shutil.move(sourceFullPath,targetDir)
        return True
    except Exception as e:
        print(f"{thisFunc} issue: {e}")
        return False

def renameFile(oldName,newName):
    """Renames the files, revealing film name"""
    
    thisFunc = inspect.currentframe().f_code.co_name
    if oldName == newName:
        return True
    else:
        try:
            os.rename(oldName,newName)
            return True
        except Exception as e:
            print(f"{thisFunc} issue: {e}")
            return False

if __name__ == "__main__":

    main()