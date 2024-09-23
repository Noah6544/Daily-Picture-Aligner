import cv2 as cv
import numpy as np
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
import shelve

print("Loading up...Hang on...")


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


    def getImageCoordinates(self,targetlandmark): #converted into a streamlined function for accessibility. can't speel. spell.
        with mp_face_mesh.FaceMesh(static_image_mode=True,max_num_faces=1,refine_landmarks=True,min_detection_confidence=0.5) as face_mesh:
            # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
            results = face_mesh.process(cv.cvtColor(self.cvimage, cv.COLOR_BGR2RGB))
            if not results.multi_face_landmarks: #if there are no face landmarks detected it will ignore.
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
        self.LeftEyeImageCoordinates = self.getImageCoordinates(468) #for the webcam alignment, this is horrendously slow. like 2fps.
        self.RightEyeImageCoordinates = self.getImageCoordinates(473) #and then to make it worse, we do it again for another eye.
        self.LeftEyex, self.LeftEyey = self.LeftEyeImageCoordinates[0],self.LeftEyeImageCoordinates[1]
        self.RightEyex, self.RightEyey = self.RightEyeImageCoordinates[0],self.RightEyeImageCoordinates[1]


    def scaleAroundPoint(self, BaseImage): #this function scales the image by a calculated scalefactor to remove and differences in camera distance.
        point = (BaseImage.LeftEyex,BaseImage.LeftEyey) 
        scaleFactor = (BaseImage.Xdifference/self.Xdifference) #a very simply formula i came up with, wasn't my first iteration, but it works now. I'm saying that like it's complex math, its literally a fraction ratio
        center = (self.Width , self.Height)
                         #x-y coord, rotation angle, scaling factor
        Matrix = cv.getRotationMatrix2D(center, 0, scaleFactor) #I was looking for a way to scale around an image for so long, it was so simple. 
        self.cvimage = cv.warpAffine(self.cvimage, Matrix, (self.Width, self.Height))

    def rotateImage(self,BaseImage): #this function rotates the image so that the slope of the eyes will align with the slope of the base image, if that makes sense. if it doesn't it just makes it better trust me.
        eyePoint = (BaseImage.LeftEyex,BaseImage.LeftEyey)

        angle = np.rad2deg(np.arctan((self.RightEyey-BaseImage.RightEyey)/(self.Xdifference)))
        rot_mat = cv.getRotationMatrix2D(eyePoint, angle, 1.0)
        self.cvimage = cv.warpAffine(self.cvimage, rot_mat, (BaseImage.Width,BaseImage.Height),cv.INTER_AREA) #INTER_AREA preserves quality and removes moire pattern?


    def translate(self, x, y): #this function simply shifts the image so that the left eye aligns with the base images left eye.
        transMat = np.float32([[1,0,x],[0,1,y]])
        dimensions = (self.cvimage.shape[1], self.cvimage.shape[0])
        self.LeftEyex += x 
        self.LeftEyey += y
        self.RightEyex += x
        self.RightEyey += y #manually updating them because it'll save some computational time in refreshing the images.
        self.cvimage = cv.warpAffine(self.cvimage, transMat, dimensions)


    def alignImagetoBaseImage(self,BaseImage):
        initialx,initially = BaseImage.LeftEyex,BaseImage.LeftEyey
        self.scaleAroundPoint(BaseImage)
        self.refreshEyeCoordinates()
        movex = initialx - self.LeftEyex 
        movey = initially - self.LeftEyey
        self.translate(movex,movey)
        self.rotateImage(BaseImage)



face_id_points = []
# For webcam input:
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv.VideoCapture(0, cv.CAP_DSHOW)
BaseImage = Image(cv.imread("BaseImages/baseimage2.jpg"))

cap.set(cv.CAP_PROP_FRAME_HEIGHT,4000)
cap.set(cv.CAP_PROP_FRAME_WIDTH,4000)
count = 0 
with mp_face_mesh.FaceMesh(
        max_num_faces=2,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        landmarkNumber = 468
        try:
            currentFrame = Image(image)
            if currentFrame.LeftEyeImageCoordinates or currentFrame.RightEyeImageCoordinates != None: #if successfully found image ##CHECK VERSION HISTORY
                if count == 0:
                    count = 1
                else:
                    if landmarkNumber == 468: #if we want the left eye
                        currentFrame.alignImagetoBaseImage(BaseImage)
                    elif landmarkNumber == 473: #if we want the right eye
                       currentFrame.alignImagetoBaseImage(BaseImage)

            # Flip the image horizontally for a selfie-view display.
            cv.imshow('MediaPipe Face Mesh', currentFrame.cvimage)  #THIS FLIP, if you're trying to find landmarks, take this into consideration.
            if cv.waitKey(1) & 0xFF == 27:
                break
        except Exception as error:
            print("No face detected." + str(error))
            if cv.waitKey(1) & 0xFF == 27:
                break
cap.release()