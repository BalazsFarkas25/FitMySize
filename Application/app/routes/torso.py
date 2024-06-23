from flask import Blueprint, request, render_template, jsonify
from app.helpers.evaluation import evaluate_torso
import cv2
import numpy as np
import base64

torso_bp = Blueprint("torso", __name__)

@torso_bp.route('/detect_torso', methods=['POST'])
def detect_torso():
    data = request.json['data']
    user_height = request.json['userInput']
    img_data = base64.b64decode(data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    torso_length = evaluate_torso(img,int(user_height))
    return jsonify({"torso": {"result":torso_length}}), 200