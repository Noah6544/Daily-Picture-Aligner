import cv2 as cv
import numpy as np
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

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


    def getImageCoordinates(self,targetlandmark,**args):
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

    def refreshEyeCoordinates(self):
        self.LeftEyeImageCoordinates = self.getImageCoordinates(468)
        self.RightEyeImageCoordinates = self.getImageCoordinates(473)
        self.LeftEyex, self.LeftEyey = self.LeftEyeImageCoordinates[0],self.LeftEyeImageCoordinates[1]
        self.RightEyex, self.RightEyey = self.RightEyeImageCoordinates[0],self.RightEyeImageCoordinates[1]
        print("refreshed stats!")



    def scale_around_point(self, BaseImage):
        # # Get the size of the image
        # (h, w) = self.image.shape[:2]

        # # Translate the point to the center of the image
        # center = (w // 2, h // 2)
        # M = cv.getRotationMatrix2D(center, 0, 1.0)
        # (tx, ty) = ((center[0] - point[0]) * scale, (center[1] - point[1]) * scale)
        # M[0, 2] += tx
        # M[1, 2] += ty

        # # Apply the transformation
        # return cv.warpAffine(image, M, (w, h))

        # Get the size of the image
        point = (BaseImage.LeftEyex,BaseImage.LeftEyey)
        scaleFactor = (BaseImage.Xdifference/self.Xdifference)
        print("ScaleFactor: " + str(scaleFactor))



        # Translate the point to the center of the image

        center = (self.Width , self.Height)
        M = cv.getRotationMatrix2D(center, 0, scaleFactor)
        print(M)
        print("done")
        # (tx, ty) = ((center[0] - point[0]) * scaleFactor, (center[1] - point[1]) * scaleFactor)
        # M[0, 2] += tx
        # M[1, 2] += ty

        # Apply the transformation
        self = cv.warpAffine(self.cvimage, M, (self.Width, self.Height))
        return self




    def translate(self,cvimage, x, y):
        transMat = np.float32([[1,0,x],[0,1,y]])
        dimensions = (cvimage.shape[1], cvimage.shape[0])
        return cv.warpAffine(cvimage, transMat, dimensions)


    def rotate_image(self, angle, pivot_point):
        rot_mat = cv.getRotationMatrix2D(pivot_point, angle, 1.0)
        result = cv.warpAffine(self.cvimage, rot_mat, self.cvimage.shape[1::-1], flags=cv.INTER_LINEAR)
        return result

    def scaleImagetoBaseImage(self,BaseImage):
        #calculating the percentage to scale our image by depending on our base image.
        # if self.Xdifference > BaseImage.Xdifference: #if our image is too big it'll negatively scale   
        #     scaleFactor = 100*(1 - (self.Xdifference/BaseImage.Xdifference))
        # elif self.Xdifference < BaseImage.Xdifference: #if our image is too small, it'll positivly scale
        #     scaleFactor = 100*(2 - (self.Xdifference/BaseImage.Xdifference)) 
        # else:
        #     scaleFactor = 1
        scaleFactor = (BaseImage.Xdifference/self.Xdifference)
        self.Height = self.Height*scaleFactor
        self.Width = self.Width*scaleFactor
        print(self.Height)
        print(self.Width)

        print("scale Factor: " + str(scaleFactor))
        print("X Difference: " + str(BaseImage.Xdifference - self.Xdifference))
        return cv.resize(self.cvimage, (int(self.Width),int(self.Height)), interpolation=cv.INTER_AREA)


    def bruteForceRotation(image,rightEyex,rightEyey):
        rotationAmount = 4
        baseimageYdifference = 1013-995 #values i pulled from my base image.
        Ydifference = 0 
        while rotationAmount > -5 and rotationAmount < 1: #values i pulled by subtracting right eye y value from left y value (my right eye is higher.)
            rotatedImage = rotate_image(image,rotationAmount,(rightEyex,rightEyey))
            rightimagecoordinates = getImageCoordinates(rotatedImage,473)
            leftimagecoordinates = getImageCoordinates(rotatedImage,468)
            Ydifference = rightimagecoordinates[1] - leftimagecoordinates[1]
            rotationAmount -= .1
            if abs(Ydifference) == 18:  #ToDo: fix this brute force rotation. take into account weird files and start lower. 
                                        #Code it so that it also checks if it's moving in the right direction, and if it overshoots, pick the last item.
                break
            print(Ydifference)
            print(rotationAmount)
            # cv.imshow("asdf",rotatedImage)
            # cv.waitKey(10)
      
        cv.destroyAllWindows()

        return rotatedImage



face_id_points = []
# For webcam input:
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv.VideoCapture(1)
cap.set(cv.CAP_PROP_FRAME_HEIGHT,720)
cap.set(cv.CAP_PROP_FRAME_WIDTH,1280)
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
        currentFrame = Image(image)



        if currentFrame.LeftEyeImageCoordinates or currentFrame.RightEyeImageCoordinates != None: #if successfully found image ##CHECK VERSION HISTORY
            if count == 0:
                BaseImage = Image(cv.imread("baseimage.jpg"))
                count = 1
            else:
                if landmarkNumber == 468: #if we want the left eye
                    initialx,initialy = .45*BaseImage.cvimage.shape[1],.5*BaseImage.cvimage.shape[0]
                    currentFrame.cvimage = currentFrame.scale_around_point(BaseImage)
                    currentFrame.refreshEyeCoordinates()
                    movex = initialx - currentFrame.LeftEyex 
                    movey = initialy - currentFrame.LeftEyey
                    image = currentFrame.translate(currentFrame.cvimage,movex,movey)
                    print(str(movex) + "move x")
                elif landmarkNumber == 473: #if we want the right eye
                    movex = initialx - RightEyex 
                    movey = initialy - RightEyey  
                    # image = translate(image,movex,movey)
        else: 
            print("No face was found for this frame: ")

        # Flip the image horizontally for a selfie-view display.
        cv.imshow('MediaPipe Face Mesh', image)  #THIS FLIP, if you're trying to find landmarks, take this into consideration.
        if cv.waitKey(5) & 0xFF == 27:
            break
cap.release()