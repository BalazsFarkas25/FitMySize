### Training Codebase | Balazs Farkas | 12030553

This projects contains all the relevant files to train a custom keypoint detection model.

#### Installation
In this project you find a pip [requirement](./requirements.txt) file, which contains all the neccessary 3rd party packages.


```bash
pip install -r requirements.txt
```

#### Run the labeling
You may skip this step, as this is only to convert the JSON annotation file exported from COCO annotator to YOLO txt format.

I use COCO Annotator to manually add keypoints and bounding boxes for the images. This tool uses COCO annotation format, which is a giant JSON file containing all the annoations and images.

See [coco annoation file](./COCO_ANNOTATIONS.json).

1. open [create_dataset.py](create_dataset.py) and specify the image folder and your annotation file.
2. ```python python create_dataset.py ```
3. You may comment in ```visualize_annotation``` to get a sample visual feedback

#### Start the Training
After some evaluation I choose [yolov8n-pose](https://github.com/ultralytics/ultralytics/blob/main/docs/en/models/yolov8.md) (more details in my thesis).

Run ```python python train.py```

This will produce metrics under [runs](./runs). Choose the latest training folder


#### TODO
- increase dataset size to make keypoint detection more accurate. 
I already noticed, by increasing epoch size I get better results, but these models still fail to provide meaningful results. To solve this issue I am working on the maunual annotation, to get at lease 1000 annotated images.

- create regression model to compare cm values (known) with the pixel distance values, to retrieve real world metrics.

- create simple webapp to pack the whole process in a user friendly way (snapping a picture -> getting back the result)
