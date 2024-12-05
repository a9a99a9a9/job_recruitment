from flask import Flask
from app.routes.auth_routes import auth_routes
from app.routes.job_routes import job_routes
from app.routes.application_routes import application_routes
from app.routes.bookmark_routes import bookmark_routes
import os

def create_app():
    # Flask 앱 생성
    app = Flask(__name__)

    # 환경 변수 설정
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'your_secret_key')  # 기본 SECRET_KEY
    app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:3000/')  # MongoDB URI

    # 블루프린트 등록
    app.register_blueprint(auth_routes, url_prefix='/auth')  # 회원 관리 API
    app.register_blueprint(job_routes, url_prefix='/jobs')  # 채용 공고 API
    app.register_blueprint(application_routes, url_prefix='/applications')  # 지원 관리 API
    app.register_blueprint(bookmark_routes, url_prefix='/bookmarks')  # 북마크 API

    return app
