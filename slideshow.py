import cv2 as cv
from pathlib import *
import os
from tqdm import tqdm, trange



path = str(Path(input("Enter path to folder with images: "))) + "/"
waitKey = int(input(("Enter waitkey: ")))

fileListSorted = list(sorted(Path(path).iterdir(), key=os.path.getctime))

if "DELETETHIS.txt" in [file.name for file in fileListSorted]: #i love list comprehensions.
    raise Exception("Delete the 'DELETETHIS.txt' file!")

while True:
	for file in tqdm(fileListSorted):
		img = cv.imread(str(file))
		height, width = img.shape[0],img.shape[1]
		factor = 1 - width/1920
		if factor == 0:
			factor = 1
		img = cv.resize(img, (int(width*factor),int(height*factor)) )
		cv.imshow("Display ", img)
		cv.waitKey(waitKey)