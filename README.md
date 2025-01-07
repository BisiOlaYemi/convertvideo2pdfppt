# Convert Video to PPT or PDF

This project provides an API that allows users to convert a video file into either a PowerPoint presentation (PPT) or a PDF document. It is designed to simplify the process of transforming video content into static, presentation-friendly formats for easier sharing, documentation, or analysis.

# Key Features
Video to PPT: Converts video content into a PowerPoint presentation, with keyframes or selected frames captured as slides.
Video to PDF: Converts video frames into a PDF document, where each page contains an extracted frame or a series of frames from the video.
Customizable Output: Options to specify frame intervals, resolution, and formatting for the generated PPT or PDF.
Easy Integration: Can be integrated into other projects or workflows using simple API calls.

# Use Cases
Educational Content: Convert lecture or tutorial videos into presentation slides for offline use or sharing.
Documentation: Extract visual content from video files for technical reports or archives.
Presentation Preparation: Quickly generate presentation-ready slides from recorded video content.

# How It Works
Upload a video file to the API.
Choose the desired output format: PPT or PDF.
Specify optional parameters like:
Frame intervals for extraction.
Number of slides/pages.
Desired resolution or quality.
Download the generated file.

Framework: FastApi

# Setup

# Clone the repository
$ git clone https://github.com/BisiOlaYemi/convertvideo2pdfppt
$ cd convertvideo2pdfppt

# Create a virtual environment
$ python -m venv env
$ source env/bin/activate    # Windows: env\Scripts\activate

# Install the required dependencies
(env) $ pip install -r requirements.txt

# Start the FastAPI application
(env) $ uvicorn app.main:app --reload




