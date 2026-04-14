import numpy as np
import mediapipe as mp
import cv2 as cv
import traceback
import PIL
from PIL import Image as I

mp_face_mesh = mp.solutions.face_mesh

ErrorFile = open("ErrorLog.txt","a")
leftEyeLandmark = 468
rightEyeLandmark = 473 
leftNoseCornerLandmark = 49
rightNoseCornerLandmark = 279
topLipLandmark = 0
bottomLipLandmark = 17
rightEyeBrowLandmark = 336
leftEyeBrowLandmark = 107

import cv2
import numpy as np
import random


class Image:
    def scaleDownImage(self):
        if self.Width > self.Height and (self.Height >= 3024 or self.Width >= 4032): # If an image is too large, there seems to be some facial detection issues, therefore, we scale the image down by 2
            self.Height, self.Width = int(self.cvimage.shape[0]/2),int(self.cvimage.shape[1]/2)
            self.Dimensions = (self.Width, self.Height)
            Matrix = cv.getRotationMatrix2D( (0,0), 0, .5) 
            self.cvimage = cv.warpAffine(self.cvimage, Matrix, self.Dimensions) 
            return self.cvimage
    
    # Look at increasingly larger sections of the images, starting from the center until you find the face.
    def getCorrectFace(self):
        count = 0
        faceNotFound = True
        refineScaleFactor = 1/6 # Increase this to speed up the process, decrease it to increase accuracy but reduce speed. It is how much we expand the search area by each loop.
        self.HeightCrop,self.WidthCrop = self.cvimage.shape[:2]
        while faceNotFound:
            if refineScaleFactor > 1: 
                refineScaleFactor = 1
            Height,Width = self.cvimage.shape[:2]
            mask = np.zeros(self.cvimage.shape, dtype=np.uint8)
            center_x, center_y = Width // 2, Height // 2
            side_length = int(Height * refineScaleFactor)
            x = center_x - side_length // 2
            y = center_y - side_length // 2
            w = h = side_length
            mask[y:y+h, x:x+w] = self.cvimage[y:y+h, x:x+w]
            self.cvimageCrop = mask

            try:
                tryToGetCoords = self.getImageCoordinates(leftEyeLandmark)[0] #ToDo: find a way to put this under the confidence and maintain the self.cvimageCrop = temp2
                faceNotFound = False
            except Exception as e:
                refineScaleFactor += 1/6
                count+=1
                if count > 10:
                    self.cvimageCrop = self.cvimage
                    faceNotFound = False
                continue           
            
            if count > 10:
                self.cvimageCrop = self.cvimage
                faceNotFound = False
                break



    def __init__(self,libfile,CorrespondingBaseImage=None):
        self.libfile = libfile
        self.name = libfile.name
        self.cvimage = cv.imread(str(libfile))
        self.cvimage = cv.cvtColor(self.cvimage, cv.COLOR_BGR2BGRA) # Transparent background for final output.
        self.failedImages = []
        self.Height, self.Width = self.cvimage.shape[:2]
        self.Dimensions = (self.Width,self.Height)
        self.scaleDownImage()
        self.getCorrectFace()
        self.HeightCrop, self.WidthCrop = self.cvimage.shape[:2] # Leave this, trust me. unless you wanna dig through the debug to figure out why (??). 
        self.LeftEyeImageCoordinates = self.getImageCoordinates(leftEyeLandmark)
        self.RightEyeImageCoordinates = self.getImageCoordinates(rightEyeLandmark)
        self.CorrespondingBaseImage = CorrespondingBaseImage if CorrespondingBaseImage is not None else None
        try:
            self.LeftEyex, self.LeftEyey = self.LeftEyeImageCoordinates[0],self.LeftEyeImageCoordinates[1]
            self.RightEyex, self.RightEyey = self.RightEyeImageCoordinates[0],self.RightEyeImageCoordinates[1]
            self.Ydifference = self.RightEyey - self.LeftEyey
            self.Xdifference = self.RightEyex - self.LeftEyex
        except Exception as error:
            pass

    #For Debugging
    def __str__(self):
        try:
            print("Shape: ", self.cvimage.shape)
            print("XdifferneceNomral = ",self.Xdifference)
            print("LeftEyeImageCoordinates: ",self.LeftEyeImageCoordinates)
            print("RightEyeImageCoordinates: ",self.RightEyeImageCoordinates)
            print("UltimateScalefactor: ",self.UltimatescaleFactor)
            print("UltimateTranslateX: ",self.UltimatetranslateX)
            print("UltimateTranslate Y:",self.UltimatetranslateY)
            print("UltimateAngle: ",self.UltimateAngle)
            return "hey"
        except Exception as error:
            # Handling error in alignImagetoBaseImage.
            return "Error in __str__ method"

    def getImageCoordinates(self,targetlandmark): 
        try:
            self.cropStatus == "None"
        except AttributeError as error:
            self.cropStatus = "None"
        
        
        try:
            with mp_face_mesh.FaceMesh(static_image_mode=True,max_num_faces=10,refine_landmarks=True,min_detection_confidence=0.85) as face_mesh:
                # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
                results = face_mesh.process(cv.cvtColor(self.cvimageCrop, cv.COLOR_BGR2RGB))
                if False: #if there are no face landmarks detected it will ignore.
                    pass
                else:
                    annotatedImage = self.cvimageCrop.copy()
                    for face_landmarks in results.multi_face_landmarks:
                        for id, landmark in enumerate(face_landmarks.landmark):
                            if id == targetlandmark: 
                                self.currentImageCoordinates = [(landmark.x*self.WidthCrop),(landmark.y*self.HeightCrop),landmark.z]
                                return self.currentImageCoordinates
                            else:
                                pass
                        
                        
        except Exception as e:
            pass # Handling error in alignImagetoBaseImage.
            

    def refreshEyeCoordinates(self): 
        try:
            self.LeftEyex, self.LeftEyey =  self.LeftEyex*self.scaleFactor, self.LeftEyey*self.scaleFactor
            self.RightEyex, self.RightEyey =  self.RightEyex*self.scaleFactor, self.RightEyey*self.scaleFactor
            self.Xdifference = self.RightEyex - self.LeftEyex
        except Exception as error:
            pass # Handling error in alignImagetoBaseImage.



    def scaleAroundPoint(self, BaseImage): # Scales the image by a calculated scalefactor to remove and differences in camera distance.
        try:
            self.scaleFactor = (BaseImage.Xdifference/self.Xdifference)
            self.scaleMatrix = cv.getRotationMatrix2D( (0,0) , 0, self.scaleFactor) 
            self.cvimage = cv.warpAffine(self.cvimage, self.scaleMatrix, self.Dimensions,borderMode=cv.BORDER_TRANSPARENT) # Multiplying by 2 to ensure the entire image stays in frame, then on the rotation (the final transform) we scale it back down to normal to ensure none of the image gets cut off
            return self.scaleMatrix

        except Exception as error:
            pass # Handling error in alignImagetoBaseImage.
            

        
    def translate(self, x, y): # Shifts the image by x,y pixels.
        self.transMat = np.float32([[1,0,x],[0,1,y]])
        self.oldEyePoints = (self.LeftEyex,self.LeftEyey)
        self.LeftEyex += x 
        self.LeftEyey += y
        self.RightEyex += x
        self.RightEyey += y 
        self.cvimage = cv.warpAffine(self.cvimage, self.transMat, (self.Width,self.Height),borderMode=cv.BORDER_TRANSPARENT)
        return self.transMat


    def rotateImage(self,BaseImage): # Rotates the image 
        self.eyePoint = (self.LeftEyex,self.LeftEyey) 
        self.angle = np.rad2deg(np.arctan((self.RightEyey-BaseImage.RightEyey)/(self.Xdifference))) # Tangent formula right triangle.
        self.rotationalMatrix = cv.getRotationMatrix2D(self.eyePoint, self.angle, 1.0)
        self.cvimage = cv.warpAffine(self.cvimage, self.rotationalMatrix, (self.Width,self.Height+400),borderMode=cv.BORDER_TRANSPARENT) # Uses the BaseImage's width and height in case there are different sizes, so for base image, use your smallest camera resolution photo. 
        return self.rotationalMatrix

    def alignImagetoBaseImage(self,BaseImage):  
        try:
            initialx,initialy = BaseImage.LeftEyex,BaseImage.LeftEyey
            self.scaleAroundPoint(BaseImage)
            self.refreshEyeCoordinates()
            movex = initialx - self.LeftEyex
            movey = initialy - self.LeftEyey
            self.translate(movex,movey) 
            self.rotateImage(BaseImage) # MUST come last.
            if self.Dimensions != BaseImage.Dimensions: #this is a check to see if we have only 1 baseimage, this is the only time this wouldn't be equal if we have 1 base image for differing resolution images. it saves us throwing in an extra argument like "1baseimage" boolean, etc.
                self.cvimage = self.cvimage[0:BaseImage.Height+400,0:BaseImage.Width] # This replaces the scaledownFunction.
                #If you're having funky results, make sure your BaseImage matches the smallest image resolutions of all other images in your folder. 
                pass
            
            return True


        except Exception as error:
            Line = ''.join(['-' for i in range (28)])
            ErrorFile.write("\nAn Error Occurred. File is: \n'" + self.name + "'\nIt is likely that:\n1. No face was found (Face detection may not work on this image, Ensure the face isn't covered and lighting isn't harsh).\n2. A scaling issue occured. \n3. Try again, or delete the image to keep going. \nCheck out the error:\n" +traceback.format_exc() + Line + str(error) +"\n")
            return self.name
        
        
class BaseImage(Image):
     
    def __init__(self, libfile):
        super().__init__(libfile)
        self.cropStatus = 'None'   
        self.translateX = None
        self.translateY = None
        self.scaleFactor= None
        self.angle = None
        
      

    def reset(self): # Essentially calling __init__ again, similar to making a new instance.
        self.name = self.libfile.name
        self.cvimage = cv.imread(str(self.libfile))
        self.Height, self.Width = self.cvimage.shape[:2]
        self.Dimensions = (int(self.Width),int(self.Height))
        self.translateX = None
        self.translateY = None
        self.scaleFactor= None
        self.angle = None
        
        self.LeftEyeImageCoordinates = self.getImageCoordinates(leftEyeLandmark)
        self.RightEyeImageCoordinates = self.getImageCoordinates(rightEyeLandmark)
        try:
            self.LeftEyex, self.LeftEyey = self.LeftEyeImageCoordinates[0],self.LeftEyeImageCoordinates[1]
            self.RightEyex, self.RightEyey = self.RightEyeImageCoordinates[0],self.RightEyeImageCoordinates[1]
            self.Ydifference = self.RightEyey - self.LeftEyey
            self.Xdifference = self.RightEyex - self.LeftEyex
        except Exception as error:
            self.Xdifference = None
            self.Ydifference = None
            self.RightEyex = None
            self.LeftEyex = None
            # Handling error in alignImagetoBaseImage.
       

    def getAlignmentInfo(self,UltimateBaseImage): 
        self.UltimateBaseImageHeight,self.UltimateBaseImageWidth = UltimateBaseImage.cvimage.shape[:2]
        self.UltimateDimensions = (self.UltimateBaseImageWidth,self.UltimateBaseImageHeight)
        self.UltimatescaleFactor = UltimateBaseImage.Xdifference/self.Xdifference
        self.ExactXdifference = self.Xdifference*self.UltimatescaleFactor
        Matrix = cv.getRotationMatrix2D((0,0), 0, self.UltimatescaleFactor)  
        self.cvimage = cv.warpAffine(self.cvimage, Matrix, UltimateBaseImage.Dimensions) 
        self.UltimatetranslateX = UltimateBaseImage.LeftEyex - self.LeftEyex 
        self.UltimatetranslateY = UltimateBaseImage.LeftEyey - self.LeftEyey
        self.UltimateAngle = np.rad2deg(np.arctan((self.RightEyey-UltimateBaseImage.RightEyey)/(self.ExactXdifference))) # Tangent formula right triangle.
        self.reset()