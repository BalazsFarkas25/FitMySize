import cv2
import os
import math
import csv
import numpy as np

def get_body_dataset(dir_path):
    file_list = os.listdir(dir_path)
    return file_list

def get_height_info(picture_name):
    """
    Helper function retrieves the height in cm from the metadata csv files

    :param picture_name: Name of the image
    """
    file = open("../../Annotation/subject_to_photo_map.csv", 'r')
    subject_id = "NONE"
    for row in csv.reader(file):
        if row[1] == picture_name.split(".")[0]:
            subject_id = row[0]
            break

    print(subject_id)
    file = open("../../Annotation/hwg_metadata.csv", 'r')
    reader = csv.DictReader(file)
    for row in reader:
        if row["subject_id"] == subject_id:
            return row["height_cm"]


def resize_img_and_save(image_name, dir_path, height):
    """
    This function resizes the training image (720 * 960) to a specific size
    based on the height value, to differentiate between shorter and taller people on the image
    This is needed, bacause in the training dataset every people have somewhat the same size on the image
    
    :param image_name: Name of the image
    :param dir_path: Directory, where the image is stored
    :param height: height (cm) value of person on image
    """
    max_height_cm = 200
    image = cv2.imread(f"{dir_path}/{image_name}")
    
    down_height = int(960*(height/max_height_cm))
    sf = down_height / 960
    down_width = int(720 * sf)
    
    down_points = (down_width, down_height)
    resized_down = cv2.resize(image, down_points, interpolation= cv2.INTER_LINEAR)
    cv2.imwrite(f"./dataset/{image_name}", resized_down) 

if __name__ == '__main__':
    dataset_dir = "../../Annotation/dataset/train/images"

    list_of_images = get_body_dataset(dataset_dir)
    for curr_img in list_of_images:
        height = get_height_info(curr_img)
        resize_img_and_save(curr_img,dataset_dir, float(height))