# hearing-assistant-monorepo

청각장애인 생활 보조 시스템용 서버 모노레포 예시입니다.

포함 서비스
- `backend-service`: 메인 백엔드(FastAPI + PostgreSQL)
- `ai-service`: AI 백엔드(FastAPI)
- `admin-web`: 아주 단순한 운영/상태 확인용 웹 페이지

> 모바일 앱(안드로이드/iOS)은 이 저장소에 포함하지 않았습니다.
> 앱은 별도 저장소 또는 별도 폴더로 관리하는 편이 일반적입니다.

## 1. 전체 구조

```text
hearing-assistant-monorepo/
├─ backend-service/
│  ├─ app/
│  │  ├─ api/routes/
│  │  ├─ core/
│  │  ├─ db/
│  │  ├─ main.py
│  │  └─ schemas.py
│  ├─ Dockerfile
│  ├─ requirements.txt
│  └─ .dockerignore
├─ ai-service/
│  ├─ app/
│  │  ├─ api/routes/
│  │  ├─ core/
│  │  ├─ services/
│  │  └─ main.py
│  ├─ Dockerfile
│  ├─ requirements.txt
│  └─ .dockerignore
├─ admin-web/
│  ├─ index.html
│  ├─ nginx.conf
│  └─ Dockerfile
├─ docker-compose.yml
├─ .env.example
├─ render.yaml
└─ RAILWAY_DEPLOY.md
```

## 2. 서비스 역할

### backend-service
- 앱/워치/AR 글래스와 통신하는 메인 백엔드
- PostgreSQL 저장
- 알림/이벤트 API 제공
- AI 백엔드에서 전달한 이벤트를 저장

### ai-service
- 라즈베리파이에서 들어온 이벤트 수신
- 위험 소리 / 방향 / STT 결과 정규화
- 메인 백엔드로 전달
- 현재 예시는 STT를 더미 함수로 넣어 둠

### admin-web
- 배포 확인용 정적 웹 페이지
- 각 서비스 health endpoint 확인용 링크 제공

## 3. 로컬 실행

루트에 `.env` 파일을 만들고 `.env.example` 내용을 복사하세요.

```bash
docker compose up --build
```

기본 주소
- backend: http://localhost:8000/docs
- ai: http://localhost:8001/docs
- admin web: http://localhost:8080
- postgres: localhost:5432

## 4. Render 배포

이 저장소에는 `render.yaml`이 포함되어 있습니다.

1. GitHub에 이 저장소 업로드
2. Render에서 Blueprint로 `render.yaml` 연결
3. postgres + backend + ai + admin-web 생성 확인
4. 필요한 환경변수 추가 수정

주의:
- `render.yaml`의 공개 URL은 최초 생성 후 Render 대시보드에서 실제 값으로 확인해야 합니다.
- 실제 운영 전에는 CORS, 인증, 비밀키, DB 마이그레이션을 보강해야 합니다.

## 5. Railway 배포

Railway는 같은 모노레포를 여러 서비스로 나누어 연결할 수 있습니다.
자세한 단계는 `RAILWAY_DEPLOY.md`를 참고하세요.

핵심은 이렇습니다.
- 하나의 Railway 프로젝트 생성
- PostgreSQL 추가
- `backend-service`를 루트 디렉터리 `/backend-service`로 연결
- `ai-service`를 루트 디렉터리 `/ai-service`로 연결
- `admin-web`를 루트 디렉터리 `/admin-web`로 연결
- 환경변수 설정 후 각각 배포

## 6. 지금 바로 수정하면 좋은 부분

### ai-service
- `services/stt.py` 실제 Whisper 또는 외부 STT로 교체
- `services/forwarder.py` 재시도/timeout/서명 검증 추가
- 라즈베리파이 인증 토큰 검증 추가

### backend-service
- Alembic 도입
- 사용자/디바이스/알림 테이블 추가
- WebSocket 또는 FCM/APNs 연동

### admin-web
- 실제 관리자 화면으로 교체 가능
- React/Vite 기반으로 바꿔도 됨

## 7. 권장 개발 순서

1. 이 뼈대를 그대로 GitHub에 올림
2. Render 또는 Railway에 우선 배포
3. AI → Backend 이벤트 전달 성공 여부 확인
4. PostgreSQL 저장 확인
5. 앱팀과 API 연결 시작
6. 이후 STT/알림/인증 순으로 고도화
