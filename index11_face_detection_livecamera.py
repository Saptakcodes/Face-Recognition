import cv2 as cv

# Initialize the webcam (0 for default camera, change if using an external camera)
cap = cv.VideoCapture(0)

# Load the Haar cascade face detector
haar_cascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break  # If frame is not read properly, exit loop

    # Convert frame to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Detect faces
    faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(50, 50))

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces_rect:
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)

    # Display the number of faces detected on the frame
    face_count_text = f'Faces Detected: {len(faces_rect)}'
    cv.putText(frame, face_count_text, (20, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the video feed with detected faces
    cv.imshow('Live Face Detection', frame)

    # Exit on pressing 'q'
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv.destroyAllWindows()
