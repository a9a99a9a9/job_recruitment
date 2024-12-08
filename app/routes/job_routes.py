from flask import Blueprint, request, jsonify
from app.models.job import Job
from app.utils.middlewares import token_required
from typing import Dict, Union

job_routes = Blueprint('jobs', __name__)

# 채용 공고 조회 (전체) - 공개 API
@job_routes.route('/', methods=['GET'])
def get_jobs():
    """채용 공고 조회 (필터 포함 가능 + 페이지네이션)"""
    filters: Dict[str, Union[str, list[str]]] = request.args.to_dict()

    # 페이지네이션 파라미터 처리
    page = int(request.args.get('page', 1))  # 기본값: 1
    limit = int(request.args.get('limit', 20))  # 기본값: 20
    skip = (page - 1) * limit

    # 필터 조건 처리 (대소문자 구분 없이 검색)
    if 'location' in filters and isinstance(filters['location'], str):
        filters['location'] = {'$regex': filters['location'], '$options': 'i'}
    if '경력' in filters and isinstance(filters['경력'], str):
        filters['경력'] = {'$regex': filters['경력'], '$options': 'i'}
    if 'company' in filters and isinstance(filters['company'], str):
        filters['company'] = {'$regex': filters['company'], '$options': 'i'}
    if 'title' in filters and isinstance(filters['title'], str):
        filters['title'] = {'$regex': filters['title'], '$options': 'i'}
    if 'deadline' in filters and isinstance(filters['deadline'], str):
        filters['deadline'] = {'$regex': filters['deadline'], '$options': 'i'}

    # 데이터베이스에서 필터 및 페이지네이션 적용
    jobs = Job.find_all(filters, skip=skip, limit=limit)
    total_jobs = Job.count(filters)  # 전체 데이터 수 계산

    # 응답 데이터 구조화
    response = {
        "data": jobs,
        "pagination": {
            "currentPage": page,
            "totalPages": (total_jobs + limit - 1) // limit,
            "totalItems": total_jobs,
            "itemsPerPage": limit,
        },
    }
    return jsonify(response), 200

# 채용 공고 등록 - 인증 필요
@job_routes.route('/', methods=['POST'])
@token_required
def add_job():
    """채용 공고 등록"""
    data = request.json
    if not data:
        return jsonify({"error": "유효한 데이터를 제공하세요."}), 400

    job_id = Job.save(data)
    return jsonify({"message": "채용 공고 등록 성공", "job_id": str(job_id)}), 201


# 채용 공고 수정 - 인증 필요
@job_routes.route('/<job_id>', methods=['PUT'])
@token_required
def update_job(job_id):
    """채용 공고 수정"""
    data = request.json
    if not data:
        return jsonify({"error": "유효한 데이터를 제공하세요."}), 400

    updated = Job.update(job_id, data)
    if updated == 0:
        return jsonify({"message": "수정된 내용이 없습니다."}), 200

    return jsonify({"message": "채용 공고 수정 성공", "updated": updated}), 200


# 채용 공고 삭제 - 인증 필요
@job_routes.route('/<job_id>', methods=['DELETE'])
@token_required
def delete_job(job_id):
    """채용 공고 삭제"""
    deleted = Job.delete(job_id)
    if deleted == 0:
        return jsonify({"error": "삭제할 데이터를 찾을 수 없습니다."}), 404

    return jsonify({"message": "채용 공고 삭제 성공"}), 200


# 채용 공고 검색 - 공개 API
@job_routes.route('/search', methods=['GET'])
def search_jobs():
    """채용 공고 검색"""
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify({"error": "검색어를 입력하세요."}), 400

    jobs = Job.search(query)
    return jsonify({"data": jobs}), 200
