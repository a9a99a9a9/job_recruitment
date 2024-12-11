from flask import Blueprint, request, jsonify, g
from app.models.bookmark import Bookmark
from app.utils.middlewares import token_required

bookmark_routes = Blueprint('bookmarks', __name__)

# 북마크 추가/제거 (토글)
@bookmark_routes.route('/', methods=['POST'])
@token_required
def toggle_bookmark():
    user_id = g.user_id  # 인증된 사용자 ID
    data = request.json
    job_id = data.get("job_id")

    if not job_id:
        return jsonify({
            "status": "error",
            "message": "job_id는 필수입니다.",
            "code": "INVALID_REQUEST"
        }), 400

    result = Bookmark.toggle(user_id, job_id)
    message = "북마크가 성공적으로 추가되었습니다." if result == "added" else "북마크가 성공적으로 제거되었습니다."
    return jsonify({
        "status": "success",
        "data": {
            "message": message
        }
    }), 200

# 북마크 조회
@bookmark_routes.route('/', methods=['GET'])
@token_required
def get_bookmarks():
    user_id = g.user_id  # 인증된 사용자 ID
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 20))
    skip = (page - 1) * limit

    bookmarks = Bookmark.find_by_user(user_id, skip=skip, limit=limit)
    total_bookmarks = Bookmark.count(user_id)

    response = {
        "status": "success",
        "data": bookmarks,
        "pagination": {
            "currentPage": page,
            "totalPages": (total_bookmarks + limit - 1) // limit,
            "totalItems": total_bookmarks,
            "itemsPerPage": limit
        }
    }
    return jsonify(response), 200
