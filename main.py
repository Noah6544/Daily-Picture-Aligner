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



###VARIABLES
DailyPhotoPath = "./DailyPhotos/"#
FailedImagesPath = "./FailedPhotos/"
BaseImagePath = "./BaseImages/" 
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

#RUNNING CODE

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

# Get all uncorrupted (>0bytes) jpg/png files.
for index, file in enumerate(tqdm(fileListSorted)):
    libfile = file
    file = file.name 
    if file in completedFiles: 
        count += 1
    else:
        if file.lower().endswith("g") and os.path.getsize(DailyPhotoPath + file) > 0:
            currentImage = classes.Image(libfile)
            success = currentImage.alignImagetoBaseImage(BaseImage)
            if success == True:
                if sortedExifList[index][0] == file:
                    date = str(sortedExifList[index][1])
                    date = date.replace(":","-") 
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
                pass #handling errors in classes.py
       
        else:
            pass
        


print("\nSuccessfully Aligned " + str(count) +" Pictures!\nIf you found this script useful, please let me know, I would love your feedback! \nIf you want to directly support my future (college, projects, etc.), you can BuyMeACoffee :D (https://buymeacoffee.com/noahbuchanan).")
if len(failedImages) > 0:
    print("However, failed to align the following images: ", str(failedImages))
input("Press Enter to exit: ")

