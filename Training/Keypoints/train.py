import os
from ultralytics import YOLO


# pretrained model. This will serve as a base for my custom training
model = YOLO('yolov8n-pose.pt')
model.train(data='./Annotation/data.yaml', epochs=100, imgsz=960, device='cpu')