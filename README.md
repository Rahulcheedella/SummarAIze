## summarAIze: The AI-Powered Video Summarizer
summarAIze is a web application that automatically generates concise summaries and full transcripts from video files. Don't have time to watch a long video? Just upload it and get the gist in seconds.

## Key Features
Easy Video Upload: A clean, drag-and-drop interface to upload your video files (MP4, MOV, AVI, etc.).

Automatic Transcription: Utilizes speech recognition to convert all spoken words in the video into a full text transcript.

AI-Powered Summarization: Employs a Transformer-based deep learning model to generate an abstractive, human-like summary of the video's content.

Web-Based Interface: Fully self-contained and accessible through a simple, intuitive web page.

## How It Works
The application follows a simple three-step architecture to process your video and deliver the summary.

Frontend (Client): The user uploads a video file through the index.html webpage. The file is sent to the backend server via an API request.

Backend (Server): A Flask server receives the video file and saves it temporarily. It then calls the AI processing pipeline.

AI Pipeline (video_summarizer.py):

Audio Extraction: The audio track is extracted from the video file using moviepy.

Speech-to-Text: The audio is converted into text using the SpeechRecognition library.

Summarization: The generated transcript is fed into a Hugging Face transformers model (distilbart-cnn-12-6) to create the final summary.

The summary and transcript are sent back to the frontend to be displayed to the user.

## Tech Stack
Backend: Python, Flask

AI & Processing: Hugging Face Transformers, PyTorch, SpeechRecognition, MoviePy

Frontend: HTML, CSS, JavaScript

Core Dependencies: See requirements.txt for a full list.

## Procedure

Install all the libraries from the requirements.txt

### 🖥️ Installation

```bash
pip install -r requirements.txt
```

### 🖥️ Creation of virtual environment

```bash
python -m venv venv
```

### 🖥️ Activation of virtual environment

```bash
venv/Scripts/activate
```

### 🖥️ Run the Flask Application

```bash
python app.py
```

## Result is the Following page:

Visit the Page: https://summaraize-1hgt.onrender.com/
