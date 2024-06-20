## Application Section

I implemented a simple Front-End and Server part, to create a user-friendly option to showcase the Cloth size suggestion process.

The flask backend with base route serves the html file as UI. In addition to this there are 2 more endpoints /detect-shoulder and /detect_chest that are used internally during detection process.

## Run Service
run ```pip install -r requirements.txt && flask run --port=3000 --debug```