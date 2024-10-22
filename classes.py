###IMPORTS


import numpy as np
import mediapipe as mp
import cv2 as cv
import traceback
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
face_cascade = cv.CascadeClassifier("C:\CODING\Github\Daily-Picture-Aligner\models\haarcascade_frontalface_default.xml")



ErrorFile = open("ErrorLog.txt","a")
leftEyeLandmark = 468
rightEyeLandmark = 473 
leftNoseCornerLandmark = 49
rightNoseCornerLandmark = 279
topLipLandmark = 0
bottomLipLandmark = 17
rightEyeBrowLandmark = 336
leftEyeBrowLandmark = 107

faceRecognizer = cv.face.LBPHFaceRecognizer_create()
faceRecognizer.read('face_trainer.yml')

class Image:
    # Instead of using facial detection (20 hours to implement)
    # Instead of using selective cropping (10 hours to implement)
    # Instead of using any other fancy method
    # Just slowly expand the image from the center.
    # After coding the last two, this took 10 minutes to implement.
    # Plan before you code, look at all potential solutions.
    def getCorrectFace(self):
        count = 0
        faceNotFound = True
        refineScaleFactor = 1/6
        self.HeightCrop,self.WidthCrop = self.cvimage.shape[:2]
        while faceNotFound:
            if refineScaleFactor > 1: #if it's too large, we can't find the face, so we just return the original image
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



            

       

    def scaleDownImage(self):
          #if it's a landscape image
        if self.Width > self.Height and (self.Height >= 3024 or self.Width >= 4032): #for some reason, if an image is too large, there seems to be some landmakr detection issues, therefore, we scale the image down by 2
            self.Height, self.Width = int(self.cvimage.shape[0]/2),int(self.cvimage.shape[1]/2)
            self.Dimensions = (self.Width, self.Height)  #divide by 2 here, and not above, for some reason, this makes sure it is a INT and not an float!
            Matrix = cv.getRotationMatrix2D( (0,0), 0, 0.5) #leave it at (0,0) it seems to work better for 1 base image alignments. idk why YET
            self.cvimage = cv.warpAffine(self.cvimage, Matrix, self.Dimensions) #warp affine last tuple argument must be floats!!
            self.refreshEyeCoordinates()
            return self.cvimage
    
    #Crops Image down to middle third to target center face  
    def cropImageThirds(self):
        self.cvimageCrop = self.cvimage[int(self.Height/8):int(self.Height/8*7),int(self.Width/3):int(self.Width/3*2)]
        self.HeightCrop,self.WidthCrop = self.cvimageCrop.shape[:2]
        self.cropStatus = 'Thirds'
        return self.cvimageCrop
    
    
    #Crops Image down to Middle Half to target center face  
    def cropImageFourths(self):
        self.cvimageCrop = self.cvimage[int(self.Height/8):int(self.Height/8*7),int(self.Width/4):int(self.Width/4*3)]
        self.HeightCrop,self.WidthCrop = self.cvimageCrop.shape[:2]
        self.cropStatus = 'Thirds'
        return self.cvimageCrop


    def __init__(self,libfile,CorrespondingBaseImage=None):
        self.libfile = libfile
        self.name = libfile.name
        self.cvimage = cv.imread(str(libfile))
        self.closest_face = []
        self.Height, self.Width = self.cvimage.shape[:2]
        self.Dimensions = (self.Width,self.Height)
        self.scaleDownImage()
        # self.cropImageThirds()
        self.getCorrectFace()
        self.HeightCrop, self.WidthCrop = self.cvimage.shape[:2] # Leave this, trust me. unless you wanna dig through the debug to figure out why. 
        self.LeftEyeImageCoordinates = self.getImageCoordinates(leftEyeLandmark)
        self.RightEyeImageCoordinates = self.getImageCoordinates(rightEyeLandmark)
        self.CorrespondingBaseImage = CorrespondingBaseImage if CorrespondingBaseImage is not None else None #straight from stack overflow    
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
            #handling error statements within the alignImagetoBaseImage class
            return ""

    def getImageCoordinates(self,targetlandmark): #converted into a streamlined function for accesiblity. can't speel. spell.
        try:
            self.cropStatus == "None"
        except AttributeError as error:
            self.cropStatus = "None"
        count = 0
        
        #Progressively extends search area through relaxing crops as loop continues if face isn't found.
          #rather- for the new crop method, parse through self.allFaces and search for the one that matches most closesly to self.averageEyeDistance
    
        try:
            #crop the image down first, if you have multiple faces in an image, this will try to limit it only to the face in teh center
            originalImage = self
            with mp_face_mesh.FaceMesh(static_image_mode=True,max_num_faces=1,refine_landmarks=True,min_detection_confidence=0.85) as face_mesh:
                # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
                results = face_mesh.process(cv.cvtColor(self.cvimageCrop, cv.COLOR_BGR2RGB))
                if not results.multi_face_landmarks: #if there are no face landmarks detected it will ignore.
                    count+=1
                # Print and draw face mesh landmarks on image.
                else:
                    annotatedImage = self.cvimageCrop.copy()
                    for face_landmarks in results.multi_face_landmarks:
                        # mp_drawing.draw_landmarks(annotatedImage, face_landmarks, mp_face_mesh.FACE_CONNECTIONS)
                        for id, landmark in enumerate(face_landmarks.landmark):
                            if id == targetlandmark: #this is the point we're targeting: 468 is the left eye, 473 for the right.
                                #We execute the cropping with the get correct face with the index for the x,y,w,h
                                self.currentImageCoordinates = [(landmark.x*self.WidthCrop),(landmark.y*self.HeightCrop),landmark.z]
                                return self.currentImageCoordinates
                            else:
                                pass
                                #don't put a return here, duh. it's looping for specific id.
                        
                        
        except Exception as e:
  
            pass #handling error statements within the alignImagetoBaseImage class
            
 

    def refreshEyeCoordinates(self): #this is needed because after the transformations, the eye locations change! #updated so that it does the transformations with basic math. saves so much computational time.
        try:
            # self.LeftEyeImageCoordinates = self.getImageCoordinates(468) #for the webcam alignment, this is horrendously slow. like 2fps.
            # self.RightEyeImageCoordinates = self.getImageCoordinates(473) #and then to make it worse, we do it again for another eye.
            self.LeftEyex, self.LeftEyey =  self.LeftEyex*self.scaleFactor, self.LeftEyey*self.scaleFactor
            self.RightEyex, self.RightEyey =  self.RightEyex*self.scaleFactor, self.RightEyey*self.scaleFactor
            self.Xdifference = self.RightEyex - self.LeftEyex
        except Exception as error:
            pass #handling errors within the alignImagetoBaseImage class



    def scaleAroundPoint(self, BaseImage): #this function scales the image by a calculated scalefactor to remove and differences in camera distance.
        try:
            self.scaleFactor = (BaseImage.Xdifference/self.Xdifference) #a very simply formula i came up with, wasn't my first iteration, but it works now. I'm saying that like it's complex math, its literally a fraction ratio
                            #x-y coord, rotation angle, scaling factor
                                            #scale from the center of img
            Matrix = cv.getRotationMatrix2D( (0,0) , 0, self.scaleFactor)  #I was looking for a way to scale around an image for so long, it was so simple. scaling from the corner
            self.cvimage = cv.warpAffine(self.cvimage, Matrix, self.Dimensions) #multiplying by 2 to ensure the entire image stays in frame, then on the rotation (the final transfomration) we scale it back down to normal to ensure none of hte image gets cut off!

        except Exception as error:
            pass #handling errors within the alignImagetoBaseImage class

    def translate(self, x, y): #this function simply shifts the image so that the left eye aligns with the base images left eye.
        transMat = np.float32([[1,0,x],[0,1,y]])
        self.LeftEyex += x 
        self.LeftEyey += y
        self.RightEyex += x
        self.RightEyey += y #manually updating them because it'll save some computational time in refreshing the iamges.
        self.cvimage = cv.warpAffine(self.cvimage, transMat, (self.Width,self.Height+400))


    def rotateImage(self,BaseImage): #this function rotates the image so that the slope of the eyes will align with the slope of the base image, if that makes sense. if it doesn't it just makes it better trust me.
        eyePoint = (self.LeftEyex,self.LeftEyey) #consider testing with Baseimage eye coordinates
        angle = np.rad2deg(np.arctan((self.RightEyey-BaseImage.RightEyey)/(self.Xdifference))) #tangent formula right triangle.
        rotationalMatrix = cv.getRotationMatrix2D(eyePoint, angle, 1.0)
        self.cvimage = cv.warpAffine(self.cvimage, rotationalMatrix, (self.Width,self.Height+400) ) #we use the base image's width and height in case there are different sizes, so for base image, use your smallest camera resolution photo. i took some with webcam and my phone for example, if i use my webcame image as base image, my phone will be properly scaled down.
        # finalMatrix = cv.getRotationMatrix2D((0,0) , 0, 1/self.scaleFactor)  #this is the inverse scale factor. THanks Dr. Garner.
        # self.cvimage = cv.warpAffine(self.cvimage, finalMatrix,self.Dimensions) #multiplying by 2 to ensure the entire image stays in frame, then on the rotation (the final transfomration) we scale it back down to normal to ensure none of hte image gets cut off!
        return angle

    def alignImagetoBaseImage(self,BaseImage):   #eyePoint = (BaseImage.LeftEyex,BaseImage.LeftEyey)
        try:
            initialx,initialy = BaseImage.LeftEyex,BaseImage.LeftEyey
            self.scaleAroundPoint(BaseImage)
            self.refreshEyeCoordinates()
            movex = initialx - self.LeftEyex 
            movey = initialy - self.LeftEyey
            self.translate(movex,movey) #consider doing another final translation? cuz translate shoould come last after scaling the image back down but this is just experimental.
            angle = self.rotateImage(BaseImage) # this MUST come last. idk why, but try flipping translate and rotate and see how wonky it gets.
            if self.Dimensions != BaseImage.Dimensions: #this is a check to see if we are have only 1 baseimage, this is the only time this wouldn't be equal if we have 1 base image for differing resolutioned images. it saves us throwing in an extra argument like "1baseimage" boolean, etc.
                self.cvimage = self.cvimage[0:BaseImage.Height+400,0:BaseImage.Width] #crop the image down. or not.
                #IF YOU'RE HAVING FUNKY RESULTS, MAKE SURE YOUR BASE IMAGE MATCHES THE SMALLEST IMAGE RESOLUTIONS OUT OF ALL OTHER 
            #IMAGES IN YOUR FOLDER! 
                pass
            #consider putting a crop if the dimensions are smaller, and not doing anything if the dimensions are larger
            return True


        except Exception as error:
            #MAKE THIS WRITE TO AN ERRORLOG FILE!! i love tqdm's format don't screw that up.
            # errorLength = len(max( traceback.format_exc().split("\n") )) #an idea i gave up on       
            # Line = ''.join(['-' for i in range(errorLength)])
            Line = ''.join(['-' for i in range (28)])
            
            ErrorFile.write("\nAn Error Occurred. File is: \n'" + self.name + "'\nIt is likely that:\n1. No face was found (Face detection may not work on this image, Ensure the face isn't covered and lighting isn't harsh).\n2. A scaling issue occured.\nCheck out the error:\n" +traceback.format_exc() + Line +"\n")
            return False
        
class BaseImage(Image):

    def __init__(self, libfile): #unsure about the use and need for super. #commendting out the __init__ somehow allows the script to still 'work'
        super().__init__(libfile)
        #ultimately, what we need is:     
        self.cropStatus = 'None'   
        self.translateX = None
        self.translateY = None
        self.scaleFactor= None
        self.angle = None
        
      

    def reset(self): #basically calling the __init__ again, similar to making a new instance. this is just for the alignment info function to reset stats.
        self.name = self.libfile.name
        self.cvimage = cv.imread(str(self.libfile))
        self.Height, self.Width = self.cvimage.shape[:2]
        self.Dimensions = (int(self.Width+400),int(self.Height+400))
        self.scaleDownImage()

        #ultimately, what we need is:        
        self.translateX = None
        self.translateY = None
        self.scaleFactor= None
        self.angle = None
        
        self.LeftEyeImageCoordinates = self.getImageCoordinates(leftEyeLandmark)
        self.RightEyeImageCoordinates = self.getImageCoordinates(rightEyeLandmark)
        try:
            # cv.imshow("BaseImage",self.cvimage)
            # cv.waitKey(0)
            # cv.destroyAllWindows()
            # cv.imshow("BaseImageCrop",self.cvimageCrop)
            # cv.waitKey(0)
            # cv.destroyAllWindows()
            self.LeftEyex, self.LeftEyey = self.LeftEyeImageCoordinates[0],self.LeftEyeImageCoordinates[1]
            self.RightEyex, self.RightEyey = self.RightEyeImageCoordinates[0],self.RightEyeImageCoordinates[1]
            self.Ydifference = self.RightEyey - self.LeftEyey
            self.Xdifference = self.RightEyex - self.LeftEyex
        except Exception as error:
            self.Xdifference = None
            self.Ydifference = None
            self.RightEyex = None
            self.LeftEyex = None
            #handling error statements within the alignImagetoBaseImage class
       

    def getAlignmentInfo(self,UltimateBaseImage):   #eyePoint = (BaseImage.LeftEyex,BaseImage.LeftEyey)
        original = self.cvimage #this is because we just want to do a mock alignment to get the info, not a final one, we want to revert it back at the end.
        oldXdifference = self.Xdifference
        self.UltimateBaseImageHeight,self.UltimateBaseImageWidth = UltimateBaseImage.cvimage.shape[:2]
        self.UltimateDimensions = (self.UltimateBaseImageWidth,self.UltimateBaseImageHeight)
        self.UltimatescaleFactor = UltimateBaseImage.Xdifference/self.Xdifference
        self.ExactXdifference = self.Xdifference*self.UltimatescaleFactor
        center = (self.LeftEyex, self.LeftEyey)
        Matrix = cv.getRotationMatrix2D((0,0), 0, self.UltimatescaleFactor)  #I was looking for a way to scale around an image for so long, it was so simple. 
        self.cvimage = cv.warpAffine(self.cvimage, Matrix, UltimateBaseImage.Dimensions) #the final one in warp affine is the image dimensions
        self.UltimatetranslateX = UltimateBaseImage.LeftEyex - self.LeftEyex 
        self.UltimatetranslateY = UltimateBaseImage.LeftEyey - self.LeftEyey

        eyePoint = (self.LeftEyex,self.LeftEyey)
        self.UltimateAngle = np.rad2deg(np.arctan((self.RightEyey-UltimateBaseImage.RightEyey)/(self.ExactXdifference))) #tangent formula right triangle.
                                                                            #I'm trying out ultimate base image as the denominator because it should be teh same?
        self.reset()