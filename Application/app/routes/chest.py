from flask import Blueprint, request, render_template, jsonify
from app.helpers.evaluation import evaluate_chest
import cv2
import numpy as np
import base64

chest_bp = Blueprint("chest", __name__)

@chest_bp.route('/detect_chest', methods=['POST'])
def detect_chest():
    data = request.json['data']
    img_data = base64.b64decode(data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    chest_length = evaluate_chest(img)
    return jsonify({"chest": {"result":chest_length}}), 200