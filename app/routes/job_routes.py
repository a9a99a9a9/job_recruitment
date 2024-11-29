from flask import Blueprint, request, jsonify
from app.models.job import Job

job_routes = Blueprint('jobs', __name__)

# 채용 공고 조회 (전체)
@job_routes.route('/jobs', methods=['GET'])
def get_jobs():
    filters = request.args
    jobs = Job.find_all(filters)
    return jsonify({"data": jobs}), 200

# 채용 공고 등록
@job_routes.route('/jobs', methods=['POST'])
def add_job():
    data = request.json
    new_job = Job(data)
    job_id = new_job.save()
    return jsonify({"message": "채용 공고 등록 성공", "job_id": str(job_id)}), 201

# 채용 공고 수정
@job_routes.route('/jobs/<job_id>', methods=['PUT'])
def update_job(job_id):
    data = request.json
    updated = Job.update(job_id, data)
    return jsonify({"message": "채용 공고 수정 성공", "updated": updated}), 200

# 채용 공고 삭제
@job_routes.route('/jobs/<job_id>', methods=['DELETE'])
def delete_job(job_id):
    Job.delete(job_id)
    return jsonify({"message": "채용 공고 삭제 성공"}), 200

# 채용 공고 검색
@job_routes.route('/jobs/search', methods=['GET'])
def search_jobs():
    query = request.args.get('query', '')
    jobs = Job.search(query)
    return jsonify({"data": jobs}), 200
