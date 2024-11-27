from flask import Flask
from app.routes.job_routes import job_routes
from app.utils.crawler import crawl_saramin, save_to_mongodb
import schedule
import threading
import time

# Flask 애플리케이션 생성
app = Flask(__name__)

# 블루프린트 등록
app.register_blueprint(job_routes, url_prefix="/api")  # API URL에 /api 접두어 추가


# 스케줄링 작업 함수
def scheduled_task():
    try:
        print("스케줄링된 작업 시작...")
        df = crawl_saramin('python', pages=5)  # 크롤링 키워드와 페이지 수
        save_to_mongodb(df)  # MongoDB에 저장
        print("스케줄링된 작업 완료.")
    except Exception as e:
        print(f"스케줄링 중 에러 발생: {e}")


# 스케줄러 설정
def start_scheduler():
    schedule.every().day.at("00:00").do(scheduled_task)  # 매일 자정에 실행
    print("스케줄러 시작. 매일 자정에 작업이 실행됩니다.")
    while True:
        schedule.run_pending()
        time.sleep(1)


# 스케줄러를 별도 스레드로 실행
def run_scheduler_in_thread():
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()


if __name__ == '__main__':
    # 스케줄러 시작
    run_scheduler_in_thread()

    # Flask 서버 실행
    app.run(host="0.0.0.0", port=5000, debug=True)  # 모든 네트워크 인터페이스에서 수신 가능
