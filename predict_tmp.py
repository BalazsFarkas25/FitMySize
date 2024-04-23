import os
from ultralytics import YOLO

model = YOLO('./runs/pose/train2/weights/best.pt')

source = "./unannotated_dataset/train/mask/0fa7dbd7ca0e34a14977e9c31d7a0427.png"
model.predict(source, save=True, imgsz=960, conf=0.5)