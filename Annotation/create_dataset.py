import os
from ultralytics import YOLO
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def visualize_annotation(image_path, annotation_path):
    """
    visualize_annotation function plots the image with the keypoints for visual feedback.
    This helps the developer to check, during converting COCO annotation to YOLO txt format,
    all the normalization and arithmetic steps were computed properly
    
    :param image_path: Path of the image you want to plot on
    :param annotation_path: Path of the generated annotation for the specific image
    """

    image = plt.imread(image_path)
    fig, ax = plt.subplots(1)
    ax.imshow(image)

    # Read annotation from file
    with open(annotation_path, "r") as f:
        annotation = f.readline().strip().split()
        class_id, center_x, center_y, bbox_width, bbox_height, *keypoints = map(float, annotation)

        # The first 4 elements are the bounding box values
        width, height = image.shape[1], image.shape[0]
        x_min = (center_x - bbox_width/2) * width
        y_min = (center_y - bbox_height/2) * height
        bbox_width *= width
        bbox_height *= height

        # Plot bounding box
        bbox_rect = patches.Rectangle((x_min, y_min), bbox_width, bbox_height, linewidth=2, edgecolor='r', facecolor='none')
        ax.add_patch(bbox_rect)

        # The rest are keypoints (x,y coordinates)
        for i in range(0, len(keypoints), 2):
            x_keypoint = keypoints[i] * width
            y_keypoint = keypoints[i+1] * height
            ax.plot(x_keypoint, y_keypoint, 'bo')

    # Show plot
    plt.show()


def folder_contains_file(folder_path, file_name):
    """
    Helper function to make sure image exists
    This helps to keep track which images got labels and which got skipped.
    
    :param folder_path: Path of the folder
    :param file_name: Name of the image
    """
    file_path = os.path.join(folder_path, file_name)
    print(file_path)
    isThere = os.path.isfile(file_path)
    return isThere


def coco_to_yolo(coco_data, image_folder):
    """
    Custom created function to convert JSON annotation to per file txt YOLO annotation
    I am using COCO annotatior to manually annotate my training images. This annotator exports
    one giant JSON file which contains list of images and it's keypoints, bboxes...etc
    In this function I iterate trough these values and create 1 txt YOLO format per image
    
    :param coco_data: JSON document
    :param image_folder: Subset (or all) of images in folder
    """
    yolov7_annotations = []

    # every image has 9 annotation elements (4*2 keypoints + 1 bounding box around the body)
    for i in range(0, len(coco_data["annotations"]), 9):
        image_annotations = coco_data["annotations"][i:i+9]

        # get respective image_info
        # every annotation element contains an image_id, this function finds the respective image name
        image_info = next(image for image in coco_data["images"] if image["id"] == image_annotations[0]["image_id"])
        
        # checks if the folder with a subset of images contains the specific image from COCO JSON file
        if not folder_contains_file(image_folder, image_info['file_name']): 
            print(f"WARNING: Not found: {image_info['file_name']} --> SKIPPING")
            continue
        
        width = image_info["width"]
        height = image_info["height"]

        # Extract bounding box coordinates
        bbox = image_annotations[0]["bbox"]
        x_min, y_min, bbox_width, bbox_height = bbox
        x_max = x_min + bbox_width
        y_max = y_min + bbox_height

        # Calculate bounding box center
        center_x = (x_min + x_max) / (2 * width)
        center_y = (y_min + y_max) / (2 * height)

        # Normalize bounding box dimensions
        bbox_width /= width
        bbox_height /= height
        
        # Iterate through keypoints, normalize it
        # we don't need 3rd component (x,y,v) v=visibility
        # assume all keypoints are visible
        normalized_keypoints = []
        for annotation in image_annotations[1:]:
            keypoints = annotation["keypoints"]
            x_keypoint, y_keypoint, _ = keypoints

            x_keypoint /= width
            y_keypoint /= height

            normalized_keypoints.append(x_keypoint)
            normalized_keypoints.append(y_keypoint)
 
        # assemble YOLO txt format       
        yolov7_annotation = f"0 {center_x:.6f} {center_y:.6f} {bbox_width:.6f} {bbox_height:.6f} {' '.join(map(str, normalized_keypoints))}"
        yolov7_annotations.append(yolov7_annotation)

        # save to txt file
        labels_folder = f"{'/'.join(image_folder.split('/')[:-1])}/labels"
        with open(f"{labels_folder}/{image_info['file_name'].split('.')[0]}.txt", "w") as f:
            for annotation in yolov7_annotations:
                f.write(annotation + "\n")
        yolov7_annotations = []


if __name__ == '__main__':
    # Read COCO data from file
    with open("./COCO_ANNOTATION.json", "r") as f:
        coco_data = json.load(f)

    image_folder = "./dataset/test/images"
    #coco_to_yolo(coco_data,image_folder)

    # Check annotation
    #visualize_annotation("./dataset/train/images/0a0b4bf37aea2ee106a9e313c4cbc510.png","./dataset/train/labels/0a0b4bf37aea2ee106a9e313c4cbc510.txt")