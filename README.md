# 미슐랭 맛집 지도

# 프로젝트 개요

이 프로젝트는 데브코스 데이터 엔지니어링 7기 1차 프로젝트로,

Django를 활용하여 미슐랭 맛집 정보를 시각화한 지도 서비스를 구현했습니다.

# 프로젝트 개요

이 프로젝트는 데브코스 데이터 엔지니어링 7기 1차 프로젝트로,

Django를 활용하여 미슐랭 맛집 정보를 시각화한 지도 서비스를 구현했습니다.

# 프로젝트 소개

## **프로젝트명**

- 미슐랭 맛집 지도

## **주요 기능**

- [미슐랭 가이드 공식 웹사이트](https://guide.michelin.com/kr/ko)에서 크롤링한 데이터를 활용하여 실제 지도에 맛집 위치를 표시합니다.
- 맛집 마커를 클릭하면 새 창이 열리며 다음 정보를 확인할 수 있습니다.
    - 식당 기본 정보
    - 별점 그래프
    - 워드 클라우드

# 사용 기술 스택

| 분야 | 기술 |
| --- | --- |
| **Backend** | Django, Python |
| **Frontend** | HTML, CSS, JavaScript |
| **Database** | SQLite  |
| **Data Crawling** | BeautifulSoup, Selenium |
| **Data Visualization** | Matplotlib, WordCloud |

# 데이터 수집 및 전처리

## **데이터 출처**

- [미슐랭 가이드 공식 웹사이트](https://guide.michelin.com/kr/ko), [카카오맵](https://map.kakao.com/)

## **수집 방식**

- Selenium을 이용하여 맛집 이름, 위치, 평점, 리뷰 등 데이터를 크롤링

## **전처리 과정**

- 불필요한 HTML 태그 제거
- 좌표 변환 및 지도 API 연동
- 텍스트 데이터 토큰화 및 워드클라우드 생성

# 파일 구조

```
DE7_team3-master
└── Team3_project
    ├── crawler/                      # 데이터 수집 (크롤러)
    │   ├── michelin_crawler.py       # 미슐랭 공식 사이트 크롤링 스크립트
    │   └── restaurant.ipynb          # 크롤링 및 데이터 전처리 노트북
    │
    ├── michelinmap/                  # Django 앱 (미슐랭 맛집 지도)
    │   ├── management/               # 관리 명령어 관련 모듈
    │   ├── migrations/               # DB 마이그레이션 파일
    │   ├── static/                   # CSS, JS, 이미지, 폰트 등 정적 파일
    │   ├── templates/                # HTML 템플릿
    │   ├── admin.py                  # Django 관리자 페이지 설정
    │   ├── apps.py                   # 앱 설정
    │   ├── models.py                 # DB 모델 정의
    │   ├── urls.py                   # URL 라우팅 설정
    │   └── views.py                  # 뷰 (로직 및 데이터 처리)
    │
    ├── mysite/                       # Django 프로젝트 설정 폴더
    │   ├── settings.py               # 전체 프로젝트 설정 (DB, 앱 등록 등)
    │   ├── urls.py                   # 루트 URL 라우팅
    │   ├── asgi.py / wsgi.py         # 서버 실행 관련 설정
    │   └── __init__.py
    │
    ├── db.sqlite3                    # SQLite 데이터베이스 파일
    ├── manage.py                     # Django 관리 명령어 실행 파일
    ├── cities.csv                    # 시군구 데이터
    ├── regions.csv                   # 시/도 데이터
    └── restaurants.csv               # 크롤링된 미슐랭 맛집 데이터

```

# 프로젝트 목표

- 실제 서비스 가능한 형태의 데이터 기반 웹 애플리케이션 구현
- 크롤링 → 전처리 → 시각화 → 웹 서비스까지의 데이터 파이프라인 전 과정 경험
- 사용자 친화적인 지도 기반 맛집 탐색 서비스 제공
