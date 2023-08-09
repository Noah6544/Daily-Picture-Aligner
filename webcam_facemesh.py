import cv2
import numpy as np
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh




def translate(img, x, y):
	transMat = np.float32([[1,0,x],[0,1,y]])
	dimensions = (img.shape[1], img.shape[0])
	return cv2.warpAffine(img, transMat, dimensions)


face_id_points = []
# For webcam input:
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
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
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		results = face_mesh.process(image)
		# Draw the face mesh annotations on the image.
		image.flags.writeable = True
		image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)		
		if results.multi_face_landmarks:
			for face_landmarks in results.multi_face_landmarks:
				
				# mp_drawing.draw_landmarks(
				# 		image=image,
				# 		landmark_list=face_landmarks,
				# 		connections=mp_face_mesh.FACEMESH_TESSELATION,
				# 		landmark_drawing_spec=None,
				# 		connection_drawing_spec=mp_drawing_styles
				# 		.get_default_face_mesh_tesselation_style())
				# mp_drawing.draw_landmarks(
				# 		image=image,
				# 		landmark_list=face_landmarks,
				# 		connections=mp_face_mesh.FACEMESH_CONTOURS,
				# 		landmark_drawing_spec=None,
				# 		connection_drawing_spec=mp_drawing_styles
				# 		.get_default_face_mesh_contours_style())
				mp_drawing.draw_landmarks(
						image=image,
						landmark_list=face_landmarks,
						connections=mp_face_mesh.FACEMESH_IRISES,
						landmark_drawing_spec=None,
						connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style())
				for id,landmark in enumerate(face_landmarks.landmark):
					image_height, image_width, image_c = image.shape
					x,y= (landmark.x*image_width),(landmark.y*image_height)
					# print(landmark.x)
					# print(landmark.y)
					# print("landmarky, x ^^")
					# print(str(x)+ ": x value\ny value: " + str(y))
					# movex = (.55*image_width) - x
					# movey = (.7*image_height) - y
					# image = translate(image,movex,movey)
					# #(x*image_width, y* image_height # the normal x is like .4, but multyping x and y by width and height (Respectively), gives you where it is. don't convert to int becauses then it looses accuracy.
					# face_id_points.append([x,y])
					cv2.putText(image, str(id), (int(x), int(y)), cv2.FONT_HERSHEY_PLAIN, 0.6, (0,0,255), 1)

	

		# Flip the image horizontally for a selfie-view display.
		cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))  #THIS FLIP, if you're trying to find landmarks, take this into consideration.
		if cv2.waitKey(5) & 0xFF == 27:
			break
cap.release()