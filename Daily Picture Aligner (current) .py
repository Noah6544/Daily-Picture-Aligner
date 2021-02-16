#IMPORTS
import cv2
import os
import glob

#VARIABLES
path = "C:\\Users\\USER\\Pictures\\"
pictures = []

#CREATING LIST OF PICTURES (doesn't need to be run after the initial writing
# creates a list from all files that end in jpg in the directory and that are bigger that 0 because 0 file size means
# that the file is curropted and will break the opencv2 thing

for file in glob.glob(path + "*.jpg"):
    if os.path.getsize(file) > 0:
        pictures.append(file)
    else:
        pass

"""
#sorts files based on the time that they are created
rawlist.sort(key=os.path.getmtime)
#writes list to file, this is because the time to recreate the list every execution is repetitive and computationally
#expensive.
#however that will need to be done if new files are added to the list.
with open("refined.txt", "w") as refinedtxt:
    txtlines = "\n".join(rawlist)
    refinedtxt.write(txtlines)
"""

#reading the previously writted text file as a str that can be written back into a list

refinedtxt = open("refined.txt","r")
txtlines = refinedtxt.read()
pictures = txtlines.split("\n")

#this for loop runs and displays each given picture
for image in pictures:
    img = cv2.imread(image)
    cv2.imshow("Output",img)
    cv2.waitKey(1)
