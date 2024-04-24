import os
from ultralytics import YOLO
from matplotlib import pyplot as plt

model = YOLO('./runs/pose/train2/weights/best.pt')

source = "../../Annotation/dataset/train/images/0a44f2ea5ca1b122ab4a2b979ed72be4.png"
results = model(source)
keypoints_in_pixel = results[0].keypoints.xy
print(keypoints_in_pixel)
im = plt.imread(source)
implot = plt.imshow(im)
for p,q in keypoints_in_pixel[0]:
    x_cord = p
    y_cord = q
    plt.scatter([x_cord], [y_cord])
plt.show()
