#IMPORTS
import cv2
import os

#VARIABLES
path = "C:/Users/User/path to picture/"
refined = []

#RUNNING
##this filters through a folder and finds files that are jpg files and discards those that aren't jpg files.
#specifically this for loop gets all files and only keeps the ones that are jpg files and aren't curropted or 0 in size.
for file in os.listdir(path):
    #endswith("g") because that's for png/jpg files. I didn't know how to check for the last 4 position slots because each file name size is different and the initial start is different. anyways this works currently
    if file.endswith("g") and os.path.getsize(path + file) > 0:
        refined.append(file)
    else:
        pass
#this for loop runs and displays each given picture
for image in refined:
    print(image)
    img = cv2.imread(path + image, 1)
    cv2.imshow("Output",img)
    cv2.waitKey(1000)
    refined.append(image)
