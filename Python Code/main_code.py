# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 18:14:31 2024

@author: Henry Gunawan, Dimitris Mantas, Sam Parijs
"""

from ultralytics import YOLO
import object_counter
import cv2

use_camera = True  #change to True is using camera, change to False if not using camera
camera_id = 0  # Change to the ID of the camera
video_path = r'C:\Users\Henry\Delft University of Technology\PLASTIC - General\FINAL SUBMISSION\Dataset\Video\video-3.mov'
model_path = r'C:\Users\Henry\Delft University of Technology\PLASTIC - General\FINAL SUBMISSION\Fix ModeL\yolov8s\weights\best.pt'
output_video_path = r'C:\Users\Henry\Delft University of Technology\PLASTIC - General\FINAL SUBMISSION\Dataset\Output Video\output_video.avi'

model = YOLO(model_path)

if use_camera:
    cap = cv2.VideoCapture(camera_id)
else:
    cap = cv2.VideoCapture(video_path)

assert cap.isOpened(), "Error reading video source"

# Set width and height based on the video source
if use_camera:
    w, h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
else:
    w, h = 1920, 1080  # For video files, set to 1920x1080

fps = int(cap.get(cv2.CAP_PROP_FPS))

# Define line points
line_points = [(1400, 0), (1400, 1080)]

# Video writer
video_writer = cv2.VideoWriter(output_video_path,
                               cv2.VideoWriter_fourcc(*'mp4v'),
                               fps,
                               (w, h))

# Init Object Counter
counter = object_counter.ObjectCounter()
counter.set_args(view_img=True,
                 reg_pts=line_points,
                 classes_names=model.names,
                 draw_tracks=True)

while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        counter.export_to_csv()  # Export to CSV
        break
    im0 = cv2.resize(im0, (w, h))
    tracks = model.track(im0, persist=True, conf=0.1)
    
    im0 = counter.start_counting(im0, tracks)
    video_writer.write(im0)
    
    if cv2.waitKey(1) & 0xFF == 27:  # Check for ESC key
        print("ESC key pressed. Exiting.")
        counter.export_to_csv()  # Export to CSV when ESC is pressed
        break

cap.release()
video_writer.release()
cv2.destroyAllWindows()
