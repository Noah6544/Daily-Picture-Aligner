###IMPORTS
import numpy as np
import mediapipe as mp
import cv2 as cv
import traceback

mp_face_mesh = mp.solutions.face_mesh
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
drawing_spec = mp_drawing.DrawingSpec(thickness=0, circle_radius=1)

ErrorFile = open("ErrorLog.txt","a")

leftLandmark = 468#468 is left eye
rightLandmark = 473 #473 is right eye

class Image:
    def scaleDownImage(self):
          #if it's a landscape image
        if self.Width > self.Height and (self.Height >= 3024 or self.Width >= 4032): #for some reason, if an image is too large, there seems to be some landmakr detection issues, therefore, we scale the image down by 2

            self.Height, self.Width = int(self.cvimage.shape[0]/2),int(self.cvimage.shape[1]/2)
            self.Dimensions = (self.Width, self.Height)  #divide by 2 here, and not above, for some reason, this makes sure it is a INT and not an float!
            Matrix = cv.getRotationMatrix2D( (0,0), 0, 0.5) #leave it at (0,0) it seems to work better for 1 base image alignments. idk why YET
            self.cvimage = cv.warpAffine(self.cvimage, Matrix, self.Dimensions) #warp affine last tuple argument must be floats!!
            self.refreshEyeCoordinates()
            return self.cvimage


    def __init__(self,libfile,CorrespondingBaseImage=None):
        self.libfile = libfile
        self.name = libfile.name
        self.cvimage = cv.imread(str(libfile))
        self.Height, self.Width = self.cvimage.shape[:2]
        self.Dimensions = (self.Width,self.Height)
        # self.EnglargedDimensions = (int(self.Width*1.05),int(self.Width*1.05)) #this was meant to account for the fact the image might be cropped when transforming, but it's not working. considering bringing back later.
        self.scaleDownImage()
        self.LeftEyeImageCoordinates = self.getImageCoordinates(leftLandmark)
        self.RightEyeImageCoordinates = self.getImageCoordinates(rightLandmark)
        self.CorrespondingBaseImage = CorrespondingBaseImage if CorrespondingBaseImage is not None else None #straight from stack overflow    
        try:
            self.LeftEyex, self.LeftEyey = self.LeftEyeImageCoordinates[0],self.LeftEyeImageCoordinates[1]
            self.RightEyex, self.RightEyey = self.RightEyeImageCoordinates[0],self.RightEyeImageCoordinates[1]
            self.Ydifference = self.RightEyey - self.LeftEyey
            self.Xdifference = self.RightEyex - self.LeftEyex
        except Exception as error:
            pass

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

    def getImageCoordinates(self,targetlandmark): #converted into a streamlined function for accessibility. can't speel. spell.
        try:
            with mp_face_mesh.FaceMesh(static_image_mode=True,max_num_faces=10,refine_landmarks=True,min_detection_confidence=0.85) as face_mesh:
                # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
                results = face_mesh.process(cv.cvtColor(self.cvimage, cv.COLOR_BGR2RGB))
                if not results.multi_face_landmarks: #if there are no face landmarks detected it will ignore.
                    return None
                # Print and draw face mesh landmarks on image.
                for face_landmarks in results.multi_face_landmarks:     
                    for id, landmark in enumerate(face_landmarks.landmark):
                        if id == targetlandmark: #this is the point I'm targeting: 468 is the left eye, 473 for the right looks great.
                            self.currentImageCoordinates = [landmark.x*self.Width,landmark.y*self.Height,landmark.z]
                            if self.currentImageCoordinates == None:
                                raise error
                            return self.currentImageCoordinates
                        else:
                            pass
                            #don't put a return here, duh. it's looping for specific id.
        except Exception as error:
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
            self.cvimage = cv.warpAffine(self.cvimage, Matrix, self.Dimensions) #multiplying by 2 to ensure the entire image stays in frame, then on the rotation (the final transfomration) we scale it back down to normal to ensure none of the image gets cut off!

        except Exception as error:
            pass #handling errors within the alignImagetoBaseImage class

    def translate(self, x, y): #this function simply shifts the image so that the left eye aligns with the base images left eye.
        transMat = np.float32([[1,0,x],[0,1,y]])
        self.LeftEyex += x 
        self.LeftEyey += y
        self.RightEyex += x
        self.RightEyey += y #manually updating them because it'll save some computational time in refreshing the images.
        self.cvimage = cv.warpAffine(self.cvimage, transMat, self.Dimensions)


    def rotateImage(self,BaseImage): #this function rotates the image so that the slope of the eyes will align with the slope of the base image, if that makes sense. if it doesn't it just makes it better trust me.
        eyePoint = (self.LeftEyex,self.LeftEyey) #consider testing with Baseimage eye coordinates
        angle = np.rad2deg(np.arctan((self.RightEyey-BaseImage.RightEyey)/(self.Xdifference))) #tangent formula right triangle.
        rotationalMatrix = cv.getRotationMatrix2D(eyePoint, angle, 1.0)
        self.cvimage = cv.warpAffine(self.cvimage, rotationalMatrix, self.Dimensions ) #we use the base image's width and height in case there are different sizes, so for base image, use your smallest camera resolution photo. i took some with webcam and my phone for example, if i use my webcame image as base image, my phone will be properly scaled down.
        # finalMatrix = cv.getRotationMatrix2D((0,0) , 0, 1/self.scaleFactor)  #this is the inverse scale factor. THanks Dr. Garner.
        # self.cvimage = cv.warpAffine(self.cvimage, finalMatrix,self.Dimensions) #multiplying by 2 to ensure the entire image stays in frame, then on the rotation (the final transfomration) we scale it back down to normal to ensure none of the image gets cut off!
        return angle

    def alignImagetoBaseImage(self,BaseImage):   #eyePoint = (BaseImage.LeftEyex,BaseImage.LeftEyey)
        try:
            initialx,initially = BaseImage.LeftEyex,BaseImage.LeftEyey
            self.scaleAroundPoint(BaseImage)
            self.refreshEyeCoordinates()
            movex = initialx - self.LeftEyex 
            movey = initially - self.LeftEyey
            self.translate(movex,movey) #consider doing another final translation? cuz translate should come last after scaling the image back down but this is just experimental.
            angle = self.rotateImage(BaseImage) # this MUST come last. idk why, but try flipping translate and rotate and see how wonky it gets.
            if self.Dimensions != BaseImage.Dimensions: #this is a check to see if we are have only 1 baseimage, this is the only time this wouldn't be equal if we have 1 base image for differing resolutioned images. it saves us throwing in an extra argument like "1baseimage" boolean, etc.
                self.cvimage = self.cvimage[0:BaseImage.Height,0:BaseImage.Width] #crop the image down. or not.
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
            
            ErrorFile.write("\nAn Error Occurred. File is: \n'" + self.name + "'\nIt is likely that:\n1. No face was found\n2. A scaling issue occurred.\nCheck out the error:\n" +traceback.format_exc() + Line +"\n")
            return False
        
class BaseImage(Image):
    def __init__(self, libfile): #unsure about the use and need for super. consult old spaceship game with classes. #commendting out the __init__ somehow allows the script to still 'work'
        super().__init__(libfile)
        #ultimately, what we need is:        
        self.translateX = None
        self.translateY = None
        self.scaleFactor= None
        self.angle = None
        
      

    def reset(self): #basically calling the __init__ again, similar to making a new instance. this is just for the alignment info function to reset stats.
        self.name = self.libfile.name
        self.cvimage = cv.imread(str(self.libfile))
        self.Height, self.Width = self.cvimage.shape[:2]
        self.Dimensions = (int(self.Width),int(self.Height))
        self.scaleDownImage()

        #ultimately, what we need is:        
        self.translateX = None
        self.translateY = None
        self.scaleFactor= None
        self.angle = None
        
        self.LeftEyeImageCoordinates = self.getImageCoordinates(leftLandmark)
        self.RightEyeImageCoordinates = self.getImageCoordinates(rightLandmark)
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
            #handling error statements within the alignImagetoBaseImage class
       

    def getAlignmentInfo(self,UltimateBaseImage):   #eyePoint = (BaseImage.LeftEyex,BaseImage.LeftEyey)
        original = self.cvimage #this is because we just want to do a mock alignment to get the info, not a final one, we want to revert it back at the end.
        oldXdifference = self.Xdifference
        self.UltimateBaseImageHeight,self.UltimateBaseImageWidth = UltimateBaseImage.cvimage.shape[:2]
        self.UltimateDimensions = (self.UltimateBaseImageWidth,self.UltimateBaseImageHeight)
        self.UltimatescaleFactor = UltimateBaseImage.Xdifference/self.Xdifference
        self.ExactXdifference = self.Xdifference*self.UltimatescaleFactor
        # print("initial ultimatexdiff: ",UltimateBaseImage.Xdifference)
        # print("initial baseimagexdiff: ",self.Xdifference)
        center = (self.LeftEyex, self.LeftEyey)
        Matrix = cv.getRotationMatrix2D((0,0), 0, self.UltimatescaleFactor)  #I was looking for a way to scale around an image for so long, it was so simple. 
        self.cvimage = cv.warpAffine(self.cvimage, Matrix, UltimateBaseImage.Dimensions) #the final one in warp affine is the image dimensions
 
        # print("2nd ultimatexdiff: ",UltimateBaseImage.Xdifference)
        # print("2nd baseimagexdiff: ",self.Xdifference)
        self.UltimatetranslateX = UltimateBaseImage.LeftEyex - self.LeftEyex 
        self.UltimatetranslateY = UltimateBaseImage.LeftEyey - self.LeftEyey

        eyePoint = (self.LeftEyex,self.LeftEyey)
        self.UltimateAngle = np.rad2deg(np.arctan((self.RightEyey-UltimateBaseImage.RightEyey)/(self.ExactXdifference))) #tangent formula right triangle.
                                                                            #I'm trying out ultimate base image as the denominator because it should be the same?
        self.reset()