---
title: Deep Fake Detector
emoji: 🕵️
colorFrom: blue
colorTo: red
sdk: docker
pinned: false
---

# 🕵️‍♂️ AI Deepfake & Image Forensics Detector

An advanced AI-powered web application designed to detect deepfakes, AI-generated images, and digital manipulations.

## 🚀 Features
- **CNN-based Face Analysis:** Detects manipulated faces using a Deep Learning model (TensorFlow/Keras).
- **Image Forensics (ELA & Noise Analysis):** Analyzes Error Level Analysis and microscopic sensor noise to detect AI generation (Midjourney, DALL-E) or heavy editing.
- **Metadata (EXIF) Extraction:** Scans for hidden software signatures in the image file.
- **MLOps Integration:** Continuous model monitoring and prediction logging using **MLflow**.
- **Modern UI:** Built with React.js and Tailwind CSS for a futuristic cyberpunk/forensic vibe.

## 🛠️ Tech Stack
- **Frontend:** React, Vite, Tailwind CSS, Framer Motion
- **Backend:** Python, Flask, OpenCV, TensorFlow/Keras
- **MLOps:** MLflow
- **Deployment:** Docker, Hugging Face Spaces

## 🌐 Live Demo
Check out the live working application here: 
👉 [Deep Fake Detector Live App](https://harshit4545-deep-fake-detector.hf.space)

## 💻 How to Run Locally

### 1. Start the Backend
Run the following commands to activate the environment and start the Flask API:
`env\Scripts\activate`
`pip install -r requirements.txt`
`python app.py`

### 2. Start the Frontend (New Terminal)
Run the following commands to start the React UI:
`cd forensic-frontend`
`npm install`
`npm run dev`

### 3. Open the MLOps Dashboard (New Terminal)
Run the following command to see the model tracking logs:
`env\Scripts\activate`
`mlflow ui --port 8080`
Then visit `http://localhost:8080` in your browser.
