# ai-service

청각장애인 생활 보조 시스템의 AI 서비스입니다.

이 서비스는 라즈베리파이(또는 AI 입력 장치)로부터 이벤트를 수신하고,  
데이터를 정규화한 뒤 STT를 수행하고, 최종 결과를 backend-service로 전달하는 역할을 담당합니다.

---

## 1. 서비스 역할

ai-service의 현재 역할은 다음과 같습니다.

1. 이벤트 수신 (`/ingest`)
2. `x-ai-token` 기반 인증
3. 입력 데이터 검증 및 정규화
4. STT 수행
5. backend-service의 `/alerts`로 HTTP forwarding

즉, 이 서비스는 **AI 이벤트 처리 + STT + backend 전달**까지 담당합니다.

---

## 2. 문서와 현재 구현의 차이

초기 전체 API 명세서 초안에는 다음과 같이 적혀 있습니다.

- AI 서비스: 오디오 수신, 노이즈 제거, 방향 추정, 정규화
- backend-service: Whisper STT, DB 저장, WebSocket 푸시 :contentReference[oaicite:1]{index=1}

하지만 **현재 팀 합의 및 실제 구현 기준에서는 STT를 ai-service가 담당**합니다.

따라서 현재 기준 역할 분리는 다음과 같습니다.

### ai-service
- ingest 수신
- 입력 정규화
- STT 수행
- backend-service로 forwarding

### backend-service
- AI 서비스로부터 alerts 수신
- DB 저장
- Redis / WebSocket / 클라이언트 푸시
- 사용자/설정/인증 처리

이 README는 **현재 구현 기준**으로 작성되어 있습니다.

---

## 3. 전체 데이터 흐름

현재 구현 기준 전체 흐름은 다음과 같습니다.

1. 라즈베리파이 또는 AI 입력 장치가 이벤트를 ai-service로 전송
2. ai-service가 입력 검증 및 정규화 수행
3. ai-service가 STT 수행
4. ai-service가 backend-service의 `/alerts`로 결과 전달
5. backend-service가 DB 저장 및 실시간 전송 처리

초기 명세서의 전체 흐름과 인증/전송 구조는 참고하되, STT 담당만 현재 구현 기준으로 수정해서 사용합니다. :contentReference[oaicite:2]{index=2}

---

## 4. 디렉토리 구조

```text
ai-service/
├─ app/
│  ├─ api/
│  │  └─ routes/
│  │      ├─ health.py
│  │      └─ ingest.py
│  │
│  ├─ core/
│  │  ├─ config.py
│  │  └─ security.py
│  │
│  ├─ schemas/
│  │  ├─ ingest.py
│  │  └─ forward.py
│  │
│  ├─ services/
│  │  ├─ normalizer.py
│  │  ├─ stt_service.py
│  │  ├─ forwarder.py
│  │  └─ pipeline.py
│  │
│  └─ main.py
│
├─ .dockerignore
├─ Dockerfile
├─ requirements.txt
└─ README.md

-------------------------------------------------------------

# 📡 API Endpoints

## 1. AI Service (ai-service)

---

### 1.1 Health Check

```http
GET /health
```

AI 서비스 상태 확인

#### Response

```json
{
  "status": "ok",
  "service": "hearing-ai-service",
  "env": "development"
}
```

---

### 1.2 Ingest (이벤트 수신)

```http
POST /ingest
```

라즈베리파이 또는 AI 입력 장치에서 이벤트 수신

#### Headers

```text
x-ai-token: {AI_SHARED_TOKEN}
```

#### Request Body

```json
{
  "device_id": "cap-001",
  "sound_type": "car_horn",
  "is_risk": true,
  "direction": "left",
  "confidence": 0.92,
  "transcript_hint": "빵빵",
  "metadata": {
    "source": "raspberry-pi"
  }
}
```

#### Field 설명

| 필드              | 타입      | 필수 | 설명                                 |
| --------------- | ------- | -- | ---------------------------------- |
| device_id       | string  | O  | 디바이스 ID                            |
| sound_type      | string  | O  | 소리 유형                              |
| is_risk         | boolean | O  | 위험 여부                              |
| direction       | string  | X  | 방향 (front/back/left/right/unknown) |
| confidence      | float   | X  | 신뢰도 (0~1)                          |
| transcript_hint | string  | X  | STT 힌트                             |
| metadata        | object  | X  | 추가 정보                              |

---

#### Response

```json
{
  "message": "AI event processed and forwarded successfully",
  "normalized_payload": {
    "device_id": "cap-001",
    "sound_type": "car_horn",
    "is_risk": true,
    "direction": "left",
    "confidence": 0.92,
    "stt_text": "빵빵",
    "raw_payload": {
      "metadata": {
        "source": "raspberry-pi"
      }
    }
  },
  "backend_response": {
    "id": 1
  }
}
```

---

## 2. Backend Service (backend-service)

AI 서비스는 아래 API와만 통신합니다.

---

### 2.1 Alerts (AI → Backend)

```http
POST /alerts
```

AI 서비스에서 처리된 이벤트를 backend-service로 전달

#### Headers

```text
x-api-key: {BACKEND_API_KEY}
```

---

#### Request Body

```json
{
  "device_id": "cap-001",
  "sound_type": "car_horn",
  "is_risk": true,
  "direction": "left",
  "confidence": 0.92,
  "stt_text": "빵빵",
  "raw_payload": {
    "transcript_hint": "빵빵",
    "metadata": {
      "source": "raspberry-pi"
    }
  }
}
```

---

#### Field 설명

| 필드          | 타입      | 필수 | 설명      |
| ----------- | ------- | -- | ------- |
| device_id   | string  | O  | 디바이스 ID |
| sound_type  | string  | O  | 소리 유형   |
| is_risk     | boolean | O  | 위험 여부   |
| direction   | string  | X  | 방향      |
| confidence  | float   | X  | 신뢰도     |
| stt_text    | string  | X  | STT 결과  |
| raw_payload | object  | X  | 원본 데이터  |

---

#### Response (Backend)

```json
{
  "id": 1,
  "device_id": "cap-001",
  "sound_type": "car_horn",
  "is_risk": true,
  "direction": "left",
  "confidence": 0.92,
  "stt_text": "빵빵",
  "created_at": "2025-01-01T00:00:00Z"
}
```

---

## 3. 전체 흐름

```text
[Device / Raspberry Pi]
        ↓
POST /ingest (AI Service)
        ↓
정규화 + STT
        ↓
POST /alerts (Backend Service)
        ↓
DB 저장 + WebSocket 전송
```

---

## 4. 인증 방식

| 구간               | 인증 방식      |
| ---------------- | ---------- |
| Device → AI      | x-ai-token |
| AI → Backend     | x-api-key  |
| Client → Backend | JWT        |

---

## ⚠ 중요

* STT는 ai-service에서 수행합니다.
* backend-service는 STT를 수행하지 않습니다.
* ai-service는 DB, WebSocket, 사용자 인증을 처리하지 않습니다.
* ai-service는 backend-service의 `/alerts` API로만 데이터를 전달합니다.

---
