import os
import glob
import cv2 as cv
import RPi.GPIO as GPIO
from picamera2 import Picamera2
import smtplib
from time import sleep, time
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Email configuration
sender = 'chakisaptak@gmail.com'
password = 'wzln knpe mvxb xzih'
receiver = 'chakisaptak@gmail.com'

DIR = '/home/pi/Pictures'
prefix = 'image'

# GPIO pin configuration for Ultrasonic Sensor, Buzzer, and LED
TRIG = 16  # Trigger pin for ultrasonic sensor
ECHO = 18  # Echo pin for ultrasonic sensor
BUZZER = 22  # Buzzer pin
LED = 12  # LED pin for Stranger detection

# Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(LED, GPIO.OUT)  # Set LED pin as output

# Load pre-trained face detection model
haar_cascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")

# List of known people
owner = ['Saptak Chaki']

# Create face recognizer and load the trained model
face_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer.read('face_trained.yml')

# Function to send email with the image attachment
def send_mail(filename):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = 'Visitor'
    body = 'Find the picture in attachments.'
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach the image file
    try:
        with open(filename, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(filename)}')
            msg.attach(part)
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to capture and save an image
def capture_img():
    print('Capturing image...')
    if not os.path.exists(DIR):
        os.makedirs(DIR)
    
    files = sorted(glob.glob(os.path.join(DIR, prefix + '[0-9][0-9][0-9].jpg')))
    count = len(files)
    filename = os.path.join(DIR, prefix + '{:03d}.jpg'.format(count))
    
    try:
        picam2 = Picamera2()
        picam2.start_and_capture_file(filename)
        print(f"Image saved: {filename}")
        send_mail(filename)
    except Exception as e:
        print(f"Failed to capture image: {e}")

# Function to measure the distance using the ultrasonic sensor
def distance():
    GPIO.output(TRIG, False)
    sleep(0.1)

    GPIO.output(TRIG, True)
    sleep(0.00001)  # Corrected pulse duration
    GPIO.output(TRIG, False)

    pulse_start = time()
    timeout = pulse_start + 0.04  # Set a timeout of 40ms

    while GPIO.input(ECHO) == 0:
        pulse_start = time()
        if pulse_start > timeout:
            print("Timeout: Echo signal not received")
            return None

    pulse_end = time()
    timeout = pulse_end + 0.04  # Set another timeout

    while GPIO.input(ECHO) == 1:
        pulse_end = time()
        if pulse_end > timeout:
            print("Timeout: Echo signal too long")
            return None

    pulse_duration = pulse_end - pulse_start
    measured_distance = pulse_duration * 17150  # Speed of sound in air

    # Validate distance reading
    if measured_distance > 200 or measured_distance <= 2:
        print("Invalid distance measurement.")
        return None
    return round(measured_distance, 2)

# Function to control LED light
def control_led(is_stranger):
    if is_stranger:
        GPIO.output(LED, GPIO.HIGH)  # Turn on LED if stranger
        print("Stranger detected. LED on.")
    else:
        GPIO.output(LED, GPIO.LOW)  # Turn off LED if owner
        print("Owner detected. LED off.")

# Main loop to detect objects and trigger actions
last_email_sent = 0
email_delay = 60  # Time in seconds to wait before sending another email

try:
    while True:
        # Face recognition process
        cap = cv.VideoCapture(0)
        ret, img = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        faces_rect = haar_cascade.detectMultiScale(gray, 1.1, 4)

        is_stranger = True  # Default assumption is stranger
        for (x, y, w, h) in faces_rect:
            faces_roi = gray[y:y+h, x:x+w]
            label, confidence = face_recognizer.predict(faces_roi)

            if confidence < 85:  # If confidence is good, consider it the owner
                label_text = owner[label]
                color = (0, 255, 0)  # Green for owner
                is_stranger = False
            else:
                label_text = "Stranger"
                color = (0, 0, 255)  # Red for stranger

            cv.putText(img, f'{label_text} - {round(confidence, 2)}', (x, y-10), cv.FONT_HERSHEY_COMPLEX, 0.8, color, thickness=2)
            cv.rectangle(img, (x, y), (x+w, y+h), color, thickness=2)

        cv.imshow('Face Detection - Live', img)
        cap.release()
        cv.destroyAllWindows()

        control_led(is_stranger)  # Control the LED based on face detection

        if is_stranger:  # If stranger is detected, ring buzzer and capture image
            dist = distance()
            if dist is not None and dist < 50:
                print("Object detected. Ringing the buzzer and capturing the image.")
                GPIO.output(BUZZER, GPIO.HIGH)  # Turn on buzzer
                capture_img()
                GPIO.output(BUZZER, GPIO.LOW)  # Turn off buzzer
                sleep(5)  # Wait before resetting
        else:
            print("Owner detected. No buzzer.")

        sleep(1)  # Small delay between iterations

except KeyboardInterrupt:
    print("Exiting...")

finally:
    GPIO.cleanup()  # Clean up GPIO on exit
