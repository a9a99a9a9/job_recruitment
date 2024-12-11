from flask import Blueprint, request, jsonify
from app.models.job import Job

job_routes = Blueprint('jobs', __name__)

# 채용 공고 목록 조회
@job_routes.route('/', methods=['GET'])
def get_jobs():
    filters = {key: value for key, value in request.args.items()}
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    skip = (page - 1) * limit
    sort_by = request.args.get('sort_by', "created_at")
    order = int(request.args.get('order', -1))

    # 필터링
    if 'location' in filters:
        filters['location'] = {"$regex": filters['location'], "$options": "i"}
    if '경력' in filters:
        filters['경력'] = {"$regex": filters['경력'], "$options": "i"}
    if 'salary' in filters and filters['salary'].isdigit():
        filters['salary'] = {"$gte": int(filters['salary'])}
    if 'stack' in filters:
        filters['stack'] = {"$in": filters['stack'].split(",")}

    # 데이터 조회
    jobs = Job.find_all(filters, sort_by=sort_by, order=order, skip=skip, limit=limit)
    total_jobs = Job.count(filters)

    response = {
        "status": "success",
        "data": jobs,
        "pagination": {
            "currentPage": page,
            "totalPages": (total_jobs + limit - 1) // limit,
            "totalItems": total_jobs,
            "itemsPerPage": limit,
        },
    }
    return jsonify(response), 200

# 채용 공고 상세 조회
@job_routes.route('/<job_id>', methods=['GET'])
def get_job_detail(job_id):
    job = Job.find_by_id(job_id)
    if not job:
        return jsonify({
            "status": "error",
            "message": "채용 공고를 찾을 수 없습니다.",
            "code": "JOB_NOT_FOUND"
        }), 404

    Job.increment_views(job_id)
    recommended = Job.recommend_jobs(job_id)

    return jsonify({
        "status": "success",
        "data": job,
        "recommended": recommended,
    }), 200

# 채용 공고 검색
@job_routes.route('/search', methods=['GET'])
def search_jobs():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify({
            "status": "error",
            "message": "검색어가 제공되지 않았습니다.",
            "code": "MISSING_QUERY"
        }), 400

    jobs = Job.search(query)
    return jsonify({
        "status": "success",
        "data": jobs
    }), 200
