import os
import glob
import cv2 as cv
import RPi.GPIO as GPIO
import smtplib
import threading
from time import sleep, time
from picamera2 import Picamera2
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Email Configuration
SENDER = 'chakisaptak@gmail.com'
PASSWORD = 'wzln knpe mvxb xzih'
RECEIVER = 'chakisaptak@gmail.com'
EMAIL_DELAY = 60  # Minimum time (seconds) between emails
last_email_sent = 0

# GPIO Configuration
TRIG, ECHO, BUZZER, LED = 16, 18, 22, 12
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup([TRIG, BUZZER, LED], GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Face Recognition Setup
haar_cascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")
face_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer.read('face_trained.yml')
owners = ['Saptak Chaki']

# Function to send email
def send_mail(filename):
    global last_email_sent
    if time() - last_email_sent < EMAIL_DELAY:
        return
    last_email_sent = time()
    
    msg = MIMEMultipart()
    msg['From'], msg['To'], msg['Subject'] = SENDER, RECEIVER, 'Visitor Detected'
    msg.attach(MIMEText('Find the attached visitor image.', 'plain'))
    
    try:
        with open(filename, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(filename)}')
            msg.attach(part)
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, RECEIVER, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Email sending failed: {e}")

# Function to capture image
def capture_img():
    filename = '/home/pi/Pictures/visitor.jpg'
    try:
        picam2 = Picamera2()
        picam2.start_and_capture_file(filename)
        print(f"Image saved: {filename}")
        threading.Thread(target=send_mail, args=(filename,)).start()
    except Exception as e:
        print(f"Failed to capture image: {e}")

# Function to measure distance
def distance():
    GPIO.output(TRIG, False)
    sleep(0.1)
    GPIO.output(TRIG, True)
    sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = time()
    timeout = pulse_start + 0.04
    while GPIO.input(ECHO) == 0:
        pulse_start = time()
        if pulse_start > timeout:
            return None
    
    pulse_end = time()
    timeout = pulse_end + 0.04
    while GPIO.input(ECHO) == 1:
        pulse_end = time()
        if pulse_end > timeout:
            return None
    
    measured_distance = (pulse_end - pulse_start) * 17150
    return round(measured_distance, 2) if 2 <= measured_distance <= 200 else None

# Function to detect faces
def detect_faces():
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 240)
    cap.set(cv.CAP_PROP_FPS, 10)
    
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return None, True
    
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(gray, 50, 150)  # Edge detection before face detection
    faces_rect = haar_cascade.detectMultiScale(edges, 1.1, 4)
    
    is_stranger = True
    for (x, y, w, h) in faces_rect:
        face_roi = gray[y:y+h, x:x+w]
        label, confidence = face_recognizer.predict(face_roi)
        if confidence < 85:
            is_stranger = False
            break
    
    return frame, is_stranger

# Main Loop
def main_loop():
    while True:
        frame, is_stranger = detect_faces()
        GPIO.output(LED, GPIO.HIGH if is_stranger else GPIO.LOW)
        
        if is_stranger:
            dist = distance()
            if dist and dist < 50:
                print("Stranger detected! Ringing buzzer and capturing image.")
                GPIO.output(BUZZER, GPIO.HIGH)
                threading.Thread(target=capture_img).start()
                GPIO.output(BUZZER, GPIO.LOW)
                sleep(5)
        sleep(1)

try:
    main_loop()
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
