import os
from ultralytics import YOLO
from matplotlib import pyplot as plt

model = YOLO('./runs/pose/train2/weights/best.pt')

source = "/Users/balazsfarkas/LEARN/BSC/To_Send/edge-raw.jpg"
results = model(source)
keypoints_in_pixel = results[0].keypoints.xy
print(keypoints_in_pixel)
# im = plt.imread(source)
# implot = plt.imshow(im)
# for p,q in keypoints_in_pixel[0]:
#     x_cord = p
#     y_cord = q
#     plt.scatter([x_cord], [y_cord])
# plt.show()
