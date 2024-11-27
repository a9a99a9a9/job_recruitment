from dotenv import load_dotenv
import os

# .env 파일을 로드하여 환경 변수 설정
load_dotenv()

# 환경 변수로 MongoDB URI를 설정
MONGO_URI = os.getenv("MONGO_URI")

# 필요한 경우 다른 환경 변수를 로드
SECRET_KEY = os.getenv("SECRET_KEY")
