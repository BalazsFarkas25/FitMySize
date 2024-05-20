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
    """
    Helper function retrieves the requested measurement in cm from the metadata csv files
    
    :param measurement_id: Id of the measurement point
    :param picture_name: Name of the image
    """

    # First retrieve subject id based on photo name
    file = open("../../Annotation/subject_to_photo_map.csv", 'r')
    subject_id = "NONE"
    for row in csv.reader(file):
        if row[1] == picture_name.split(".")[0]:
            subject_id = row[0]
            break

    print(subject_id)

    # get measurement info for specific subject id
    file = open("../../Annotation/measurements.csv", 'r')
    reader = csv.DictReader(file)
    for row in reader:
        if row["subject_id"] == subject_id:
            return row[measurement_id]

def get_height_info(picture_name):
    """
    Helper function retrieves the height in cm from the metadata csv files
    Currenlty I don't use get_measurement_info function for this, because
    The height info is stored in a different csv metadata file-
    TODO refactor in the future

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
    
def get_prediction_value(picture_name,dataset_dir, model_path, measurement_id):
    """
    This function runs a detection with the custom trained ML model, to get pixel info of 
    the bounding box and keypoints 
    
    :param picture_name: Name of the image
    :param dataset_dir: Directory where the image is stored
    :param model_path: Location of the trained model
    :param measurement_id: Keypoint you want to check (shoulder, height ...etc)

    """
    model = YOLO(model_path)
    source = f"{dataset_dir}/{picture_name}"
    results = model(source)

    if measurement_id == "height":
        bbox = (results[0].boxes)
        # height
        return bbox.xywh[0][3].item()
    else:
        keypoints_in_pixel = (results[0].keypoints.xy)[0]
        return keypoints_in_pixel[measurement_mapping[measurement_id]:measurement_mapping[measurement_id]+2]
    

def calculate_pixel_distance(keypoint_coordinates):
    return math.sqrt(math.pow(keypoint_coordinates[1][0]-keypoint_coordinates[0][0],2)
                     +math.pow(keypoint_coordinates[1][1]-keypoint_coordinates[0][1],2))

if __name__ == '__main__':
    #dataset_dir = "../../Annotation/dataset/train/images"
    dataset_dir = "./dataset"
    model_path = "../Keypoints/runs/pose/train2/weights/best.pt"

    ####################################################################################
    #################### GET MEASUREMENT POINTS MAPPING ################################
    ####################################################################################

    
    list_of_images = get_body_dataset(dataset_dir)
    
    for curr_measurement_point in measurement_mapping.keys():
        X_values = []
        Y_values = []
    
        for curr_img in list_of_images:
            if(curr_img.endswith('.png')):
                # get known cm value
                measurement_cm = get_measurement_info(curr_measurement_point,curr_img)
                # get model's keypoint prediction
                keypoint_coordinates = get_prediction_value(curr_img,dataset_dir,model_path,curr_measurement_point)
                # calculate pixel distance from keypoint coordinates
                pixel_distance = calculate_pixel_distance(keypoint_coordinates)
                
                X_values.append(pixel_distance)
                Y_values.append(measurement_cm)
        
        df = pd.DataFrame({'Keypoint Pixel Distance':X_values, 'CM Distance':Y_values}) 
        df.to_csv(f'./PixelToCmMapping/{curr_measurement_point}.csv', index=False) 