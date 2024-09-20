import os
import pathlib
import sys
import numpy as np
import mediapipe as mp
import cv2 as cv
from pathlib import *
import argparse
import classes 
import time
from tqdm import tqdm, trange

parser = argparse.ArgumentParser(
    prog='Daily Picture Aligner',
    description = "Automate the eye coordinate alignment process (scaling, rotating, translating) of hundreds of photo to an initial image. ")
parser.add_argument('--photos', default='./DailyPhotos/')
parser.add_argument('--output', default='./AlignedPhotos/')
parser.add_argument('--baseimage', default='./BaseImages/')
parser.add_argument('-c', '--confidence', default=0.2, help='Confidence level for detecting faces (0.0 - 1.0')
parser.add_argument('-s', '--skip-existing', action='store_true', help='Skip already aligned images in output folder')
parser.add_argument('-b', '--add-blur', action='store_true', help='Adds a background blur to empty areas')
args = parser.parse_args()

### VARIABLES ###
OUT_EXT = ".png" # using png as it's a common lossless format with transparency
IMAGE_EXT = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']
#################

class FileManager: # TODO: find a better classname for the filemanager
    def __init__(self,file):
        self.file 

files = os.listdir(Path(args.baseimage))
files = list(filter(lambda a: not a.startswith("."), files))

if len(files) > 1:
    raise Exception("Ensure there's only one base image, and that you deleted the initial text file.")

file = files[0]

lib_file = PurePath(args.baseimage + file)
base_image = classes.BaseImage(lib_file)

print("\n-------------------------------")
print("Starting Script\nAdjusting Images\nWriting Files")
print("Check 'AlignedPhotos' folder and make sure the script is working")
print("Check ErrorLog.txt if output isn't working as expected!")
print("-------------------------------\n")

time.sleep(2)
count = 1
fileList = os.listdir(args.photos)
file_list_sorted = list(sorted(Path(args.photos).iterdir(), key=os.path.getctime))

for file in tqdm(file_list_sorted):
    # Get various parts of the filename
    file_path = str(file)
    full_filename = file.name
    file_ext = pathlib.Path(file_path).suffix
    filename = pathlib.Path(file_path).stem

    # Skip file if skip-existing flag is set and the image has already been aligned
    if args.skip_existing and filename+OUT_EXT in os.listdir(args.output):
        pass

    # Skip file if its size is 0
    if file_ext in IMAGE_EXT and os.path.getsize(file_path) == 0:
        pass

    current_image = classes.Image(file, confidence=args.confidence)
    success = current_image.align_image_to_base_image(base_image)
    if not success:
        pass

    if args.add_blur:
        current_image.add_blur(file_path)

    cv.imwrite(str(args.output) + filename + OUT_EXT, current_image.cvimage)
    count+=1


print("\nSuccessfully Aligned " + str(count) +" Pictures!")
print("If you found this script useful, please let me know, I would love your feedback!")
print("If you want to directly support my future (college, projects, etc.), "
      "my CashApp is $NoahCutz, or you can BuyMeACoffee (https://buymeacoffee.com/noahbuchanan).")

