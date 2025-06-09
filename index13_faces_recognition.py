# pylint:disable=no-member
import numpy as np
import cv2 as cv

# Load pre-trained face detection model
haar_cascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")

# List of known people
owner = ['Saptak Chaki']

# Create face recognizer and load the trained model
face_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer.read('face_trained.yml')

# Open a connection to the webcam (0 for default camera)
cap = cv.VideoCapture(0)

# Set a confidence threshold for identifying a "stranger"
confidence_threshold = 75  # You can adjust this value as needed
flag=0
while True:
    # Capture frame-by-frame
    ret, img = cap.read()

    # If frame is captured correctly
    if not ret:
        print("Failed to grab frame")
        break

    # Convert image to grayscale for face detection
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces_rect = haar_cascade.detectMultiScale(gray, 1.1, 4)

    # Iterate through each detected face
    for (x, y, w, h) in faces_rect:
        # Get the region of interest (ROI) for the detected face
        faces_roi = gray[y:y+h, x:x+w]

        # Predict the label (name) and confidence of the detected face
        label, confidence = face_recognizer.predict(faces_roi)

        # Check if the confidence is below the threshold to classify as "Stranger"
        if confidence < confidence_threshold:
            label_text = owner[label]  # Recognized face
            color = (0, 255, 0)  # Green for owner
            flag=1
        else:
            label_text = "Stranger"
            color = (0, 0, 255)  # Red for stranger
            flag=0

        # Display the label and confidence on the frame
        cv.putText(img, f'{label_text} - {round(confidence, 2)}', (x, y-10), cv.FONT_HERSHEY_COMPLEX, 0.8, color, thickness=2)

        # Draw rectangle around the face
        cv.rectangle(img, (x, y), (x+w, y+h), color, thickness=2)

    # Display the resulting frame with face recognition
    cv.imshow('Face Detection - Live', img)

    # Exit the loop when the user presses 'q'
    if cv.waitKey(20) & 0xFF == ord('q'):
        break
if flag==1:
    print("owner detected")
else:
    print("stranger detected")
# Release the webcam and close the OpenCV window
cap.release()
cv.destroyAllWindows()
