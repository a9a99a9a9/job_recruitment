from flask import Blueprint, request, jsonify
from app.models.job import Job

job_routes = Blueprint('jobs', __name__)

# 채용 공고 조회 (전체)
@job_routes.route('/', methods=['GET'])  # /jobs 경로로 연결됨
def get_jobs():
    filters = request.args.to_dict()
    jobs = Job.find_all(filters)
    return jsonify({"data": jobs}), 200

# 채용 공고 등록
@job_routes.route('/', methods=['POST'])  # /jobs 경로로 연결됨
def add_job():
    data = request.json
    if not data:
        return jsonify({"error": "유효한 데이터를 제공하세요."}), 400
    job_id = Job.save(data)
    return jsonify({"message": "채용 공고 등록 성공", "job_id": str(job_id)}), 201

# 채용 공고 수정
@job_routes.route('/<job_id>', methods=['PUT'])  # /jobs/<job_id> 경로로 연결됨
def update_job(job_id):
    data = request.json
    if not data:
        return jsonify({"error": "유효한 데이터를 제공하세요."}), 400
    updated = Job.update(job_id, data)
    if updated == 0:
        return jsonify({"message": "수정된 내용이 없습니다."}), 200
    return jsonify({"message": "채용 공고 수정 성공", "updated": updated}), 200

# 채용 공고 삭제
@job_routes.route('/<job_id>', methods=['DELETE'])  # /jobs/<job_id> 경로로 연결됨
def delete_job(job_id):
    deleted = Job.delete(job_id)
    if deleted == 0:
        return jsonify({"error": "삭제할 데이터를 찾을 수 없습니다."}), 404
    return jsonify({"message": "채용 공고 삭제 성공"}), 200

# 채용 공고 검색
@job_routes.route('/search', methods=['GET'])  # /jobs/search 경로로 연결됨
def search_jobs():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify({"error": "검색어를 입력하세요."}), 400
    jobs = Job.search(query)
    return jsonify({"data": jobs}), 200
