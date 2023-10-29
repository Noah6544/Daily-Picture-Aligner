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
images_path = "daily"
daily_photo_path = "C:\\Users\\Noah\'s Marc P. 4648\\Pictures\\FinalDailyPics\\"
daily_photo_path = "Daily Photo Converted\\"

adjusted_images_path = "C:\\Users\\Noah\'s Marc P. 4648\\Pictures\\FinalDailyPics\\Adjusted\\"
adjusted_images_path = "adjusted images\\"

mp_face_mesh = mp.solutions.face_mesh
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
drawing_spec = mp_drawing.DrawingSpec(thickness=0, circle_radius=1)




def scale_around_point(image, point, scale):
	# Get the size of the image
	(h, w) = image.shape[:2]

	# Translate the point to the center of the image
	center = (w // 2, h // 2)
	M = cv.getRotationMatrix2D(center, 0, 1.0)
	(tx, ty) = ((center[0] - point[0]) * scale, (center[1] - point[1]) * scale)
	M[0, 2] += tx
	M[1, 2] += ty

	# Apply the transformation
	return cv.warpAffine(image, M, (w, h))


def getImageCoordinates(img,targetlandmark):
	imgHeight, imgWidth = img.shape[:2]
	with mp_face_mesh.FaceMesh(static_image_mode=True,max_num_faces=1,refine_landmarks=True,min_detection_confidence=0.5) as face_mesh:
		# Convert the BGR image to RGB and process it with MediaPipe Face Detection.
		results = face_mesh.process(cv.cvtColor(img, cv.COLOR_BGR2RGB))
		if not results.multi_face_landmarks: #if there are no face landmarks detected it will ignore.
			return None
		# Print and draw face mesh landmarks on image.
		for face_landmarks in results.multi_face_landmarks:		
			face_id_points = []
			for id, landmark in enumerate(face_landmarks.landmark):
				if id == targetlandmark: #this is the point I'm targeting: 468 is the left eye, 473 for the right looks great.
					currentImageCoordinates = [int(landmark.x*imgWidth),int(landmark.y*imgHeight),landmark.z]
					return currentImageCoordinates
				else:
					pass


def translate(img, x, y):
	transMat = np.float32([[1,0,x],[0,1,y]])
	dimensions = (img.shape[1], img.shape[0])
	return cv.warpAffine(img, transMat, dimensions)


def rotate_image(image, angle, pivot_point):
	rot_mat = cv.getRotationMatrix2D(pivot_point, angle, 1.0)
	result = cv.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv.INTER_LINEAR)
	return result

def scaleImagetoBaseImage(image,Xdifference,ConstantXdifference):
	scaleFactor = ConstantXdifference - Xdifference
	print("scale Factor: " + str(scaleFactor))
	return cv.resize(image, (image.shape[:2]), scaleFactor*10,scaleFactor*10)


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
	
#ToDo: implement a cool "drawing with your eyes." kinda thing

def getBaseImageStats(baseimage):
	LeftEyeImageCoordinates = getImageCoordinates(baseimage,468)
	RightEyeImageCoordinates = getImageCoordinates(baseimage,473)
	LeftEyex, LeftEyey = LeftEyeImageCoordinates[0],LeftEyeImageCoordinates[1]
	RightEyex, RightEyey = RightEyeImageCoordinates[0],RightEyeImageCoordinates[1]
	Ydifference = RightEyey - LeftEyey
	Xdifference = RightEyex - LeftEyex
	return ([LeftEyex,LeftEyey],[RightEyex,RightEyey],[Xdifference,Ydifference])

  

	
###RUNNING CODE


baseimage = cv.imread("baseimage.jpg")
BaseImageStats = getBaseImageStats(baseimage)
print(BaseImageStats)
count = 1

landmarkNumber = 468
#specifically this for loop gets all files and only keeps the ones that are jpg files and aren't curropted or 0 in size.
for file in os.listdir(daily_photo_path):
	if file in os.listdir(adjusted_images_path):
		pass
	else:
		#endswith("g") because that's for png/jpg files. I didn't know how to check for the last 4 position slots because each fle name size is different and the initial start is different. anyways this works currently
		if file.endswith("g") and os.path.getsize(daily_photo_path + file) > 0 and file != "1871.jpg":
			cvimage = cv.imread(daily_photo_path + file)
			#cv2image = cv.resze(cv2image, (width,height))
			LeftEyeImageCoordinates = getImageCoordinates(cvimage,468)
			RightEyeImageCoordinates = getImageCoordinates(cvimage,473)
			if RightEyeImageCoordinates and LeftEyeImageCoordinates != None: #if successfullyfound image
				LeftEyex, LeftEyey = LeftEyeImageCoordinates[0],LeftEyeImageCoordinates[1]
				RightEyex, RightEyey = RightEyeImageCoordinates[0],RightEyeImageCoordinates[1]

				if landmarkNumber == 468: #if we want the left eye
					
					initialx,initialy = .45*cvimage.shape[1],.5*cvimage.shape[0] #those are % alues of where i want theleft eye to be. about 45% over to the left and 60% up on the sreen.
					movex = initialx - LeftEyex 
					movey = initialy - LeftEyey
					# imge = scaleImagetoBaseImage(cvimage,(RightEyex-LeftEyex),BseImageStats[2][0])
					finalimage = translate(cvimage,movex,movey)
					print(str(movex) + "move x")
				elif landmarkNumber == 473: #if we wantthe right eye
					initialx, initiay = BaseImageStats[1][0],BaseImageStats[1][1] #.5 and .34 are arbitary numbers i picked.
					move = initialx - Rightyex 
					movey = initialy - RightEyey  
					finalimage = translate(cvimage,movex,movey)


				# cv.imshow("Newly Aligned Image",finalimage)
				# cv.waitKey(100)				added_imag = v2.addWeihted(baseimage,0.4,finalimage,0.1,0)
				finalimage.resize(200,200)
				baseimage.resize((200,200))
				added_image = cv.addWeighted(baseimage,0.4,finalimage,0.1,0)
				cv.imwrite(file+"_overlayadjusted.jpg",added_image)
				print("Successfully aligned and wrote to file image: \'" + str(file) +"\' #" + str(count))
				count += 1
			
			else: 
				print("No face was found for file: " + file)	
		else:
			pass

				
