from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.utils.jwt_helper import create_access_token, decode_access_token

auth_routes = Blueprint('auth', __name__)

# 회원 가입
@auth_routes.route('/auth/register', methods=['POST'])
def register_user():
    data = request.json
    if not data.get('email') or not data.get('password'):
        return jsonify({"error": "이메일과 비밀번호는 필수입니다."}), 400

    hashed_password = generate_password_hash(data['password'])
    new_user = User(email=data['email'], password=hashed_password)
    user_id = new_user.save()

    return jsonify({"message": "회원 가입 성공", "user_id": str(user_id)}), 201

# 로그인
@auth_routes.route('/auth/login', methods=['POST'])
def login_user():
    data = request.json
    user = User.find_by_email(data['email'])
    if user and check_password_hash(user['password'], data['password']):
        token = create_access_token(user_id=str(user['_id']))
        return jsonify({"message": "로그인 성공", "token": token}), 200

    return jsonify({"error": "이메일 또는 비밀번호가 잘못되었습니다."}), 401

# 회원 정보 수정
@auth_routes.route('/auth/profile', methods=['PUT'])
def update_profile():
    token = request.headers.get('Authorization')
    user_id = decode_access_token(token)
    if not user_id:
        return jsonify({"error": "유효하지 않은 토큰입니다."}), 401

    data = request.json
    updated = User.update(user_id, data)
    return jsonify({"message": "회원 정보 수정 성공", "updated": updated}), 200

# 회원 탈퇴
@auth_routes.route('/auth/delete', methods=['DELETE'])
def delete_user():
    token = request.headers.get('Authorization')
    user_id = decode_access_token(token)
    if not user_id:
        return jsonify({"error": "유효하지 않은 토큰입니다."}), 401

    User.delete(user_id)
    return jsonify({"message": "회원 탈퇴 성공"}), 200
