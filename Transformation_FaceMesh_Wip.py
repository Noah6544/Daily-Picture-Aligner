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
daily_photo_path = "Daily Photo Converted\\"
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
		cv.imshow("asdf",rotatedImage)
		cv.waitKey(10)
  
	cv.destroyAllWindows()

	return rotatedImage
			

  
	
###RUNNING CODE


baseimage = cv.imread("baseimage.jpg")


#specifically this for loop gets all files and only keeps the ones that are jpg files and aren't curropted or 0 in size.
for file in os.listdir(daily_photo_path):
	#endswith("g") because that's for png/jpg files. I didn't know how to check for the last 4 position slots because each file name size is different and the initial start is different. anyways this works currently
	if file.endswith("g") and os.path.getsize(daily_photo_path + file) > 0 and file != "1871.jpg":
		cvimage = cv.imread(daily_photo_path + file)
		#cv2image = cv.resize(cv2image, (width,height))
		currentImageCoordinates = getImageCoordinates(cvimage,473)
		print(currentImageCoordinates)
		if currentImageCoordinates != None: #if successfully found image
			currentImagex, currentImagey = currentImageCoordinates[0],currentImageCoordinates[1]
			initialx, initialy = cvimage.shape[0]*.55,cvimage.shape[1]*.34 #.55 and .34 are arbitary numbers i picked.
			print(cvimage.shape)
			movex = initialx - currentImagex 
			movey = initialy - currentImagey  
			finalimage = scale_around_point(cvimage,(currentImagex,currentImagey),-currentImageCoordinates[2])
			print(movex,movey)
			finalimage = translate(cvimage,movex,movey)
			finalimage = bruteForceRotation(finalimage,currentImagex,currentImagey)
			cv.imshow("fingerscrossed",finalimage)
			cv.waitKey(10)
			cv.imwrite(adjusted_images_path+file+"_adjusted.jpg",finalimage)
		else: 
			print("No face was found for file: " + file)
	else:
		pass	
