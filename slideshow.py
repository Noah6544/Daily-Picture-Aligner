import cv2 as cv
from pathlib import *
import os
from tqdm import tqdm


path = str(Path(input("Enter path to folder with images: "))) + "/"
waitKey = int(input(("Enter waitkey: ")))

fileListSorted = list(sorted(Path(path).iterdir(), key=os.path.getctime))

if "DELETETHIS.txt" in [file.name for file in fileListSorted]:
    raise Exception("Delete the 'DELETETHIS.txt' file!")

while True:
	for file in tqdm(fileListSorted):
		img = cv.imread(str(file))
		height, width = img.shape[0],img.shape[1]
		factor = width/1920
		if factor == 0:
			factor = 1

		print(width*factor)
		aspect_ratio = width / height
		new_width = 1280
		new_height = int(new_width / aspect_ratio)
		img2 = cv.resize(img, (new_width, new_height))
		cv.imshow("Display ", img2)
		cv.waitKey(waitKey)