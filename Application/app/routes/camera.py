from flask import Blueprint, render_template

camera_bp = Blueprint("camera", __name__)

@camera_bp.route('/')
def index():
    return render_template('index.html')
