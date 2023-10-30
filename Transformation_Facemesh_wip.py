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
daily_photo_path = "Daily Photo Converted\\"

adjusted_images_path = "adjusted images\\"

adjusted_images_path_aroundpoint = "adjusted images aroundpoint\\"

adjusted_images_path_aroundpoint_translatefirst = "adjusted images aroundpoint translatefirst\\"


rotatedimagepath = "rotatedimages\\"




adjusted_images_path_noscale = "adjusted images no scale\\"

mp_face_mesh = mp.solutions.face_mesh
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
drawing_spec = mp_drawing.DrawingSpec(thickness=0, circle_radius=1)

class Image:
    def __init__(self,cvimage):
        self.cvimage = cvimage
        self.Height, self.Width = self.cvimage.shape[:2]
        self.LeftEyeImageCoordinates = self.getImageCoordinates(468)
        self.RightEyeImageCoordinates = self.getImageCoordinates(473)
        self.LeftEyex, self.LeftEyey = self.LeftEyeImageCoordinates[0],self.LeftEyeImageCoordinates[1]
        self.RightEyex, self.RightEyey = self.RightEyeImageCoordinates[0],self.RightEyeImageCoordinates[1]
        self.Ydifference = self.RightEyey - self.LeftEyey
        self.Xdifference = self.RightEyex - self.LeftEyex


    def getImageCoordinates(self,targetlandmark): #converted into a streamlined function for accesiblity. can't speel. spell.
        with mp_face_mesh.FaceMesh(static_image_mode=True,max_num_faces=1,refine_landmarks=True,min_detection_confidence=0.5) as face_mesh:
            # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
            results = face_mesh.process(cv.cvtColor(self.cvimage, cv.COLOR_BGR2RGB))
            if not results.multi_face_landmarks: #if there are no face landmarks detected it will ignore.
                print('no faces')
                return None
            # Print and draw face mesh landmarks on image.
            for face_landmarks in results.multi_face_landmarks:     
                face_id_points = []
                for id, landmark in enumerate(face_landmarks.landmark):
                    if id == targetlandmark: #this is the point I'm targeting: 468 is the left eye, 473 for the right looks great.
                        self.currentImageCoordinates = [int(landmark.x*self.Width),int(landmark.y*self.Height),landmark.z]
                        return self.currentImageCoordinates
                    else:
                        pass

    def refreshEyeCoordinates(self): #this is needed because after the transformations, the eye locations change!
        self.LeftEyeImageCoordinates = self.getImageCoordinates(468)
        self.RightEyeImageCoordinates = self.getImageCoordinates(473)
        self.LeftEyex, self.LeftEyey = self.LeftEyeImageCoordinates[0],self.LeftEyeImageCoordinates[1]
        self.RightEyex, self.RightEyey = self.RightEyeImageCoordinates[0],self.RightEyeImageCoordinates[1]



    def scale_around_point(self, BaseImage): #this function scales the image by a calculated scalefactor to remove and differences in camera distance.

        point = (BaseImage.LeftEyex,BaseImage.LeftEyey) 
        scaleFactor = (BaseImage.Xdifference/self.Xdifference) #a very simply formula i came up with, wasn't my first iteration, but it works now. I'm saying that like it's complex math, its literally a fraction ratio
        center = (self.Width , self.Height)
                         #x-y coord, rotation angle, scaling factor
        Matrix = cv.getRotationMatrix2D(center, 0, scaleFactor) #I was looking for a way to scale around an image for so long, it was so simple. 
        self.cvimage = cv.warpAffine(self.cvimage, Matrix, (self.Width, self.Height))

    def translate(self, x, y): #this function simply shifts the image so that the left eye aligns with the base images left eye.
        transMat = np.float32([[1,0,x],[0,1,y]])
        dimensions = (self.cvimage.shape[1], self.cvimage.shape[0])
        self.cvimage = cv.warpAffine(self.cvimage, transMat, dimensions)


    def rotate_image(self,BaseImage): #this function rotates the image so that the slope of the eyes will align with the slope of the base image, if that makes sense. if it doesn't it just makes it better trust me.
        angle = np.rad2deg(np.arctan((self.RightEyey-BaseImage.RightEyey)/(self.Xdifference)))
        rot_mat = cv.getRotationMatrix2D((BaseImage.LeftEyex,BaseImage.LeftEyey), angle, 1.0)
        self.cvimage = cv.warpAffine(self.cvimage, rot_mat, self.cvimage.shape[1::-1], flags=cv.INTER_LINEAR)


 
#ToDo: implement a cool "drawing with your eyes." kinda thing

    def getStats(baseimage):
 
        return ([LeftEyex,LeftEyey],[RightEyex,RightEyey],[Xdifference,Ydifference])
      

    
###RUNNING CODE

print("made it here")
BaseImage = Image(cv.imread("baseimage.jpg"))
count = 1

landmarkNumber = 468
#specifically this for loop gets all files and only keeps the ones that are jpg files and aren't curropted or 0 in size.
for file in os.listdir(daily_photo_path):
    if file in os.listdir(adjusted_images_path):
        pass
    else:
        #endswith("g") because that's for png/jpg files. I didn't know how to check for the last 4 position slots because each fle name size is different and the initial start is different. anyways this works currently
        if file.endswith("g") and os.path.getsize(daily_photo_path + file) > 0 and file != "1871.jpg":
            currentImage = Image(cv.imread(daily_photo_path + file))
            # #cv2image = cv.resze(cv2image, (width,height))
            # LeftEyeImageCoordinates = getImageCoordinates(cvimage,468)
            # RightEyeImageCoordinates = getImageCoordinates(cvimage,473)
            if currentImage.RightEyeImageCoordinates and currentImage.LeftEyeImageCoordinates != None: #if successfullyfound image
                # LeftEyex, LeftEyey = LeftEyeImageCoordinates[0],LeftEyeImageCoordinates[1]
                # RightEyex, RightEyey = RightEyeImageCoordinates[0],RightEyeImageCoordinates[1]

                if landmarkNumber == 468: #if we want the left eye
                    
                    # initialx,initialy = .45*cvimage.shape[1],.5*cvimage.shape[0] #those are % alues of where i want theleft eye to be. about 45% over to the left and 60% up on the sreen.

                    initialx,initialy = BaseImage.LeftEyex,BaseImage.LeftEyey
                    currentImage.scale_around_point(BaseImage)
                    currentImage.refreshEyeCoordinates()
                    movex = initialx - currentImage.LeftEyex 
                    movey = initialy - currentImage.LeftEyey
                    currentImage.translate(movex,movey)
                    currentImage.refreshEyeCoordinates()
                    currentImage.rotate_image(BaseImage)
                elif landmarkNumber == 473: #if we want to SHIFT to the right eye
                    initialx, initiay = BaseImageStats[1][0],BaseImageStats[1][1] #.5 and .34 are arbitary numbers i picked.
                    move = initialx - Rightyex 
                    movey = initialy - RightEyey  
                    finalimage = translate(cvimage,movex,movey)


                # cv.imshow("Newly Aligned Image",finalimage)
                # cv.waitKey(100)               added_imag = v2.addWeihted(baseimage,0.4,finalimage,0.1,0)
                
                cv.imwrite(rotatedimagepath+file+"_adjustedandscaled.jpg",currentImage.cvimage)
                print("Successfully aligned and wrote to file image: \'" + str(file) +"\' #" + str(count))
                count += 1
            
            else: 
                print("No face was found for file: " + file)    
        else:
            pass

                
