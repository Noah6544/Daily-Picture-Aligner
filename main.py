import os
import sys
import numpy as np
import mediapipe as mp
import cv2 as cv
from pathlib import *
import argparse
import classes 
import time
from tqdm import tqdm, trange




# if __name__ == "__main__": # today (11/24/23) i finally understood what this does when trying to use main as a package in terminal
parser = argparse.ArgumentParser(
    prog='Daily Picture Aligner',
    description = "Automate the eye coordinate alignment process (scaling, rotating, translating) of hundreds of photo to an initial image. ")
arguments = parser.parse_args()

###VARIABLES
DailyPhotoPath = "./DailyPhotos/"# "ALL Daily photos/"
BaseImagePath = "./BaseImages/" # "./BaseImages/"
OutputPath = "./AlignedPhotos/"
fileAffix = "_Aligned.jpg"
fileSuffix = "_"


class FileManager: #toDO: find a better classname for the filemanager
    def __init__(self,file):
        self.file 

files = os.listdir(Path(BaseImagePath))
files = list(filter(lambda a: not a.startswith("."), files))

if len(files) > 1:
    raise Exception("Ensure there's only one base image, and that you deleted the initial text file.")

file = files[0]

libfile = PurePath(BaseImagePath+file)
BaseImage = classes.BaseImage(libfile)

###RUNNING CODE

print("\n-------------------------------\nStarting Script\nAdjusting Images\nWriting Files\nCheck 'AlignedPhotos' folder and make sure the script is working\nCheck ErrorLog.txt if output isn't working as expected!\n-------------------------------\n")
time.sleep(5)
count = 1
fileList = os.listdir(DailyPhotoPath)
# fileListSorted = fileList.sort(key=lambda x: os.path.getctime(x))
fileListSorted = list(sorted(Path(DailyPhotoPath).iterdir(), key=os.path.getctime))

#specifically this for loop gets all files and only keeps the ones that are jpg files and aren't curropted or 0 in size.
for file in tqdm(fileListSorted):
    libfile = file
    file = file.name #Pathlib returns it as a pathlib.WindowsPath instead of a string, and it returns the parent folder like this: parentfolder/file.jpg, so we need to convert it back into a string for the logic ahead using file.name, just the file name as string
    if fileSuffix+file+fileAffix in os.listdir(OutputPath): #if our file has already been aligned, do nothing.
        pass
    else:
        #endswith("g") because that's for png/jpg files. I didn't know how to check for the last 4 position slots because each file name size is different and the initial start is different. anyways this works currently
        if file.lower().endswith("g") and os.path.getsize(DailyPhotoPath + file) > 0 and file != "1871.jpg":
            currentImage = classes.Image(libfile)
            #consider taking away the walrus operator cuz its only python 3.8.0+
            success = currentImage.alignImagetoBaseImage(BaseImage)
            if success:
                cv.imwrite(OutputPath+str(count)+fileSuffix+file+fileAffix,currentImage.cvimage)
                count+=1
            else:
                pass #handling errors in classes.py
       
        else:
            pass
print("\nSuccessfully Aligned " + str(count) +" Pictures!\nIf you found this script useful, please let me know, I would love your feedback! \nIf you want to directly support my future (college, projects, etc.), my CashApp is $NoahCutz, or you can BuyMeACoffee (https://buymeacoffee.com/noahbuchanan).")
input("Press Enter to exit: ")
