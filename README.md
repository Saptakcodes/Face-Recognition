# Face-Recognition
Contactless IOT Doorbell using Raspberry Pi 3 and Face Detection and Face Recognition models
Contactless IoT Doorbell with Face Recognition
Project Overview
This project implements a contactless IoT doorbell system using Raspberry Pi 3, featuring:

Ultrasonic sensor for touchless visitor detection

Camera module for capturing visitor images

Face detection and recognition using OpenCV

Email notifications via SMTP

Buzzer alert system

Hardware Requirements
Raspberry Pi 3 with Raspbian OS

Pi Camera or USB webcam

Ultrasonic sensor HC-SR04

Buzzer module

Jumper wires

64GB SD card

SD card adapter

Software Requirements
Raspberry Pi Imager

REAL VNC Viewer

VNC server

Advanced IP Scanner

OpenCV

SMTP libraries

Installation and Setup
1. Enable Camera Interface
bash
sudo raspi-config
Navigate to Interfacing Options > Camera and enable it.

2. Install Required Packages
bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-opencv
pip install smtplib
3. Clone this Repository
bash
git clone https://github.com/Saptakcodes/FaceRecognition.git
cd contactless-iot-doorbell
Project Structure
text
contactless-iot-doorbell/
├── main.py                # Main program script
├── face_detection.py       # Face detection module
├── face_recognition.py     # Face recognition module
├── email_notification.py   # Email notification handler
├── requirements.txt        # Python dependencies
├── haarcascades/           # Haar cascade files
├── known_faces/            # Database of known faces
└── README.md               # This file
Usage
Connect all hardware components as per the circuit diagram

Run the main program:

bash
python3 main.py
The system will:

Detect visitors using the ultrasonic sensor

Capture images when someone approaches

Attempt face recognition

Send email notifications for unrecognized visitors

Sound the buzzer

Features
Contactless visitor detection

Face recognition to identify known visitors

Email notifications with visitor images

Configurable detection range (default: 80cm)

Rate-limited email notifications to prevent spam

Future Scope
Advanced facial recognition with AI

Real-time video streaming

Two-way audio communication

Integration with smart home systems

Mobile app development

Enhanced security features

Cloud integration

Troubleshooting
If camera isn't detected, ensure it's properly enabled in raspi-config

For SMTP issues, check your email provider's app password requirements

Adjust ultrasonic sensor sensitivity if detection is inconsistent

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
OpenCV community for computer vision libraries

Raspberry Pi Foundation for hardware support

Python community for various supporting libraries

