## Training
This folder contains 2 important sections

## Keypoints
In this folder, you'll find the script that trains a Yolo-based model on my custom dataset.

Yolov8 is the biggest and best ML model for general pose detection. 

At this point, I only ran a simple training without adjusting the hyperparameters. See [train.py](./Keypoints/train.py).


#### Custom training
To run the training do ```pip install -r requirements.txt && python train.py```

This will output the latest custom training and model to runs/.

I kept some example training results for reference.

#### Prediction
To get an example prediction run

```python predict.py```

## Regression Model
After training a custom model, I created a regresson model with "X" values being the pixel distance between the keypoints (e.g. Shoulder keypoints) and dependent ("Y") values being the actual cm value retreived from the known metadata [csv files](../Annotation).

To build the dataset with these columns run:

- ```pip install -r requirements.txt```

- ```python resize_image.py```

This script resizes the images based on the height of the person on the image.
This is only needed, because I observed that the training images are normalized. 156cm person and 187cm person have the same size on the image. Without resizing, the cm value mapping does not make sense.

This is only needed for the training data, as the user will be properly guided from what angle and distance to take the picture.


- ```python create_dataset.py```

See output as [keypoints.csv](./Regression/keypoints.csv) and [height.csv](./Regression/height.csv)

### Jupiter Notebook
You can open this [notebook](./Regression/Regression.ipynb) and see the result of the Regression model.