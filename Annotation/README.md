## Annotaion Section
For the project, the first important part is the annotation. I have a 6,000-image body [dataset](https://aws.amazon.com/marketplace/pp/prodview-w3762gcflmhzk) (unannotated). From these, in this round, I used 100 images. See the [dataset](./dataset) folder.


### COCO annotation.
To annotate these images, I used the COCO annotator tool. This tool is simple software that can be installed on macOS. 

I defined 5 annotaion groups.

- body (bounding box around body)
- shoulder (2x keypoints)
- chest (2x keypoints)
- waist (2x keypoints)
- hip (2x keypoints)

After annotating all the images, I exported the labels as JSON (COCO format) see [COCO_ANNOTATION.json](./COCO_ANNOTATION.json).

### Converting annotation format to Yolo txt
For the training, I chose a YOLO base model (read in detail in the [Training](../Training) folder)

This uses a txt labeling approach, where every row in a txt file contains 

- class_id
- bounding box (x,y,w,h)
- keypoints (x,y)

See labels in [dataset/train/labels](./dataset/train/labels)

run ```pip install -r requirements.txt && python create_dataset.py```

This script outputs 1 txt label file/image into a desired folder based on the COCO annotation json file.

## Note
You will also find the [data.yaml](./data.yaml) file in this folder. This is needed for the training and some CSV files to retrieve metadata about the specific training images. This is needed to compare pixel data with a ground truth (cm) value (read more in [Regression](../Training/Regression))
