from flask import Flask
from app.routes.camera import camera_bp
from app.routes.shoulder import shoulder_bp
from app.routes.torso import torso_bp

app = Flask(__name__)

app.register_blueprint(camera_bp)
app.register_blueprint(shoulder_bp)
app.register_blueprint(torso_bp)