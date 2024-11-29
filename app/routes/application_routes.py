from flask import Blueprint, request, jsonify
from app.models.application import Application

application_routes = Blueprint('applications', __name__)

# 지원하기
@application_routes.route('/', methods=['POST'])
def apply_job():
    data = request.json
    if not data.get('user_id') or not data.get('job_id'):
        return jsonify({"error": "user_id와 job_id는 필수입니다."}), 400

    application_id = Application.create(data)
    return jsonify({"message": "지원 성공", "application_id": str(application_id)}), 201

# 지원 내역 조회
@application_routes.route('/', methods=['GET'])
def get_applications():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id는 필수입니다."}), 400

    applications = Application.find_by_user(user_id)
    if not applications:
        return jsonify({"message": "지원 내역이 없습니다."}), 200

    return jsonify({"data": applications}), 200

# 지원 취소
@application_routes.route('/<application_id>', methods=['DELETE'])
def cancel_application(application_id):
    if not Application.exists(application_id):
        return jsonify({"error": "해당 지원 내역을 찾을 수 없습니다."}), 404

    Application.delete(application_id)
    return jsonify({"message": "지원 취소 성공"}), 200

# 지원 상태 업데이트 (Custom 추가)
@application_routes.route('/<application_id>/status', methods=['PATCH'])
def update_application_status(application_id):
    status = request.json.get('status')
    if not status:
        return jsonify({"error": "상태는 필수입니다."}), 400

    updated = Application.update_status(application_id, status)
    if not updated:
        return jsonify({"error": "해당 지원 내역을 찾을 수 없습니다."}), 404

    return jsonify({"message": "지원 상태 업데이트 성공"}), 200
