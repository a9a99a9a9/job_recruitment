from flask import Blueprint, request, jsonify, g
from app.models.bookmark import Bookmark
from app.utils.middlewares import token_required

bookmark_routes = Blueprint('bookmarks', __name__)

# 북마크 추가
@bookmark_routes.route('/', methods=['POST'])
@token_required
def add_bookmark():
    user_id = g.user_id  # 미들웨어에서 저장된 user_id 사용
    data = request.json
    data['user_id'] = user_id  # 요청 데이터에 user_id 추가
    bookmark_id = Bookmark.add(data)
    return jsonify({"message": "북마크 추가 성공", "bookmark_id": str(bookmark_id)}), 201

# 북마크 조회
@bookmark_routes.route('/', methods=['GET'])
@token_required
def get_bookmarks():
    user_id = g.user_id  # 미들웨어에서 저장된 user_id 사용
    bookmarks = Bookmark.find_by_user(user_id)
    return jsonify({"data": bookmarks}), 200

# 북마크 삭제
@bookmark_routes.route('/<bookmark_id>', methods=['DELETE'])
@token_required
def delete_bookmark(bookmark_id):
    user_id = g.user_id  # 미들웨어에서 저장된 user_id 사용
    Bookmark.delete(bookmark_id, user_id)  # user_id를 삭제 조건으로 전달
    return jsonify({"message": "북마크 삭제 성공"}), 200

# 북마크 필터링 (Custom 추가)
@bookmark_routes.route('/filter', methods=['GET'])
@token_required
def filter_bookmarks():
    user_id = g.user_id  # 미들웨어에서 저장된 user_id 사용
    filters = request.args
    filters = {**filters, "user_id": user_id}  # 필터 조건에 user_id 추가
    bookmarks = Bookmark.filter(filters)
    return jsonify({"data": bookmarks}), 200
