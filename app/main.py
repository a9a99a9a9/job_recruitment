from flask import Flask
from app.routes.auth_routes import auth_routes
from app.routes.job_routes import job_routes
from app.routes.application_routes import application_routes
from app.routes.bookmark_routes import bookmark_routes
from app.utils.crawler import crawl_saramin, save_to_mongodb
import os
import schedule
import threading
import time
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Flask 애플리케이션 생성 함수
def create_app():
    app = Flask(__name__)

    # 환경 변수 설정
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'your_secret_key')
    app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')

    # 블루프린트 등록
    app.register_blueprint(auth_routes, url_prefix='/auth')
    app.register_blueprint(job_routes, url_prefix='/jobs')
    app.register_blueprint(application_routes, url_prefix='/applications')
    app.register_blueprint(bookmark_routes, url_prefix='/bookmarks')

    logger.info("Flask 애플리케이션 생성 및 블루프린트 등록 완료.")
    return app

# 스케줄링 작업 함수
def scheduled_task():
    try:
        logger.info("스케줄링된 작업 시작...")
        # 'python' 키워드로 5페이지 크롤링
        df = crawl_saramin('python', pages=5)
        # MongoDB에 데이터 저장
        save_to_mongodb(df)
        logger.info("스케줄링된 작업 완료.")
    except Exception as e:
        logger.error(f"스케줄 작업 중 오류 발생: {e}", exc_info=True)

# 스케줄러 설정
def start_scheduler():
    schedule.every().day.at("00:00").do(scheduled_task)  # 매일 자정 실행
    logger.info("스케줄러 시작. 매일 자정에 작업이 실행됩니다.")

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)  # 1초 대기
    except Exception as e:
        logger.error(f"스케줄러 실행 중 오류 발생: {e}", exc_info=True)

# 스케줄러를 별도 스레드로 실행
def run_scheduler_in_thread():
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()
    logger.info("스케줄러 스레드 실행 중...")

if __name__ == '__main__':
    # Flask 애플리케이션 생성
    app = create_app()

    # 스케줄러 시작
    run_scheduler_in_thread()

    # Flask 서버 실행
    try:
        logger.info("Flask 서버 시작 중...")
        app.run(debug=True, host='0.0.0.0', port=5000)  # 필요 시 포트 변경
    except Exception as e:
        logger.error(f"Flask 서버 실행 중 오류 발생: {e}", exc_info=True)
