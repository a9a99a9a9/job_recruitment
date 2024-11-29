from flask import Blueprint, request, jsonify
from app.models.application import Application

application_routes = Blueprint('applications', __name__)

# 지원하기
@application_routes.route('/applications', methods=['POST'])
def apply_job():
    data = request.json
    application_id = Application.create(data)
    return jsonify({"message": "지원 성공", "application_id": str(application_id)}), 201

# 지원 내역 조회
@application_routes.route('/applications', methods=['GET'])
def get_applications():
    user_id = request.args.get('user_id')
    applications = Application.find_by_user(user_id)
    return jsonify({"data": applications}), 200

# 지원 취소
@application_routes.route('/applications/<application_id>', methods=['DELETE'])
def cancel_application(application_id):
    Application.delete(application_id)
    return jsonify({"message": "지원 취소 성공"}), 200

# 지원 상태 업데이트 (Custom 추가)
@application_routes.route('/applications/<application_id>/status', methods=['PATCH'])
def update_application_status(application_id):
    status = request.json.get('status')
    Application.update_status(application_id, status)
    return jsonify({"message": "지원 상태 업데이트 성공"}), 200
