from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from flask_pymongo import PyMongo
from flasgger import Swagger, swag_from
import os
import logging
import signal
import sys
from apscheduler.schedulers.background import BackgroundScheduler

try:
    from app.routes.auth_routes import auth_routes
except ImportError:
    auth_routes = None
try:
    from app.routes.job_routes import job_routes
except ImportError:
    job_routes = None
try:
    from app.routes.application_routes import application_routes
except ImportError:
    application_routes = None
try:
    from app.routes.bookmark_routes import bookmark_routes
except ImportError:
    bookmark_routes = None
from app.utils.crawler import crawl_saramin, save_to_mongodb

# 로깅 설정
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# .env 파일 로드
if load_dotenv():
    logger.info(".env 파일 로드 성공")
else:
    logger.warning(".env 파일 로드 실패 또는 존재하지 않음")

# MongoDB 초기화
mongo = PyMongo()

# Flask 애플리케이션 생성 함수
def create_app():
    app = Flask(__name__)
    CORS(app)  # CORS 설정 추가

    # 환경 변수 설정
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'your_secret_key')
    app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/job_crawler')

    # MongoDB 초기화
    mongo.init_app(app)

    # Swagger 설정 (swagger.yaml 파일 경로 지정)
    swagger_template_path = os.path.join(os.path.dirname(__file__), "swagger", "swagger.yaml")
    Swagger(app, template_file=swagger_template_path)

    # 블루프린트 등록
    if auth_routes:
        app.register_blueprint(auth_routes, url_prefix='/auth')
    if job_routes:
        app.register_blueprint(job_routes, url_prefix='/jobs')
    if application_routes:
        app.register_blueprint(application_routes, url_prefix='/applications')
    if bookmark_routes:
        app.register_blueprint(bookmark_routes, url_prefix='/bookmarks')

    # 상태 확인용 헬스체크 엔드포인트
    @app.route('/health', methods=['GET'])
    @swag_from({
        "responses": {
            200: {
                "description": "Flask 앱 상태 확인",
                "examples": {
                    "application/json": {
                        "status": "running",
                        "message": "Flask 앱이 정상적으로 실행 중입니다."
                    }
                }
            }
        }
    })
    def health_check():
        return jsonify({"status": "running", "message": "Flask 앱이 정상적으로 실행 중입니다."}), 200

    # 루트 경로 처리
    @app.route('/', methods=['GET'], strict_slashes=False)
    def root():
        return (
            "<h1>Flask 앱이 정상적으로 실행 중입니다!</h1>"
            "<p>추가 경로: <a href='/health'>/health</a></p>"
            "<p>API 문서 확인: <a href='/apidocs'>Swagger UI</a></p>"
        ), 200

    logger.info("Flask 애플리케이션 생성 및 블루프린트 등록 완료.")
    return app

# 스케줄링 작업 함수
def scheduled_task():
    try:
        logger.info("스케줄링된 작업 시작: 사라민 크롤링 수행")
        df = crawl_saramin('python', pages=5)  # 'python' 키워드로 5페이지 크롤링
        logger.info(f"크롤링된 데이터 수: {len(df)}")
        save_to_mongodb(df)  # MongoDB에 데이터 저장
        logger.info("스케줄링된 작업 완료 및 MongoDB 저장 완료.")
    except Exception as e:
        logger.error(f"스케줄 작업 중 오류 발생: {e}", exc_info=True)

# 스케줄러 시작
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_task, 'cron', hour=0, minute=0)  # 매일 자정 실행
    scheduler.start()
    logger.info("스케줄러 시작. 매일 자정에 작업이 실행됩니다.")
    return scheduler

# 서버 종료 처리
def shutdown_server(_signal, _frame):
    logger.info("서버 종료 요청 수신됨.")
    sys.exit(0)

if __name__ == '__main__':
    app = create_app()
    job_scheduler = start_scheduler()

    signal.signal(signal.SIGINT, shutdown_server)
    signal.signal(signal.SIGTERM, shutdown_server)

    try:
        logger.info("Flask 서버 시작 중...")
        app.run(debug=True, host='0.0.0.0', port=int(os.getenv('FLASK_RUN_PORT', 5001)))
    except Exception as e:
        logger.error(f"Flask 서버 실행 중 오류 발생: {e}", exc_info=True)
