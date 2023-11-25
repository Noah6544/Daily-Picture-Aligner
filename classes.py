###IMPORTS
import numpy as np
import mediapipe as mp
import cv2 as cv

mp_face_mesh = mp.solutions.face_mesh
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
drawing_spec = mp_drawing.DrawingSpec(thickness=0, circle_radius=1)

class Image:
    def __init__(self,libfile,CorrespondingBaseImage=None):
        self.name = libfile.name
        self.cvimage = cv.imread(str(libfile))
        self.Height, self.Width = self.cvimage.shape[:2]
        self.LeftEyeImageCoordinates = self.getImageCoordinates(468)
        self.RightEyeImageCoordinates = self.getImageCoordinates(473)
        self.CorrespondingBaseImage = CorrespondingBaseImage if CorrespondingBaseImage is not None else None #straight from stack overflow    
        try:
            self.LeftEyex, self.LeftEyey = self.LeftEyeImageCoordinates[0],self.LeftEyeImageCoordinates[1]
            self.RightEyex, self.RightEyey = self.RightEyeImageCoordinates[0],self.RightEyeImageCoordinates[1]
            self.Ydifference = self.RightEyey - self.LeftEyey
            self.Xdifference = self.RightEyex - self.LeftEyex
        except Exception as error:
            print("Error solving for eyes.")
            print(error)


    def getImageCoordinates(self,targetlandmark): #converted into a streamlined function for accesiblity. can't speel. spell.
        try:
            with mp_face_mesh.FaceMesh(static_image_mode=True,max_num_faces=10,refine_landmarks=True,min_detection_confidence=0.8) as face_mesh:
                # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
                results = face_mesh.process(cv.cvtColor(self.cvimage, cv.COLOR_BGR2RGB))
                # print(getattr(results))
                # raise NameError
                if not results.multi_face_landmarks: #if there are no face landmarks detected it will ignore.
                    return None
                # Print and draw face mesh landmarks on image.
                for face_landmarks in results.multi_face_landmarks:     
                    face_id_points = []
                    for id, landmark in enumerate(face_landmarks.landmark):
                        if id == targetlandmark: #this is the point I'm targeting: 468 is the left eye, 473 for the right looks great.
                            self.currentImageCoordinates = [landmark.x*self.Width,landmark.y*self.Height,landmark.z]
                            return self.currentImageCoordinates
                        else:
                            pass
        except Exception as error:
            print("No Faces Found!")
            print(error)


    def refreshEyeCoordinates(self): #this is needed because after the transformations, the eye locations change!
        self.LeftEyeImageCoordinates = self.getImageCoordinates(468) #for the webcam alignment, this is horrendously slow. like 2fps.
        self.RightEyeImageCoordinates = self.getImageCoordinates(473) #and then to make it worse, we do it again for another eye.
        self.LeftEyex, self.LeftEyey = self.LeftEyeImageCoordinates[0],self.LeftEyeImageCoordinates[1]
        self.RightEyex, self.RightEyey = self.RightEyeImageCoordinates[0],self.RightEyeImageCoordinates[1]
        self.Xdifference = self.RightEyex - self.LeftEyex


    def scaleAroundPoint(self, BaseImage): #this function scales the image by a calculated scalefactor to remove and differences in camera distance.
        scaleFactor = (BaseImage.Xdifference/self.Xdifference) #a very simply formula i came up with, wasn't my first iteration, but it works now. I'm saying that like it's complex math, its literally a fraction ratio
        center = (self.Width , self.Height)
                        #x-y coord, rotation angle, scaling factor
        Matrix = cv.getRotationMatrix2D(center, 0, scaleFactor)  #I was looking for a way to scale around an image for so long, it was so simple. scaling from the corner
        self.cvimage = cv.warpAffine(self.cvimage, Matrix,center)


    def translate(self, x, y): #this function simply shifts the image so that the left eye aligns with the base images left eye.
        transMat = np.float32([[1,0,x],[0,1,y]])
        dimensions = (self.Width, self.Height)
        self.LeftEyex += x 
        self.LeftEyey += y
        self.RightEyex += x
        self.RightEyey += y #manually updating them because it'll save some computational time in refreshing the iamges.
        self.cvimage = cv.warpAffine(self.cvimage, transMat, dimensions)


    def rotateImage(self,BaseImage): #this function rotates the image so that the slope of the eyes will align with the slope of the base image, if that makes sense. if it doesn't it just makes it better trust me.
        eyePoint = (self.LeftEyex,self.LeftEyey) #consider testing with Baseimage eye coordinates
        print("RightEyey: " +str(self.RightEyey))
        print("Baseimagerighteyey: "+ str(BaseImage.RightEyey))
        angle = np.rad2deg(np.arctan((self.RightEyey-BaseImage.RightEyey)/(self.Xdifference))) #tangent formula right triangle.
        rotationalMatrix = cv.getRotationMatrix2D(eyePoint, angle, 1.0)
        self.cvimage = cv.warpAffine(self.cvimage, rotationalMatrix, (BaseImage.Width,BaseImage.Height)) #we use the base image's width and height in case there are different sizes, so for base image, use your smallest camera resolution photo. i took some with webcam and my phone for example, if i use my webcame image as base image, my phone will be properly scaled down.


    def alignImagetoBaseImage(self,BaseImage):   #eyePoint = (BaseImage.LeftEyex,BaseImage.LeftEyey)
        try:
            initialx,initialy = BaseImage.LeftEyex,BaseImage.LeftEyey
            self.scaleAroundPoint(BaseImage)
            self.refreshEyeCoordinates()
            movex = initialx - self.LeftEyex 
            movey = initialy - self.LeftEyey
            self.translate(movex,movey) 
            self.rotateImage(BaseImage) # this MUST come last. idk why, but try flipping translate and rotate and see how wonky it gets.
            return True
        except Exception as error:
            print("An Error Occured!! File is: " + self.name + "\nIt is likely that:\n1. No face was found\n2. A scaling issue occured.\nCheck out the error:\n~~~~~~~~\n" + str(error) + "\n~~~~~~")
            return False
        
        
    def alignImagetoUltimateBaseImage(self,BaseImage):
        try: #using manual instead of functions for better control? and making more functions might be redundant? idk. polish later
            #SCALING
            center = (self.Width,self.Height)
            scaleMatrix = cv.getRotationMatrix2D(center,0,BaseImage.scaleFactor)
            self.cvimage = cv.warpAffine(self.cvimage, scaleMatrix, center)
            #TRANSLATING
            self.translate(BaseImage.translateX,BaseImage.translateY)
            #ROTATING
            eyePoint = (BaseImage.LeftEyex,BaseImage.LeftEyey)
            rotationalMatrix = (eyePoint,BaseImage.angle,1.0)
            self.cvimage = cv.warmAffine(self.cvimage,rotationalMatrix,(self.Width,self.Height))
            return True           
        except Exception as error:
            print("ERROR! so close yet so far. file is: " + self.name + "Error is: \n" + str(error))


class BaseImage(Image):
    def __init__(self, libfile): #unsure about the use and need for super. consult old spaceship game with classes.
        self.name = libfile.name
        self.cvimage = cv.imread(str(libfile))
        cv.imshow("asfd",self.cvimage)
        cv.waitKey(10000)
        self.Height, self.Width = self.cvimage.shape[:2]
        #ultimately, what we need is:
        
        self.translateX = None
        self.translateY = None
        self.scaleFactor= None
        self.angle = None
        
        self.LeftEyeImageCoordinates = self.getImageCoordinates(468)
        self.RightEyeImageCoordinates = self.getImageCoordinates(473)
        try:
            self.LeftEyex, self.LeftEyey = self.LeftEyeImageCoordinates[0],self.LeftEyeImageCoordinates[1]
            self.RightEyex, self.RightEyey = self.RightEyeImageCoordinates[0],self.RightEyeImageCoordinates[1]
            self.Ydifference = self.RightEyey - self.LeftEyey
            self.Xdifference = self.RightEyex - self.LeftEyex
        except Exception as error:
            print("Error solving for eyes.")
            print(error)
       

        
    def getAlignmentInfo(self,UltimateBaseImage):   #eyePoint = (BaseImage.LeftEyex,BaseImage.LeftEyey)

        self.scaleFactor = (UltimateBaseImage.Xdifference/self.Xdifference) 
        center = (self.Width , self.Height)
        Matrix = cv.getRotationMatrix2D(center, 0, self.scaleFactor)  #I was looking for a way to scale around an image for so long, it was so simple. 
        self.cvimage = cv.warpAffine(self.cvimage, Matrix, (self.Width, self.Height))
        self.refreshEyeCoordinates()
        self.translateX = UltimateBaseImage.LeftEyex - self.LeftEyex 
        self.translateY = UltimateBaseImage.LeftEyey - self.LeftEyey
        self.eyePoint = (self.LeftEyex,self.LeftEyey)
        self.angle = np.rad2deg(np.arctan((self.RightEyey-UltimateBaseImage.RightEyey)/(self.Xdifference))) #tangent formula right triangle.

        

