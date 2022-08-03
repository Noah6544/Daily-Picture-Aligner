###IMPORTS
import os
import math
import numpy as np
import time
import mediapipe as mp
import cv2 as cv
import random
###IMPORTS



###VARIABLES
images_path = "C:\\Users\\Noah\'s Marc P. 4648\\Pictures\\DAILY PIC\\"
adjusted_images_path = "C:\\CODING\\Github\\Daily-Picture-Aligner\\adjusted_images\\"
Stabalyzing_point_coordinate_path = "C:\\CODING\\Github\\Daily-Picture-Aligner\\Stabalizing_point_file.txt"
images_list = []
translated_list = []
width, height = 640,360
mp_face_mesh = mp.solutions.face_mesh
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
drawing_spec = mp_drawing.DrawingSpec(thickness=0, circle_radius=1)
left_eye_xy = ""
initialx = .495247483253479
initialy = .5778067111968994


x_ylist = []


def find_left_eye(img):
    global left_eye
    Center_Coordinate_File = open(Stabalyzing_point_coordinate_path, "w")
    with mp_face_mesh.FaceMesh(static_image_mode=True,max_num_faces=1,refine_landmarks=True,min_detection_confidence=0.5) as face_mesh:
        # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
        results = face_mesh.process(cv.cvtColor(img, cv.COLOR_BGR2RGB))

        # Print and draw face mesh landmarks on image.
        if not results.multi_face_landmarks: #if there are no face landmarks detected it will ignore.
            pass

        annotated_image = img.copy()
        for face_landmarks in results.multi_face_landmarks:
            #print("face landmarks:",face_landmarks)


            mp_drawing.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_IRISES,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style())
            face_id_points = []

            for id,landmark in enumerate(face_landmarks.landmark):
                image_height, image_width, image_c = annotated_image.shape
                x,y= int(landmark.x*image_width),int(landmark.y*image_height)
                cv.putText(annotated_image, str(id), (x, y), cv.FONT_HERSHEY_PLAIN, 0.8, (255,255,255), )

                face_id_points.append([x,y])

            print(face_id_points[5])

            Center_Coordinate_File.write(str(face_id_points[1]))

            # draws face/eye box/dots on image
            #image = mp_drawing.draw_detection(annotated_image, detection)
            # shows images on screen.
            cv.imshow("annotated image",annotated_image)
            cv.waitKey(0)
            # stores new annotated image in file path
            #cv2.imwrite(store_image_path + str(idx) + '.png', annotated_image)

            #return left_eye



###PLEASE ASNWER THIS IN THE FUTURE WHY DOES THE CODE FROM ONLINE (TRANSLATE) WORK AND THE ONE I COPIED FROM THE VIDEO DOESN'T!!?!?!
#I COPIED AND PASTED TRANSLATE BUT IT WORKS AND THE ONE I MANUALLY TYPED DOESN"T''T'"!?!?!!!
#I FOUND IT THE NEXT DAY, YO IDIOT, ITS THE 1,0 IN [1,0,Y]

def move_image(img, x, y):
    transMat = np.float32([[1,0,x],[1,0,y]])
    dimensions = (img.shape[1], img.shape[0])
    return cv.warpAffine(img, transMat, dimensions)


def translate(img, x, y):
    transMat = np.float32([[1,0,x],[0,1,y]])
    dimensions = (img.shape[1], img.shape[0])
    return cv.warpAffine(img, transMat, dimensions)

def List_formatting(file):
    global xlist
    global ylist
    xlist = []
    ylist = []
    left_eye_xy = file.read()
    # stripping the list of all extra values (x,y,whitespaaces, colons)    print(left_eye_xy)
    left_eye_xy = left_eye_xy.split("\n")
    if len(left_eye_xy) > 2:
        left_eye_xy.pop(2)
    else:
        pass
    for index, value in enumerate(left_eye_xy):

        if index == 0:
            for idx, char in enumerate(value):
                if idx == 1 or idx == 2 or idx == 0:
                    pass
                else:
                    xlist.append(char)
        elif index == 1:
            for idx, char in enumerate(value):
                if idx == 1 or idx == 2 or idx == 0:
                    pass
                else:
                    ylist.append(char)
            ylist.insert(0, ",")
    x_ylist = xlist + ylist
    ylist = []
    xlist = []
    list_split_index = 0
    # this loop will seperate x_ylist into just the 2 x/y lists we need.
    for inx, char in enumerate(x_ylist):
        if char == ",":
            # a variable that is later used to split the lists, we then append each character depending if it falls
            # bfore or after this variable.
            # if it falls after, its part of the y varible, if before, it is part of the x
            list_split_index = inx
            for indx, char in enumerate(x_ylist):
                if indx > list_split_index:
                    ylist.append(char)
                elif indx < list_split_index:
                    xlist.append(char)
    return xlist, ylist

#this is noah 7 months after dropping this project. its july 1 2022. I think the problem is that I calculated the differences ocmpletely wrong trying to do my own math.
def Find_Difference(ixlist,iylist,xlist,ylist):
    float(ixlist)
    float(iylist)
    float(xlist)
    float(ylist)
    difference_x = (float(xlist) - float(ixlist))
    difference_y = (float(ylist) - float(iylist))
    if difference_x < 0:
        difference_x = abs(difference_x)
    elif difference_x > 0:
        difference_x = difference_x * -1
    if difference_y < 0:
        difference_y = abs(difference_y)
    elif difference_y > 0:
        difference_y = difference_y * -1
    return difference_x, difference_y

# the "i" means initial, the other ones are from the new image.
def Find_Difference_distanceformula(ixlist,iylist,xlist,ylist):
    float(ixlist)
    float(iylist)
    float(xlist)
    float(ylist)
    distance = math.sqrt( ((xlist-ixlist)^2) + ( (ylist-iylist)^2) )
    return distance


#specifically this for loop gets all files and only keeps the ones that are jpg files and aren't curropted or 0 in size.
for file in os.listdir(images_path):
    #endswith("g") because that's for png/jpg files. I didn't know how to check for the last 4 position slots because each file name size is different and the initial start is different. anyways this works currently
    if file.endswith("g") and os.path.getsize(images_path + file) > 0 and file != "1871.jpg":
        images_list.append(images_path + file)
    else:
        pass








for image in images_list:

    print(image)
    Left_eye_mediapipe_file = open(Stabalyzing_point_coordinate_path)
    xlist = []
    ylist = []
    cv2image = cv.imread(image)


    #cv2image = cv.resize(cv2image, (width,height))
    find_left_eye(cv2image)

 #   currnentlist = List_formatting(Left_eye_mediapipe_file)
 #   currentxlist = "".join(currnentlist[0])
 #   currentylist = "".join(currnentlist[1])
 #   image = str(image[48:-4])
 #   print(image)
 #   translated = translate(cv2image, ((Find_Difference(initialx,initialy,currentxlist,currentylist))[0] *1000 ),((Find_Difference(initialx,initialy,currentxlist,currentylist))[1] * 1000))
 #   cv.imwrite(adjusted_images_path + "\\adjusted_facemesh" + image + ".jpg",translated)

    #translated_list.append(translated)
    #cv.imshow("translated",translated)

    #cv.waitKey(.1)



#write the x,y coords to file
#close file
#open file again in read mode and read its contents to a list/str
#delete the "x:" and "y:" and any whitespaces: " "
#split the 2 numbers into a list with different indexes