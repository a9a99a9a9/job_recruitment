import jwt
from datetime import datetime, timedelta, timezone

# 비밀 키 (환경 변수 또는 config 파일로 관리 권장)
SECRET_KEY = "your_secret_key"

# 액세스 토큰 생성
def create_access_token(user_id, expires_in=1):
    """
    액세스 토큰 생성
    :param user_id: 사용자 ID
    :param expires_in: 만료 시간 (기본 1시간)
    :return: JWT 액세스 토큰
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=expires_in),
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# 액세스 토큰 검증
def decode_access_token(token):
    """
    액세스 토큰 검증
    :param token: JWT 액세스 토큰
    :return: user_id (유효한 경우), None (유효하지 않은 경우)
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None  # 만료된 토큰
    except jwt.InvalidTokenError:
        return None  # 잘못된 토큰

# 리프레시 토큰 생성
def create_refresh_token(user_id, expires_in=7):
    """
    리프레시 토큰 생성
    :param user_id: 사용자 ID
    :param expires_in: 만료 시간 (기본 7일)
    :return: JWT 리프레시 토큰
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(days=expires_in),
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# 리프레시 토큰 검증
def decode_refresh_token(token):
    """
    리프레시 토큰 검증
    :param token: JWT 리프레시 토큰
    :return: user_id (유효한 경우), None (유효하지 않은 경우)
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None  # 만료된 토큰
    except jwt.InvalidTokenError:
        return None  # 잘못된 토큰