# pylint:disable=no-member
import os
import cv2 as cv
import numpy as np

# List of people (each person should have a subfolder inside DIR)
people = ['Saptak_Chaki']

# Main directory where subfolders for each person exist
DIR = r'C:\Users\pc\OneDrive\Desktop' 


# Load Haar cascade
haar_cascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")

# Lists to store training data
features = []
labels = []

def create_train():
    for person in people:
        path = os.path.join(DIR, person)  # Path to person's folder
        label = people.index(person)  # Label based on index

        if not os.path.exists(path):
            print(f"Warning: Directory not found - {path}")
            continue

        for img in os.listdir(path):
            img_path = os.path.join(path, img)

            img_array = cv.imread(img_path)
            if img_array is None:
                print(f"Skipping invalid image: {img_path}")  # Debugging info
                continue 

            gray = cv.cvtColor(img_array, cv.COLOR_BGR2GRAY)

            faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(50, 50))

            for (x, y, w, h) in faces_rect:
                faces_roi = gray[y:y+h, x:x+w]
                features.append(faces_roi)
                labels.append(label)

# Create training data
create_train()

# Debugging output to check how many samples we have
print(f"Training done. Total face samples collected: {len(features)}")
print(f"Total labels collected: {len(labels)}")

# If no faces were found, stop the program
if len(features) == 0 or len(labels) == 0:
    print("Error: No face data found. Check dataset and parameters.")
    exit()

# Convert lists to NumPy arrays
features = np.array(features, dtype='object')
labels = np.array(labels)

# Create and train the LBPH Face Recognizer
face_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer.train(features, labels)

# Save the trained model and data
face_recognizer.save('face_trained.yml')
np.save('features.npy', features)
np.save('labels.npy', labels)

print("Model saved successfully!")
