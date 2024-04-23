from ultralytics import YOLO
import pandas as pd 
import os
import csv
import math

measurement_mapping  = { "shoulder-breadth":0,"chest":2,"waist":4,"hip":6 }

def get_body_dataset(dir_path):
    file_list = os.listdir(dir_path)
    return file_list

def get_measurement_info(measurement_id, picture_name):
    file = open("../../Annotation/subject_to_photo_map.csv", 'r')
    subject_id = "NONE"
    for row in csv.reader(file):
        if row[1] == picture_name.split(".")[0]:
            subject_id = row[0]
            break

    print(subject_id)
    file = open("../../Annotation/measurements.csv", 'r')
    reader = csv.DictReader(file)
    for row in reader:
        if row["subject_id"] == subject_id:
            return row[measurement_id]
    
def get_prediction_value(picture_name,dataset_dir, model_path, measurement_id):
    model = YOLO(model_path)
    source = f"{dataset_dir}/{picture_name}"
    results = model(source)
    keypoints_in_pixel = (results[0].keypoints.xy)[0]
    return keypoints_in_pixel[measurement_mapping[measurement_id]:measurement_mapping[measurement_id]+2]

def calculate_pixel_distance(keypoint_coordinates):
    return math.sqrt(math.pow(keypoint_coordinates[1][0]-keypoint_coordinates[0][0],2)
                     +math.pow(keypoint_coordinates[1][1]-keypoint_coordinates[0][1],2))

if __name__ == '__main__':
    dataset_dir = "../../Annotation/dataset/train/images"
    model_path = "../Keypoints/runs/pose/train2/weights/best.pt"
    measurement_id = "shoulder-breadth"

    X_values = []
    Y_values = []
    list_of_images = get_body_dataset(dataset_dir)
    for curr_img in list_of_images:
        # get known cm value
        measurement_cm = get_measurement_info(measurement_id,curr_img)
        # get model's keypoint prediction
        keypoint_coordinates = get_prediction_value(curr_img,dataset_dir,model_path,measurement_id)
        # calculate pixel distance from keypoint coordinates
        pixel_distance = calculate_pixel_distance(keypoint_coordinates)
        print(measurement_cm)
        Y_values.append(measurement_cm)
        print(pixel_distance)
        X_values.append(pixel_distance)
    
    df = pd.DataFrame({'Pixel Distance':X_values, 'CM Distance':Y_values}) 
    df.to_csv('temp.csv', index=False) 