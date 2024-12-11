from flask import Blueprint, request, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.utils.jwt_helper import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    add_to_blacklist
)
from app.utils.middlewares import token_required  # 수정된 데코레이터 사용

auth_routes = Blueprint('auth', __name__)

# 회원 가입
@auth_routes.route('/register', methods=['POST'])
def register_user():
    data = request.json
    if not data.get('email') or not data.get('password'):
        return jsonify({"error": "이메일과 비밀번호는 필수입니다."}), 400

    username = data.get('username', None)
    hashed_password = generate_password_hash(data['password'])

    new_user = User(email=data['email'], password=hashed_password, username=username)

    try:
        user_id = new_user.save()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"message": "회원 가입 성공", "user_id": str(user_id)}), 201


# 로그인
@auth_routes.route('/login', methods=['POST'])
def login_user():
    data = request.json
    user = User.find_by_email(data['email'])
    if user and check_password_hash(user['password'], data['password']):
        access_token = create_access_token(user_id=str(user['_id']))
        refresh_token = create_refresh_token(user_id=str(user['_id']))
        return jsonify({
            "message": "로그인 성공",
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200

    return jsonify({"error": "이메일 또는 비밀번호가 잘못되었습니다."}), 401


# 토큰 갱신
@auth_routes.route('/refresh', methods=['POST'])
def refresh_token():
    refresh_token = request.json.get('refresh_token')
    if not refresh_token:
        return jsonify({"error": "리프레시 토큰이 제공되지 않았습니다."}), 400

    user_id = decode_refresh_token(refresh_token)
    if not user_id:
        return jsonify({"error": "유효하지 않은 리프레시 토큰입니다."}), 401

    new_access_token = create_access_token(user_id=user_id)
    return jsonify({
        "message": "토큰 갱신 성공",
        "access_token": new_access_token
    }), 200


# 로그아웃
@auth_routes.route('/logout', methods=['POST'])
@token_required
def logout_user():
    token = request.headers.get('Authorization').split(" ")[1]
    add_to_blacklist(token)
    return jsonify({"message": "로그아웃 성공"}), 200


# 회원 정보 수정
@auth_routes.route('/profile', methods=['PUT'])
@token_required
def update_profile():
    data = request.json
    updated = User.update(g.user_id, data)
    if updated == 0:
        return jsonify({"message": "수정된 내용이 없습니다."}), 200
    return jsonify({"message": "회원 정보 수정 성공"}), 200


# 회원 탈퇴
@auth_routes.route('/delete', methods=['DELETE'])
@token_required
def delete_user():
    deleted = User.delete(g.user_id)
    if deleted == 0:
        return jsonify({"error": "사용자 삭제 실패"}, 400)
    return jsonify({"message": "회원 탈퇴 성공"}), 200