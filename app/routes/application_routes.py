from flask import Blueprint, request, jsonify, g
from app.models.application import Application
from app.utils.middlewares import token_required

application_routes = Blueprint('applications', __name__)

# 지원하기
@application_routes.route('/', methods=['POST'])
@token_required
def apply_job():
    user_id = g.user_id
    data = request.json
    job_id = data.get("job_id")
    resume = data.get("resume")  # 선택적 필드

    if not job_id:
        return jsonify({"error": "job_id는 필수입니다."}), 400

    try:
        application_id = Application.apply(user_id, job_id, resume)
        return jsonify({"message": "지원 성공", "application_id": str(application_id)}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# 지원 내역 조회
@application_routes.route('/', methods=['GET'])
@token_required
def get_applications():
    user_id = g.user_id
    status = request.args.get("status")
    sort_by = request.args.get("sort_by", "created_at")
    order = int(request.args.get("order", "-1"))

    filters = {}
    if status:
        filters["status"] = status

    applications = Application.find_by_user(user_id, filters, sort_by, order)
    return jsonify({"data": applications}), 200

# 지원 취소
@application_routes.route('/<application_id>', methods=['DELETE'])
@token_required
def cancel_application(application_id):
    try:
        Application.cancel(application_id)
        return jsonify({"message": "지원 취소 성공"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# 지원 상태 업데이트
@application_routes.route('/<application_id>/status', methods=['PATCH'])
@token_required
def update_application_status(application_id):
    status = request.json.get("status")
    if not status:
        return jsonify({"error": "상태는 필수입니다."}), 400

    updated = Application.update_status(application_id, status)
    if updated == 0:
        return jsonify({"error": "해당 지원 내역을 찾을 수 없습니다."}), 404

    return jsonify({"message": "지원 상태 업데이트 성공"}), 200
