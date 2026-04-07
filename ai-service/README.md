# ai-service

청각장애인 생활 보조 시스템의 AI 이벤트 처리 서비스입니다.

이 서비스는 라즈베리파이(또는 AI 입력 장치)로부터 전달받은 위험 소리 / 호출 감지 결과를 수신하고,
입력 데이터를 검증 및 정규화한 뒤 backend-service로 전달하는 역할을 담당합니다.

현재 ai-service는 **STT를 수행하지 않으며**, **이벤트 데이터 처리 및 전달**에만 집중합니다.

---

# 1. 서비스 개요

ai-service는 라즈베리파이에서 이미 분석한 이벤트 결과를 받아 backend-service로 전달합니다.

예시:

* 자동차 경적 감지
* 사이렌 감지
* 자전거 벨 감지
* 사람 호출음 감지
* 방향 정보 포함 (left / right / front / back / unknown)

즉, 이 서비스의 핵심 역할은 아래와 같습니다.

* 이벤트 데이터 수신
* 인증 확인
* 입력 검증
* 데이터 정규화
* backend-service `/alerts`로 forwarding

---

# 2. 역할 분리

## ai-service

* `x-ai-token` 기반 인증
* 위험 소리 / 호출 감지 이벤트 수신
* 입력 데이터 검증 및 정규화
* backend-service의 `/alerts`로 HTTP forwarding

## backend-service

* ai-service로부터 alerts 수신
* DB 저장
* Redis / WebSocket / 클라이언트 푸시
* 사용자 / 설정 / 인증 처리

---

# 3. 전체 동작 구조

## 위험 소리 / 호출 감지 흐름

```text
[4-ch microphone]
        ↓
[Raspberry Pi]
위험 소리 감지 / 호출 감지 / 방향 추정
        ↓
POST /ingest/event (AI Service)
        ↓
입력 검증 / 정규화
        ↓
POST /alerts (Backend Service)
        ↓
DB 저장 + 실시간 전송

ai-service/
├─ app/
│  ├─ api/
│  │  ├─ __init__.py
│  │  ├─ deps.py
│  │  └─ routes/
│  │      ├─ __init__.py
│  │      ├─ health.py
│  │      └─ event.py
│  │
│  ├─ core/
│  │  ├─ __init__.py
│  │  ├─ config.py
│  │  └─ security.py
│  │
│  ├─ schemas/
│  │  ├─ __init__.py
│  │  ├─ event.py
│  │  └─ forward.py
│  │
│  ├─ services/
│  │  ├─ __init__.py
│  │  ├─ normalizer.py
│  │  ├─ forwarder.py
│  │  └─ pipeline.py
│  │
│  ├─ utils/
│  │  ├─ __init__.py
│  │  └─ logger.py
│  │
│  └─ main.py
│
├─ .dockerignore
├─ Dockerfile
├─ requirements.txt
└─ README.md