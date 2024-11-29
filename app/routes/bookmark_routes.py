from flask import Blueprint, request, jsonify
from app.models.bookmark import Bookmark

bookmark_routes = Blueprint('bookmarks', __name__)

# 북마크 추가
@bookmark_routes.route('/bookmarks', methods=['POST'])
def add_bookmark():
    data = request.json
    bookmark_id = Bookmark.add(data)
    return jsonify({"message": "북마크 추가 성공", "bookmark_id": str(bookmark_id)}), 201

# 북마크 조회
@bookmark_routes.route('/bookmarks', methods=['GET'])
def get_bookmarks():
    user_id = request.args.get('user_id')
    bookmarks = Bookmark.find_by_user(user_id)
    return jsonify({"data": bookmarks}), 200

# 북마크 삭제
@bookmark_routes.route('/bookmarks/<bookmark_id>', methods=['DELETE'])
def delete_bookmark(bookmark_id):
    Bookmark.delete(bookmark_id)
    return jsonify({"message": "북마크 삭제 성공"}), 200

# 북마크 필터링 (Custom 추가)
@bookmark_routes.route('/bookmarks/filter', methods=['GET'])
def filter_bookmarks():
    filters = request.args
    bookmarks = Bookmark.filter(filters)
    return jsonify({"data": bookmarks}), 200
