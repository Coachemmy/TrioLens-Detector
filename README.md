https://github.com/user-attachments/assets/1a438045-8795-4f57-85d3-c2a41ffea007


# TrioLens Detector

TrioLens Detector is a hand tracking project emerged from the desire to combine intuitive human-computer interaction 
with artificial intelligence.

This project leverages MediaPipe's hand tracking and Gemini AI to create a no-code interface for 
mathematical problem solving and shape recognition through intuitive gestures.

## USER CONTROLS

- Thumb up    →    Clear canvas
- Index finger extended    →    Draw
- Middle + Index fingers    →    Pause
- Middle + Index + Thumb fingers    →    Send to AI

## Deployment

Deployment of the Triolens Detector is designed to be straightforward and platform-agnostic. The application runs on local machines using the Streamlit development server, allowing users and developers to test functionality without complex setup. Deployment steps are streamlined to allow educational institutions and research labs to quickly integrate the tool into their environments.

## How to Run the App Locally 

1. Clone the repository

2. Install required packages using:

    "pip install mediapipe streamlit opencv-python cvzone pillow google-genei"

3. Place the required assets (screen1.png, screen2.png, etc., and triolens.jpg) in the working directory.

4. Run the app using:
    "streamlit run main.py"
5. Enjoy the the TrioLens detection.
