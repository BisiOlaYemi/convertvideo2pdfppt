import cv2
import os
from ..config import settings

async def extract_frames(video_path: str, frame_interval: int = 30):
    """Extract frames from video at specified intervals"""
    if not os.path.exists(settings.FRAMES_DIR):
        os.makedirs(settings.FRAMES_DIR)
    
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    saved_frames = []
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_count % frame_interval == 0:
            frame_path = os.path.join(settings.FRAMES_DIR, f'frame_{frame_count}.jpg')
            cv2.imwrite(frame_path, frame)
            saved_frames.append(frame_path)
            
        frame_count += 1
    
    cap.release()
    return saved_frames