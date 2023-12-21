import cv2 as cv
from pathlib import *
import os
from tqdm import tqdm, trange


path = str(Path(input("Enter path to folder with images: "))) + "/"
print("\n\n\n\n",path,"\n\n\n\n")
waitKey = int(input(("Enter waitkey: ")))


while True:
	for file in tqdm(os.listdir(path)):
		img = cv.imread(str(path)+file)
		height, width = img.shape[0],img.shape[1]
		factor = 1 - width/1920
		if factor == 0:
			factor = 1
		img = cv.resize(img,  (int(width*factor),int(height*factor)) )
		cv.imshow("Display ", img)
		cv.waitKey(waitKey)