#TBH copilot wrote this.

import cv2
import os
import numpy as np

# Initialize the face recognizer and face detector
recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Path to the dataset
dataset_path = 'trainFaces'

# Prepare training data
faces = []
labels = []

# Assign a unique ID to each person
label_id = 0
label_dict = {}

for person_name in os.listdir(dataset_path):
    person_path = os.path.join(dataset_path, person_name)
    if not os.path.isdir(person_path):
        continue

    label_dict[label_id] = person_name

    for image_name in os.listdir(person_path):
        image_path = os.path.join(person_path, image_name)
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces
        face_rects = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in face_rects:
            face = gray[y:y+h, x:x+w]
            faces.append(face)
            labels.append(label_id)

    label_id += 1

# Train the recognizer
recognizer.train(faces, np.array(labels))

# Save the trained model
recognizer.save('face_trainer.yml')

# Save the label dictionary
with open('labels.txt', 'w') as f:
    for label_id, person_name in label_dict.items():
        f.write(f"{label_id},{person_name}\n")

print("Training complete and model saved as face_trainer.yml")
