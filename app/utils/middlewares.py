from flask import request, jsonify, g
import jwt
import os
import logging
from functools import wraps

# 로깅 설정
logger = logging.getLogger(__name__)

def token_required(f):
    """JWT 토큰 검증 미들웨어"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # 헤더에서 Authorization 토큰 추출
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(" ")[1]
            except IndexError:
                logger.warning("Authorization 헤더 형식 오류")
                return jsonify({"error": "Authorization 헤더의 형식이 잘못되었습니다. Bearer <token> 형식을 사용하세요."}), 400

        if not token:
            logger.warning("토큰이 제공되지 않음")
            return jsonify({"error": "토큰이 제공되지 않았습니다."}), 401

        try:
            # JWT 토큰 검증
            decoded_token = jwt.decode(
                token,
                os.getenv('FLASK_SECRET_KEY', 'your_secret_key'),
                algorithms=["HS256"]
            )
            # 추출된 사용자 ID를 플라스크 글로벌 객체에 저장
            g.user_id = decoded_token.get('user_id')
            if not g.user_id:
                logger.warning("토큰에 user_id가 포함되지 않음")
                return jsonify({"error": "유효하지 않은 토큰입니다."}), 401
        except jwt.ExpiredSignatureError:
            logger.warning("JWT 토큰이 만료됨")
            return jsonify({"error": "토큰이 만료되었습니다."}), 401
        except jwt.InvalidTokenError as e:
            logger.warning(f"유효하지 않은 토큰: {str(e)}")
            return jsonify({"error": "유효하지 않은 토큰입니다."}), 401

        # 데코레이터로 전달된 원래 함수 실행
        return f(*args, **kwargs)

    return decorated
