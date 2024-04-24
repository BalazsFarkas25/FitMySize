### Training Codebase | Balazs Farkas | 12030553

Please read specific folder's Readme to understand what different parts do in more detail.

## Process
- Annotate images
- Train Keypoint Detection model
- Create Regression model to convert pixel distance to cm value
- Application to showcase workflow


## Changelog
2024-04-24

Achieved

- setup whole workflow POC
- Annotated 100 sample images to train first POC model
- Trainied first example custom models
- Created regression model based on cm & pixel values
- Created Application for user friendly testing (no real suggestion returned yet)
- Created all the steps of the workflow, to validate project idea
- Created evaluation metrics to see how good the model predicts

Conclusions:

- Training dataset not big enough. POC done -> increase dataset
- I have to train better keypoint detection model with more data because regression model does not show linearity (R2 = -0.26) between cm value and pixel distance value.
- These were expected, as the training was done on a really small dataset


2024-03-26

Achieved

- [Project kick-off document](https://docs.google.com/document/d/1puc7ISEr8Z04BxxYuRpCgMbOrizoeGfTrX2ffYIyr1U/edit)