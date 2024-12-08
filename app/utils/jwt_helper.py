import jwt
from datetime import datetime, timedelta, timezone
import os

# 비밀 키 (환경 변수 또는 config 파일로 관리 권장)
SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "your_secret_key")

# 토큰 블랙리스트 (예: Redis 또는 MongoDB와 연동 가능)
BLACKLIST = set()

# 액세스 토큰 생성
def create_access_token(user_id, expires_in=1):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=expires_in),
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# 액세스 토큰 검증
def decode_access_token(token):
    try:
        if token in BLACKLIST:
            return None  # 블랙리스트에 있는 토큰
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None  # 만료된 토큰
    except jwt.InvalidTokenError:
        return None  # 잘못된 토큰

# 리프레시 토큰 생성
def create_refresh_token(user_id, expires_in=7):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(days=expires_in),
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# 리프레시 토큰 검증
def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None  # 만료된 토큰
    except jwt.InvalidTokenError:
        return None  # 잘못된 토큰

# 블랙리스트에 토큰 추가
def add_to_blacklist(token):
    BLACKLIST.add(token)

# 블랙리스트 상태 확인
def is_blacklisted(token):
    return token in BLACKLIST
