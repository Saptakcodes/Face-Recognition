# 🎯 Face Recognition Doorbell  
### 🚪 Contactless IoT Doorbell using Raspberry Pi 3, Face Detection & Recognition

---

## 📌 Project Overview

This project implements a **contactless smart doorbell system** using **Raspberry Pi 3**, featuring:

- 📡 Ultrasonic sensor for touchless visitor detection  
- 📷 Camera module for capturing visitor images  
- 🤖 Face detection and recognition using OpenCV  
- 📧 Email notifications via SMTP  
- 🔔 Buzzer alert system for unknown visitors  

---

## 🧰 Hardware Requirements

- 🧠 Raspberry Pi 3 with Raspbian OS  
- 📸 Pi Camera or USB Webcam  
- 📏 Ultrasonic Sensor HC-SR04  
- 🔊 Buzzer Module  
- 🔌 Jumper Wires  
- 💾 64GB microSD Card  
- 🖴 SD Card Adapter  

---

## 💻 Software Requirements

- 🛠️ Raspberry Pi Imager  
- 🖥️ REAL VNC Viewer  
- 🖧 VNC Server  
- 🔍 Advanced IP Scanner  
- 🧠 OpenCV (Python Library)  
- ✉️ Python SMTP Libraries  

---

## ⚙️ Installation & Setup

### 🎥 Enable Camera Interface


sudo raspi-config


Go to Interfacing Options > Camera and enable it. Then reboot the Pi.

📦 Install Required Packages
bash
Copy
Edit
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-opencv
pip install smtplib
🔗 Clone This Repository
bash
Copy
Edit
git clone https://github.com/Saptakcodes/Face-Recognition.git
cd contactless-iot-doorbell
📁 Project Structure
bash
Copy
Edit
Face-Recognition/
│
├── raspberry_pi_finalmodel_optimized.py      # Final Raspberry Pi model
├── index11_face_detection_livecamera.py      # Face detection module using live camera
├── index13_face_recognition.py               # Face recognition module
├── index12_faces_train.py                    # Script to train on known faces
├── Saptak_Chaki/                             # Owner's face images (training data)
├── haarcascade_frontalface_default.xml       # Haar cascade classifier
├── face_trained.yml                          # Trained face recognition model
└── README.md                                 # This file
▶️ Usage
✅ Connect all hardware components as per the circuit diagram.

🏃‍♂️ Run the main program:

bash
Copy
Edit
python3 main.py
📸 System Workflow:

Detects visitors via ultrasonic sensor

Captures image when someone approaches

Detects and recognizes face in real-time

If unrecognized, it:

Sends email notification with captured image

Rings the buzzer

If recognized as the owner, it does nothing

🌟 Features
🙌 Contactless visitor detection

🧠 Real-time face recognition

📧 Email notifications with visitor images

🚫 No buzzer disturbance for recognized faces

⚙️ Adjustable detection range (default: 80 cm)

🛑 Rate-limited email alerts to prevent spamming

🔮 Future Scope
🤖 Integration of deep learning models (FaceNet, Dlib, etc.)

📱 Mobile app for live feed and control

🔐 Smart lock integration for automated access

🎥 Real-time video and audio communication

☁️ Cloud storage and dashboard analytics

📡 Compatibility with smart home ecosystems (Alexa, Google Home)

🔒 GDPR-compliant privacy and encryption standards

🧪 Troubleshooting
❌ Camera not detected?
Run sudo raspi-config to enable it under Interfacing Options.

⚠️ SMTP not working?
Use an App Password (especially for Gmail) instead of your main password.

🔍 Sensor not accurate?
Check distance range, wiring, or adjust the threshold in code.

📜 License
This project is licensed under the MIT License. See the LICENSE file for more details.

🙏 Acknowledgments
🧠 OpenCV – for face detection & recognition

🍓 Raspberry Pi Foundation – for hardware and documentation

🐍 Python Community – for libraries and open-source support

🚀 Built with 💡 innovation and 🔒 security by Group 1
