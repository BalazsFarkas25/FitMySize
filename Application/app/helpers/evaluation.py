import os
import math
import pandas as pd 
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import uuid

def find_body_height(array):
    first_index = None
    last_index = None

    # Find the first occurrence of the value
    for i, element in enumerate(array):
        if element != -1:
            first_index = i
            break

    # Find the last occurrence of the value
    for i in range(len(array) - 1, -1, -1):
        if array[i] != -1:
            last_index = i
            break

    return last_index-first_index

def find_max_subarray_with_elements_ge_1(arr, max_zero_tolerance = 3):
    tolerance = max_zero_tolerance
    max_start = 0
    max_len = 0

    current_start = 0
    current_len = 0

    for i in range(len(arr)):
        if (arr[i] >= 1):
            if current_len == 0:
                current_start = i
            current_len += 1
        elif (arr[i]>=-2 and tolerance != 0):
            tolerance-= 1
            if current_len == 0:
                current_start = i
            current_len += 1
        else:
            tolerance = max_zero_tolerance
            if current_len > max_len:
                max_len = current_len
                max_start = current_start
            current_len = 0

    # Check the last subarray
    if current_len > max_len:
        max_len = current_len
        max_start = current_start

    return list(range(max_start,max_start+max_len+1))


def find_border_non_negative_index(array, startingFromEnd):
    if startingFromEnd:
        for i in range(len(array) - 1, -1, -1):
            if array[i] != -1:
                return i
        return -1
    else:
        for i in range(len(array)):
            if array[i] != -1:
                # mirror values in case of left side
                # Make the middle of the body (end of the left side) 0-> index 358 is widht-358-> X relative to middle of body
                return len(array)-i
        return -1

def get_white_contour_of_half_bodies(image):
    _, width = image.shape
    left_half = image[:, :width // 2]
    right_half = image[:, width // 2:]

    return left_half,right_half


def find_contour_pixels(binary_half,isRightSide):
    contour_pixels = []
    for row in range(binary_half.shape[0]):
        white_pixels = np.where(binary_half[row] == 255,binary_half[row],-1)

        if white_pixels.size > 0:
            last_white_pixel = find_border_non_negative_index(white_pixels, startingFromEnd = isRightSide)
            contour_pixels.append(last_white_pixel)
    return contour_pixels

def find_shoulder_coordinate(contour_white_pixel,half_body, isRightSide, window_size=25, isDebug=False):
    # Calculate the differences between consecutive elements within the window
    differences = np.diff(contour_white_pixel)
    gradual_jump_indices = []
    print(gradual_jump_indices)
    print(differences)
    gradual_jump_indices = find_max_subarray_with_elements_ge_1(differences)

    x_keypoint = []
    y_keypoint = gradual_jump_indices
    
    if(isRightSide):
        x_keypoint = [contour_white_pixel[y] for y in gradual_jump_indices]

        if(isDebug):
            fig, ax = plt.subplots(1, figsize=(12, 8))
            ax.imshow(half_body)
            for y in gradual_jump_indices:
                ax.plot(contour_white_pixel[y], y, 'bo',markersize=3)
            plt_name = str(uuid.uuid4()) + '.png'
            plt.savefig(f'./debug/{plt_name}')
            plt.close()
    else:
        x_keypoint = [half_body.shape[1] - contour_white_pixel[y] for y in gradual_jump_indices]
        if(isDebug):
            fig, ax = plt.subplots(1, figsize=(12, 8))
            ax.imshow(half_body)
            for y in gradual_jump_indices:
                ax.plot(half_body.shape[1]-contour_white_pixel[y], y, 'bo',markersize=3)
            plt_name = str(uuid.uuid4()) + '.png'
            plt.savefig(f'./debug/{plt_name}')
            plt.close()

    return x_keypoint,y_keypoint

def calculate_torso_width(data):
    if len(data) == 0:
        return None

    max_element = max(data)
    max_index = data.index(max_element)

    data = data[max_index:]
    # Calculate Q1 (25th percentile) and Q3 (75th percentile)
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)

    # Calculate the IQR
    IQR = Q3 - Q1

    # Determine the lower and upper bounds
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Filter out the outliers
    filtered_data = [x for x in data if lower_bound <= x <= upper_bound]

    if len(filtered_data) == 0:
        return None

    # Calculate the average of the remaining elements
    average = np.mean(filtered_data)

    return average



def evaluate_shoulders(img):
    left_half, right_half = get_white_contour_of_half_bodies(img)
    contour_white_pixel_right = find_contour_pixels(right_half, isRightSide=True)
    contour_white_pixel_left = find_contour_pixels(left_half, isRightSide=False)
        
    x_right, y_right = find_shoulder_coordinate(contour_white_pixel_right[:len(contour_white_pixel_right)//3],half_body=right_half,isRightSide=True,isDebug=False)
    x_left, y_left = find_shoulder_coordinate(contour_white_pixel_left[:len(contour_white_pixel_left)//3],half_body=left_half,isRightSide=False,isDebug=False)

    x_right = [value + left_half.shape[1] for value in x_right]

    body_height_pixel = find_body_height(contour_white_pixel_right)
    shoulder_length = (176/body_height_pixel)*(x_right[-1]-x_left[-1])
    print("Total length of the line:", shoulder_length) 
    return shoulder_length, [x_right[-1],y_right[-1],x_left[-1],y_left[-1]]

def evaluate_chest(img):
    cv2.imwrite('./chest_test.jpg', img)
    left_half, right_half = get_white_contour_of_half_bodies(img)
    contour_white_pixel_right = find_contour_pixels(right_half, isRightSide=True)
    contour_white_pixel_left = find_contour_pixels(left_half, isRightSide=False)
    torso_width = calculate_torso_width(contour_white_pixel_right[:len(contour_white_pixel_right)//2])+calculate_torso_width(contour_white_pixel_left[:len(contour_white_pixel_left)//2])
    
    body_height_pixel = find_body_height(contour_white_pixel_right)
    print(body_height_pixel)
    print(calculate_torso_width(contour_white_pixel_right[:len(contour_white_pixel_right)//2]))
    print(calculate_torso_width(contour_white_pixel_left[:len(contour_white_pixel_left)//2]))
    torso_width = (176/body_height_pixel)*(torso_width)
    print("Total length of the line:", torso_width)
    return torso_width