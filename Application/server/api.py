from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from preprocessImg import preprocessImg
from PIL import Image
import base64
import io
import re


app = Flask(__name__)
cors = CORS(app)

@app.route('/getSize', methods=['POST','OPTIONS'])
@cross_origin()
def process_image():
    # remove base64 prefix from Post request
    image_data = re.sub('^data:image/.+;base64,', '',request.json.get('blob'))
    image = Image.open(io.BytesIO(base64.b64decode(image_data)))
    #Preprocessing input image for training
    preprocessed_img = preprocessImg(image)

    # Predict keypoints
    suggestedSize = 'M'
    return jsonify({'prediction': suggestedSize})

if __name__ == '__main__':
    app.run(debug=False, port=3001)
