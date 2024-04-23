import cv2
import numpy as np
from rembg import remove 

def preprocessImg(image):
    # use 3rd party library to remove bg
    body_shape = remove(image) 
    
    # create black - white shyluette
    body_shape = np.array(body_shape)
    alpha_channel = body_shape[:,:,3]
    mask = cv2.threshold(alpha_channel, 128,255, cv2.THRESH_BINARY)[1]
    mask = cv2.bitwise_not(mask)
    body_shape[mask != 0] = [0,0,0,255]
    body_shape[mask == 0] = [255,255,255,255]

    # Resize image based on training dataset: height ~960px
    h,w = body_shape.shape[:2]
    sf = 960/ h
    new_w = int(w * sf)
    resized_img = cv2.resize(body_shape, (new_w, 960))

    return resized_img