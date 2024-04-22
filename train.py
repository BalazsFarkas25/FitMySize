import os
from ultralytics import YOLO


# pretrained model. This will serve as a base for my custom training
model = YOLO('yolov8n-pose.pt')
model.train(data='./data.yaml', epochs=1, imgsz=960, device='cpu')


