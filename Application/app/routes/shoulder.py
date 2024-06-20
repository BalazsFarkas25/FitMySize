from flask import Blueprint, request, render_template, jsonify
from app.helpers.evaluation import evaluate_shoulders
import cv2
import numpy as np
import base64

shoulder_bp = Blueprint("shoulder", __name__)

@shoulder_bp.route('/detect_shoulder', methods=['POST'])
def detect_shoulder():
    data = request.json['data']
    img_data = base64.b64decode(data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    shoulder_length, keypoints = evaluate_shoulders(image)
    return jsonify({"shoulder": {"result":shoulder_length, "keypoints": keypoints}}), 200