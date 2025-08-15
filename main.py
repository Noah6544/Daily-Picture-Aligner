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
from PIL import Image as ExifImage



# if __name__ == "__main__": # today (11/24/23) i finally understood what this does when trying to use main as a package in terminal
parser = argparse.ArgumentParser(
    prog='Daily Picture Aligner',
    description = "Automate the eye coordinate alignment process (scaling, rotating, translating) of hundreds of photo to an initial image. ")
arguments = parser.parse_args()

###VARIABLES
DailyPhotoPath = "./DailyPhotos/"# "ALL Daily photos/"
FailedImagesPath = "./FailedPhotos/"
BaseImagePath = "./BaseImages/" # "./BaseImages/"
OutputPath = "./AlignedPhotos/"
fileAffix = ".png"
fileSuffix = "Aligned_"
failedImages = []

files = os.listdir(Path(BaseImagePath))
files = list(filter(lambda a: not a.startswith("."), files))

if len(files) > 1:
    raise Exception("Ensure there's only one base image, and that you deleted the initial text file.")

file = files[0]

libfile = PurePath(BaseImagePath+file)
BaseImage = classes.BaseImage(libfile)

###RUNNING CODE

print("\n-------------------------------\nStarting Script\nAdjusting Images\nWriting Files\nCheck 'AlignedPhotos' folder and make sure the script is working\nCheck ErrorLog.txt if output isn't working as expected!\n-------------------------------\n")


#The following code sorts images by EXIF data, the metadate embeded in the file, as opposed to creation date.
#This is because files downloaded from, for example, GooglePhotos, have creation date at the time of download, but exif data of the time they were taken
 
fileList = os.listdir(DailyPhotoPath)
exifDict = dict.fromkeys(fileList)
fileListSorted =  []

for img in fileList:
    try:
        exifDict[img] = (ExifImage.open(DailyPhotoPath+img)._getexif()[36867])
    except:
        del exifDict[img]

sortedExifList = sorted(exifDict.items(), key=lambda x: x[1]) #sorts images in a [(path/, date), (path, date)] format

for img in sortedExifList:
    img = Path(DailyPhotoPath + img[0])
    fileListSorted.append(img)

completedFiles = open("completedImages.txt", "r").read().split(",")
count = 0

#this for gets all files keeps the ones that are uncorrupted (>0bytes) jpg/png files.
for index, file in enumerate(tqdm(fileListSorted)):
    libfile = file
    file = file.name #Pathlib returns it as a pathlib.WindowsPath instead of a string, and it returns the parent folder like this: parentfolder/file.jpg, so we need to convert it back into a string for the logic ahead using file.name, just the file name as string
    if file in completedFiles: #if our file has already been aligned, do nothing.
        count+=1
    else:
        #endswith("g") because that's for png/jpg files. I didn't know how to check for the last 4 position slots because each fle name size is different and the initial start is different. anyways this works currently
        if file.lower().endswith("g") and os.path.getsize(DailyPhotoPath + file) > 0:
            currentImage = classes.Image(libfile)
            success = currentImage.alignImagetoBaseImage(BaseImage)
            if success == True:
                if sortedExifList[index][0] == file:
                    date = str(sortedExifList[index][1])
                    date = date.replace(":","-") #colons aren't allowd in file names!! 
                    count+=1
                    cv.imwrite(OutputPath+str(count)+"_"+fileSuffix+libfile.stem+"_"+date+"_"+fileAffix , currentImage.cvimage)
                else:
                    count+=1
                    cv.imwrite(OutputPath+str(count)+"_"+fileSuffix+libfile.stem+fileAffix , currentImage.cvimage)
                
                with open("completedImages.txt", "a") as completed_file:
                    completed_file.write(file + ",")
            else:
                failedImages.append(success)
                os.rename(libfile, FailedImagesPath + file)
                failedImages.append(file)
                # Move the picture to the failedPhotos, this helps you debug the issue instead of having to go through the entire folder of images again.
                
                pass #handling errors in classes.py
       
        else:
            pass
        
    # break  


print("\nSuccessfully Aligned " + str(count) +" Pictures!\nIf you found this script useful, please let me know, I would love your feedback! \nIf you want to directly support my future (college, projects, etc.), my CashApp is $NoahCutz, or you can BuyMeACoffee (https://buymeacoffee.com/noahbuchanan).")
if len(failedImages) > 0:
    print("However, failed to align the following images: ", str(failedImages))
input("Press Enter to exit: ")
