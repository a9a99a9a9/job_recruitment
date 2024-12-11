from flask import Blueprint, request, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.utils.jwt_helper import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    add_to_blacklist
)
from app.utils.middlewares import token_required
import re
from datetime import datetime

auth_routes = Blueprint('auth', __name__)

# 응답 메시지와 상태 코드 상수
RESPONSES = {
    "INVALID_EMAIL": {"message": "유효하지 않은 이메일 형식입니다.", "code": "INVALID_EMAIL"},
    "INVALID_PASSWORD": {"message": "비밀번호는 최소 6자 이상이어야 합니다.", "code": "INVALID_PASSWORD"},
    "EMAIL_ALREADY_EXISTS": {"message": "중복된 이메일이 존재합니다.", "code": "EMAIL_ALREADY_EXISTS"},
    "LOGIN_SUCCESS": {"message": "로그인 성공", "code": "LOGIN_SUCCESS"},
    "LOGIN_FAILED": {"message": "이메일 또는 비밀번호가 잘못되었습니다.", "code": "LOGIN_FAILED"},
    "TOKEN_REFRESH_SUCCESS": {"message": "토큰 갱신 성공", "code": "TOKEN_REFRESH_SUCCESS"},
    "PROFILE_UPDATED": {"message": "회원 정보 수정 성공", "code": "PROFILE_UPDATED"},
    "NO_CHANGES": {"message": "수정된 내용이 없습니다.", "code": "NO_CHANGES"},
    "DELETE_SUCCESS": {"message": "회원 탈퇴 성공", "code": "DELETE_SUCCESS"},
    "INVALID_TOKEN": {"message": "유효하지 않은 리프레시 토큰입니다.", "code": "INVALID_TOKEN"}
}

# 회원 가입
@auth_routes.route('/register', methods=['POST'])
def register_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({
            "status": "error",
            "message": RESPONSES["INVALID_EMAIL"]["message"],
            "code": RESPONSES["INVALID_EMAIL"]["code"]
        }), 400
    if not password or len(password) < 6:
        return jsonify({
            "status": "error",
            "message": RESPONSES["INVALID_PASSWORD"]["message"],
            "code": RESPONSES["INVALID_PASSWORD"]["code"]
        }), 400

    username = data.get('username')
    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password, username=username)

    try:
        user_id = new_user.save()
    except ValueError:
        return jsonify({
            "status": "error",
            "message": RESPONSES["EMAIL_ALREADY_EXISTS"]["message"],
            "code": RESPONSES["EMAIL_ALREADY_EXISTS"]["code"]
        }), 400

    return jsonify({
        "status": "success",
        "data": {
            "message": "회원 가입이 성공적으로 완료되었습니다.",
            "user_id": str(user_id)
        }
    }), 201

# 로그인
@auth_routes.route('/login', methods=['POST'])
def login_user():
    data = request.json
    user = User.find_by_email(data['email'])
    if user and check_password_hash(user['password'], data['password']):
        access_token = create_access_token(user_id=str(user['_id']))
        refresh_token = create_refresh_token(user_id=str(user['_id']))
        User.log_login(user['_id'], datetime.utcnow())
        return jsonify({
            "status": "success",
            "data": {
                "message": RESPONSES["LOGIN_SUCCESS"]["message"],
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        }), 200

    return jsonify({
        "status": "error",
        "message": RESPONSES["LOGIN_FAILED"]["message"],
        "code": RESPONSES["LOGIN_FAILED"]["code"]
    }), 401

# 토큰 갱신
@auth_routes.route('/refresh', methods=['POST'])
def refresh_token():
    refresh_token = request.json.get('refresh_token')
    if not refresh_token:
        return jsonify({
            "status": "error",
            "message": RESPONSES["INVALID_TOKEN"]["message"],
            "code": RESPONSES["INVALID_TOKEN"]["code"]
        }), 401

    user_id = decode_refresh_token(refresh_token)
    if not user_id:
        return jsonify({
            "status": "error",
            "message": RESPONSES["INVALID_TOKEN"]["message"],
            "code": RESPONSES["INVALID_TOKEN"]["code"]
        }), 401

    new_access_token = create_access_token(user_id=user_id)
    return jsonify({
        "status": "success",
        "data": {
            "message": RESPONSES["TOKEN_REFRESH_SUCCESS"]["message"],
            "access_token": new_access_token
        }
    }), 200

# 로그아웃
@auth_routes.route('/logout', methods=['POST'])
@token_required
def logout_user():
    token = request.headers.get('Authorization').split(" ")[1]
    add_to_blacklist(token)
    return jsonify({
        "status": "success",
        "data": {
            "message": "로그아웃 성공"
        }
    }), 200

# 회원 정보 수정
@auth_routes.route('/profile', methods=['PUT'])
@token_required
def update_profile():
    data = request.json
    if "password" in data:
        data['password'] = generate_password_hash(data['password'])

    updated = User.update(g.user_id, data)
    if updated:
        return jsonify({
            "status": "success",
            "data": {
                "message": RESPONSES["PROFILE_UPDATED"]["message"]
            }
        }), 200
    return jsonify({
        "status": "success",
        "data": {
            "message": RESPONSES["NO_CHANGES"]["message"]
        }
    }), 200

# 회원 탈퇴
@auth_routes.route('/delete', methods=['DELETE'])
@token_required
def delete_user():
    deleted = User.delete(g.user_id)
    if deleted:
        return jsonify({
            "status": "success",
            "data": {
                "message": RESPONSES["DELETE_SUCCESS"]["message"]
            }
        }), 200
    return jsonify({
        "status": "error",
        "message": "회원 탈퇴 실패",
        "code": "DELETE_FAILED"
    }), 400
