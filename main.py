import os
import numpy as np
import mediapipe as mp
import cv2 as cv
from pathlib import *
import argparse
import classes 




# if __name__ == "__main__": # today (11/24/23) i finally understood what this does when trying to use main as a package in terminal
parser = argparse.ArgumentParser(
    prog='Daily Picture Aligner',
    description = "Automate the eye coordinate alignment process (scaling, rotating, translating) of hundreds of photo to an initial image. ")
arguments = parser.parse_args()

###VARIABLES
DailyPhotoPath = "ALL Daily photos/"
BaseImagePath = "./BaseImages/"
OutputPath = "AlignedPhotos/"

class FileManager: #toDO: find a better classname for the filemanager
    def __init__(self,file):
        self.file 

#there are many different sized dimensions for each images
        #1920x1080 #1
        #3088x2088 #2
        #4032x3216 #3
#we need unique, automatic base images for each. likely from a folder.
#we need to align each of the base images that isn't the smallest (#2, and #3) to base image #1, this is known as ultimate baseImage
#we need to store the values of the exact scaling and x,y coordiantes that was applied to each of base images.
        #this is so when we align each image to it's corresponding base image,
        #we can then perform the SAME translate and scale to all of them. this will minimize any inaccuracies

BaseImageDictionary = {}
for file in os.listdir(Path(BaseImagePath)):
    libfile = PurePath(BaseImagePath+file)
    BaseImage = classes.BaseImage(libfile)
    BaseImageDictionary[BaseImage.cvimage.shape[:2]] = BaseImage #adding new baseimage entry to dictionary. key = shape; value = BaseImageObject 
    # BaseImageDictionary[(1080, 1920)].LeftEyeImageCoordinates[0] #testing
#now that we have our baseimages, we need to make an 'ultimate' one to align all the others to (which is going to be the smallest. should we do it algorithmically or manually?)    
Keys = list(BaseImageDictionary.keys())
Keys.sort()
BaseImageDictionary = {i: BaseImageDictionary[i] for i in Keys} #this is a rough sort that I'm not 100% works the way I think it does.
UltimateBaseImageShape = list(BaseImageDictionary)[0] #if the dictionary above sorted correctly, the first shape will be the dimensions of the smallest image
#now that we have a way to index the actual base image, we need to take all the others and store their translations
for index, (shape,BaseImage) in enumerate(BaseImageDictionary.items()):
    if index == 0:w
        UltimateBaseImage = BaseImageDictionary.get(UltimateBaseImageShape) 
        print(UltimateBaseImage.cvimage.shape)
    else:
        BaseImage.getAlignmentInfo(UltimateBaseImage)

###RUNNING CODE

count = 1

fileList = os.listdir(DailyPhotoPath)
# fileListSorted = fileList.sort(key=lambda x: os.path.getctime(x))
fileListSorted = list(sorted(Path(DailyPhotoPath).iterdir(), key=os.path.getmtime))
#specifically this for loop gets all files and only keeps the ones that are jpg files and aren't curropted or 0 in size.
for file in fileListSorted:
    libfile = file
    file = file.name #Pathlib returns it as a pathlib.WindowsPath instead of a string, and it returns the parent folder like this: parentfolder/file.jpg, so we need to convert it back into a string for the logic ahead using file.name, just the file name as string
    if file in os.listdir(OutputPath): #if our file has already been aligned, do nothing.
        pass
    else:
        #endswith("g") because that's for png/jpg files. I didn't know how to check for the last 4 position slots because each fle name size is different and the initial start is different. anyways this works currently
        if file.endswith("g") and os.path.getsize(DailyPhotoPath + file) > 0 and file != "1871.jpg":
            currentImage = classes.Image(libfile)
            if currentImage.RightEyeImageCoordinates and currentImage.LeftEyeImageCoordinates != None: #if successfully found face in image
                CoorespondingBaseImage = BaseImageDictionary.get(currentImage.cvimage.shape) #each image is aligned to the baseimage with the same dimensions, then we'll take all those aligned images and align them AGAIN based on the baseimage's alignment. this way, even if there are errors in alignment, they'll be the same and look aligned.
                success = currentImage.alignImagetoBaseImage(CoorespondingBaseImage) #1st alignent to baseimage
                success = currentImage.alignImagetoUltimateBaseImage(CoorespondingBaseImage)  #2nd/final alignent to ultimatebaseimage using the correspoinding base image's stats for continuity.        
                if success:
                    cv.imwrite(OutputPath+str(count)+"___"+file+"___ScaleRotateTranslate.jpg",currentImage.cvimage)
                    print("Successfully aligned and wrote to file image: \'" + str(file) +"\' #" + str(count))
                    count += 1
                else:
                    print("passing")
            
            else: 
                print("No face was found for file: " + file)  

        else:
            pass
print("\n~~~~~~~~~~~\nSuccessfully Aligned " + str(count) +" Pictures!")
                
