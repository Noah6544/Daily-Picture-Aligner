import os
import cv2 as cv
from wand.image import Image


heic_image_path = "C:\\Users\\Noah\'s Marc P. 4648\\Pictures\\DAILY PIC\\Daily photo\\"
final_image_path = "C:\\Users\\Noah\'s Marc P. 4648\\Pictures\\DAILY PIC\\Phone_jpg\\"

count = 0
for file in os.listdir(heic_image_path):
    count +=1
    source_file = heic_image_path + file
    final_file = final_image_path + file.replace(".HEIC", ".jpg")
    with Image(filename=source_file) as original:
        with original.convert('heic') as converted:
        #img.format = 'jpg'
            converted.save(filename=final_file)

    print("Converted " + file + " to JPG successfully!\nConversion #"+str(count))

    break


    #
    # img = Image(filename=source_file)
    # img.format=".jpg"
    # img.save(filename=final_file)
    # img.close()



for file in os.listdir(final_image_path):
    image = cv.imread(file)
    cv.imshow("sadf",image)