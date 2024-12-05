from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

def create_app():
    # .env 파일 로드
    load_dotenv()

    app = Flask(__name__)
    CORS(app)  # CORS 활성화

    # 환경 변수 설정
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'your_secret_key')
    app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:3000/')

    return app
