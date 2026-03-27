# Railway 배포 메모

## 권장 방식
1. Railway에서 Empty Project 생성
2. PostgreSQL 추가
3. Empty Service 3개 생성
   - hearing-backend-service
   - hearing-ai-service
   - hearing-admin-web
4. 각 서비스에 같은 GitHub 모노레포 연결
5. 각 서비스 Root Directory 설정
   - backend: `/backend-service`
   - ai: `/ai-service`
   - admin: `/admin-web`
6. 각 서비스 환경변수 설정
7. Deploy

## backend-service 환경변수 예시
- PORT=8000
- APP_ENV=production
- APP_NAME=hearing-backend-service
- DATABASE_URL=${{Postgres.DATABASE_URL}} 또는 Railway가 제공하는 DB URL
- API_KEY=원하는 비밀키
- BACKEND_CORS_ORIGINS=https://여러분-admin-domain

## ai-service 환경변수 예시
- PORT=8001
- APP_ENV=production
- APP_NAME=hearing-ai-service
- BACKEND_INTERNAL_URL=https://backend 공개도메인
- AI_SHARED_TOKEN=원하는 비밀키

## admin-web
별도 환경변수 없이 바로 배포 가능

## 주의
- Railway에서 서비스 간 private domain 또는 public domain을 어떤 방식으로 쓸지 팀에서 통일하세요.
- 처음에는 public URL 기준으로 붙이고, 추후 private networking으로 바꿔도 됩니다.
- 운영 전에는 비밀키, 인증, 재시도, DB migration을 추가하세요.
