.
├── README.md                  # 프로젝트 설명 및 실행 방법을 담고 있는 문서입니다.
├── app                         # 애플리케이션의 코드와 설정 파일들이 들어 있는 디렉토리입니다.
│   ├── __init__.py            # 애플리케이션 초기화 파일로, 패키지로서의 역할을 합니다.
│   ├── __pycache__            # Python 컴파일 후 생성되는 바이트 코드 파일들이 저장되는 디렉토리입니다.
│   ├── config.py              # 애플리케이션의 설정 파일 (예: DB 연결, 환경 변수 등)
│   ├── crawler_errors.log     # 크롤러 실행 중 발생한 오류를 기록한 로그 파일입니다.
│   ├── main.py                # 애플리케이션의 엔트리 포인트가 되는 파일입니다. Flask 앱 실행.
│   ├── models                 # 데이터베이스 모델들을 정의하는 디렉토리입니다.
│   │   ├── application.py     # 지원 관련 데이터베이스 모델
│   │   ├── bookmark.py        # 북마크 관련 데이터베이스 모델
│   │   ├── job.py             # 채용 공고 관련 데이터베이스 모델
│   │   └── user.py            # 사용자 관련 데이터베이스 모델
│   ├── routes                 # API 엔드포인트를 처리하는 라우터 파일들
│   │   ├── application_routes.py # 지원 관련 API 라우팅
│   │   ├── auth_routes.py     # 인증 관련 API 라우팅
│   │   ├── bookmark_routes.py   # 북마크 관련 API 라우팅
│   │   └── job_routes.py      # 채용 공고 관련 API 라우팅
│   ├── swagger                # Swagger API 문서 파일이 저장된 디렉토리
│   │   ├── swagger.json       # Swagger API 문서 (JSON 형식)
│   │   └── swagger.yaml       # Swagger API 문서 (YAML 형식)
│   └── utils                  # 유틸리티 함수들 (크롤러, JWT 처리, 미들웨어 등)
│       ├── crawler.py         # 크롤러 관련 유틸리티 파일
│       ├── db_helper.py       # DB 연결 및 유틸리티 함수
│       ├── jwt_helper.py      # JWT 생성 및 검증 함수들
│       └── middlewares.py     # 인증 미들웨어 등
├── crawler_errors.log         # 크롤링 중 발생한 오류를 기록한 로그 파일
├── data                       # 크롤링된 데이터 및 관련 로그 파일
│   ├── crawled_data.json      # 크롤링된 데이터 (JSON 형식)
│   └── logs                   # 로그 디렉토리
│       ├── api.log            # API 호출 로그
│       └── crawl.log          # 크롤링 로그
└── requirements.txt           # 프로젝트에 필요한 Python 라이브러리 목록


1. README.md
프로젝트에 대한 설명, 실행 방법, 개발 환경, 의존성 설치 방법, API 문서 등을 포함하는 파일입니다. 프로젝트 시작 시 개발자 및 사용자가 참고할 수 있도록 작성됩니다.

2. app/
애플리케이션 코드가 포함된 디렉토리입니다. 주요 파일들은 다음과 같습니다:
__init__.py: Flask 애플리케이션을 초기화하고, 패키지로서의 역할을 하는 파일입니다.
config.py: 데이터베이스 연결, 환경 변수 등의 애플리케이션 설정을 포함합니다.
main.py: Flask 애플리케이션을 실행시키는 진입점입니다. 애플리케이션의 라우팅, 초기화 등을 담당합니다.

3. models/
데이터베이스 모델을 정의하는 디렉토리입니다. 각 모델은 데이터베이스의 테이블(또는 컬렉션)을 나타냅니다:
application.py: 지원 관련 정보를 관리하는 모델입니다.
bookmark.py: 북마크 관련 정보를 관리하는 모델입니다.
job.py: 채용 공고 정보를 관리하는 모델입니다.
user.py: 사용자 정보를 관리하는 모델입니다.

4. routes/
API 엔드포인트를 정의하는 라우터 파일들이 포함된 디렉토리입니다:
application_routes.py: 지원 관련 API 엔드포인트들이 정의된 파일입니다.
auth_routes.py: 회원 가입, 로그인, 인증 등 인증 관련 API 엔드포인트들을 처리합니다.
bookmark_routes.py: 북마크 추가, 제거, 조회 등을 처리하는 API 엔드포인트입니다.
job_routes.py: 채용 공고 조회, 추가, 수정 등을 처리하는 API 엔드포인트입니다.

5. swagger/
Swagger API 문서를 정의하는 디렉토리입니다:
swagger.json: Swagger API 문서의 JSON 형식 버전입니다.
swagger.yaml: Swagger API 문서의 YAML 형식 버전입니다. Swagger UI에서 API 문서를 동적으로 테스트할 수 있도록 제공됩니다.

6. utils/
다양한 유틸리티 함수들이 포함된 디렉토리입니다:
crawler.py: 크롤러 관련 유틸리티 함수들이 포함되어 있습니다.
db_helper.py: 데이터베이스 연결 및 기타 DB 관련 유틸리티 함수들이 정의됩니다.
jwt_helper.py: JWT 생성 및 검증을 위한 함수들이 포함됩니다.
middlewares.py: 인증 및 권한 검사 등 미들웨어 관련 함수들이 포함됩니다.

7. crawler_errors.log
크롤링 중 발생한 오류들을 기록한 로그 파일입니다. 크롤러가 실행되는 동안 발생한 예외나 오류를 추적할 수 있습니다.

8. data/
크롤링된 데이터와 관련된 파일들이 저장되는 디렉토리입니다:
crawled_data.json: 크롤링된 데이터가 JSON 형식으로 저장됩니다.
logs/: 크롤링 및 API 호출과 관련된 로그 파일들이 저장됩니다:
api.log: API 호출에 대한 로그.
crawl.log: 크롤러 실행에 대한 로그.

9. requirements.txt
프로젝트에서 사용하는 Python 패키지 목록을 정의하는 파일입니다. 이 파일을 통해 프로젝트에서 필요한 모든 의존성 패키지를 설치할 수 있습니다:



pip install -r requirements.txt
애플리케이션 실행


python app/main.py
또는 Flask 애플리케이션을 실행하려면 다음 명령어를 사용할 수 있습니다:


pip install -r requirements.txt

python app/main.py
