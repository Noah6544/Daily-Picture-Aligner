import cv2
import numpy as np
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh



def scale_around_point(image, point, scale):
	# Get the size of the image
	(h, w) = image.shape[:2]

	# Translate the point to the center of the image
	center = (w // 2, h // 2)
	M = cv2.getRotationMatrix2D(center, 0, 1.0)
	(tx, ty) = ((center[0] - point[0]) * scale, (center[1] - point[1]) * scale)
	M[0, 2] += tx
	M[1, 2] += ty

	# Apply the transformation
	return cv2.warpAffine(image, M, (w, h))


def translate(img, x, y):
	transMat = np.float32([[1,0,x],[0,1,y]])
	dimensions = (img.shape[1], img.shape[0])
	return cv2.warpAffine(img, transMat, dimensions)


def scaleImagetoBaseImage(image,Xdifference,ConstantXdifference):
	#maybe create a loop to keep scalling it until the scale factor is close to 0.
	distanceDifference = ConstantXdifference - Xdifference
	scaleFactor = 1
	print("scale Factor: " + str(scaleFactor))
	running = True
	while distanceDifference != 0:
		if scaleFactor > 0: #if face is larger than baseimage: then shrink it
			testimage = cv2.resize(image, (image.shape[0],image.shape[1]), -1*scaleFactor,-1*scaleFactor)
		elif scaleFactor <0: #if face is smaller than baseimage: then scale it up
			testimage = cv2.resize(image, (image.shape[0],image.shape[1]), scaleFactor,scaleFactor)

		LeftEyeImageCoordinates = getImageCoordinates(testimage,468)
		RightEyeImageCoordinates = getImageCoordinates(testimage,473)
		LeftEyex, LeftEyey = LeftEyeImageCoordinates[0],LeftEyeImageCoordinates[1]
		RightEyex, RightEyey = RightEyeImageCoordinates[0],RightEyeImageCoordinates[1]
		distanceDifference = ConstantXdifference - (RightEyex-LeftEyex)
		scaleFactor += 10
		print("distanceDifference: " + str(distanceDifference))
		print("Left eye coordinates: " + str(LeftEyeImageCoordinates) + "\nRight Eye coordinates: " + str(RightEyeImageCoordinates))
		print("Test image X Value: "+ str(RightEyex) +" Y value: " + str(LeftEyex))
		print("Scale Factor: " + str(scaleFactor))
		cv2.imshow("growing window",testimage)
		cv2.waitKey(10)
		cv2.destroyAllWindows() 
		if distanceDifference  == 0:
			return testimage
	
def getBaseImageStats(baseimage):
	print(baseimage.shape[:-1])
	LeftEyeImageCoordinates = getImageCoordinates(baseimage,468)
	RightEyeImageCoordinates = getImageCoordinates(baseimage,473)
	LeftEyex, LeftEyey = LeftEyeImageCoordinates[0],LeftEyeImageCoordinates[1]
	RightEyex, RightEyey = RightEyeImageCoordinates[0],RightEyeImageCoordinates[1]
	Ydifference = RightEyey - LeftEyey
	Xdifference = RightEyex - LeftEyex
	return ([LeftEyex,LeftEyey],[RightEyex,RightEyey],[Xdifference,Ydifference])

def getImageCoordinates(img,targetlandmark):
	imgHeight, imgWidth = img.shape[:2]
	with mp_face_mesh.FaceMesh(static_image_mode=True,max_num_faces=1,refine_landmarks=True,min_detection_confidence=0.5) as face_mesh:
		# Convert the BGR image to RGB and process it with MediaPipe Face Detection.
		results = face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
		if not results.multi_face_landmarks: #if there are no face landmarks detected it will ignore.
			return None
		# Print and draw face mesh landmarks on image.
		for face_landmarks in results.multi_face_landmarks:	
			# mp_drawing.draw_landmarks(
			# 	image=image,
			# 	landmark_list=face_landmarks,
			# 	connections=mp_face_mesh.FACEMESH_TESSELATION,
			# 	landmark_drawing_spec=None,
			# 	connection_drawing_spec=mp_drawing_styles
			# 	.get_default_face_mesh_tesselation_style())
			# mp_drawing.draw_landmarks(
			# 	image=image,
			# 	landmark_list=face_landmarks,
			# 	connections=mp_face_mesh.FACEMESH_CONTOURS,
			# 	landmark_drawing_spec=None,
			# 	connection_drawing_spec=mp_drawing_styles
			# 	.get_default_face_mesh_contours_style())
			# mp_drawing.draw_landmarks(
			# image=image,
			# landmark_list=face_landmarks,
			# connections=mp_face_mesh.FACEMESH_IRISES,
			# landmark_drawing_spec=None,
			# connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style())
		
			face_id_points = []
			for id, landmark in enumerate(face_landmarks.landmark):
				if id == targetlandmark: #this is the point I'm targeting: 468 is the left eye, 473 for the right looks great.
					currentImageCoordinates = [int(landmark.x*imgWidth),int(landmark.y*imgHeight),landmark.z]
					return currentImageCoordinates
				else:
					pass

face_id_points = []
# For webcam input:
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
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
		LeftEyeImageCoordinates = getImageCoordinates(image,468)
		RightEyeImageCoordinates = getImageCoordinates(image,473)
		

		if LeftEyeImageCoordinates or RightEyeImageCoordinates != None: #if successfully found image ##CHECK VERSION HISTORY
			LeftEyex, LeftEyey = LeftEyeImageCoordinates[0],LeftEyeImageCoordinates[1]
			RightEyex, RightEyey = RightEyeImageCoordinates[0],RightEyeImageCoordinates[1]
			if count == 0:
				BaseImageStats = getBaseImageStats(image)
				print("BaseImageStats: "+ str(BaseImageStats))
				count = 1
			else:
				if landmarkNumber == 468: #if we want the left eye
					initialx, initialy = BaseImageStats[0][0],BaseImageStats[0][1] #.55 and .34 are arbitary numbers i picked.
					movex = initialx - LeftEyex 
					movey = initialy - LeftEyey
					image = scaleImagetoBaseImage(image,(RightEyex-LeftEyex),BaseImageStats[2][0])
					image = translate(image,movex,movey)
					print(str(movex) + "move x")
				elif landmarkNumber == 473: #if we want the right eye
					initialx, initialy = BaseImageStats[1][0],BaseImageStats[1][1] #.55 and .34 are arbitary numbers i picked.
					movex = initialx - RightEyex 
					movey = initialy - RightEyey  
					image = translate(image,movex,movey)
		else: 
			print("No face was found for this frame: ")

		# Flip the image horizontally for a selfie-view display.
		cv2.imshow('MediaPipe Face Mesh', image)  #THIS FLIP, if you're trying to find landmarks, take this into consideration.
		if cv2.waitKey(5) & 0xFF == 27:
			break
cap.release()