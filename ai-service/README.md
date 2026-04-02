# ai-service

청각장애인 생활 보조 시스템의 AI 서비스입니다.

이 서비스는 라즈베리파이(또는 AI 입력 장치)로부터 전달받은 데이터를 처리하고,
필요 시 STT를 수행한 뒤, 최종 결과를 backend-service로 전달하는 역할을 담당합니다.

---

# 1. 서비스 개요

현재 ai-service는 두 가지 기능을 담당합니다.

## 1) 위험 소리 / 호출 감지 이벤트 처리

라즈베리파이에서 이미 분석한 결과를 ai-service가 받아 정규화한 뒤 backend-service로 전달합니다.

예시:

* 자동차 경적 감지
* 사이렌 감지
* 자전거 벨 감지
* 사람 호출음 감지 ("야", "저기요", "잠시만요" 등)
* 방향 정보 포함 (left / right / front / back / unknown)

즉, 이 기능은 **이벤트 처리 및 전달**이 핵심입니다.

---

## 2) 소통 모드 STT 처리

앱 또는 워치에서 소통 모드가 시작되면,
라즈베리파이가 수집한 음성 파일을 ai-service로 전송합니다.

ai-service는 해당 음성 파일에 대해 Whisper 기반 STT를 수행하고,
텍스트 결과를 backend-service로 전달합니다.

즉, 이 기능은 **음성 파일 업로드 → STT → 결과 전달**이 핵심입니다.

---

# 2. 역할 분리

## ai-service

* `x-ai-token` 기반 인증
* 위험 소리 / 호출 감지 이벤트 수신
* 소통 모드 음성 파일 수신
* 입력 데이터 검증 및 정규화
* Whisper 기반 STT 수행
* backend-service의 `/alerts`로 HTTP forwarding

## backend-service

* ai-service로부터 alerts 수신
* DB 저장
* Redis / WebSocket / 클라이언트 푸시
* 사용자 / 설정 / 인증 처리

---

# 3. 전체 동작 구조

## A. 위험 소리 / 호출 감지 흐름

```text
[4-ch microphone]
        ↓
[Raspberry Pi]
위험 소리 감지 / 호출 감지 / 방향 추정
        ↓
POST /ingest/event (AI Service)
        ↓
정규화
        ↓
POST /alerts (Backend Service)
        ↓
DB 저장 + 실시간 전송
```

---

## B. 소통 모드 STT 흐름

```text
[Watch / App]
소통 모드 시작
        ↓
[4-ch microphone]
        ↓
[Raspberry Pi]
음성 파일 수집
        ↓
POST /ingest/stt (AI Service)
        ↓
Whisper STT
        ↓
정규화
        ↓
POST /alerts (Backend Service)
        ↓
DB 저장 + 실시간 전송
```

---

# 4. 디렉토리 구조

```text
ai-service/
├─ app/
│  ├─ api/
│  │  ├─ __init__.py
│  │  ├─ deps.py
│  │  └─ routes/
│  │      ├─ __init__.py
│  │      ├─ health.py
│  │      ├─ ingest.py
│  │      ├─ event.py
│  │      └─ stt.py
│  │
│  ├─ core/
│  │  ├─ __init__.py
│  │  ├─ config.py
│  │  └─ security.py
│  │
│  ├─ schemas/
│  │  ├─ __init__.py
│  │  ├─ ingest.py
│  │  ├─ event.py
│  │  ├─ stt.py
│  │  └─ forward.py
│  │
│  ├─ services/
│  │  ├─ __init__.py
│  │  ├─ normalizer.py
│  │  ├─ stt_service.py
│  │  ├─ forwarder.py
│  │  ├─ pipeline.py
│  │  └─ file_store.py
│  │
│  ├─ utils/
│  │  ├─ __init__.py
│  │  └─ logger.py
│  │
│  └─ main.py
│
├─ tmp_uploads/
├─ .dockerignore
├─ Dockerfile
├─ requirements.txt
└─ README.md
```

---

# 5. API Endpoints

## 5.1 Health Check

```http
GET /health
```

### Response

```json
{
  "status": "ok",
  "service": "hearing-ai-service",
  "env": "development"
}
```

---

## 5.2 Event Ingest (위험 소리 / 호출 감지)

```http
POST /ingest/event
```

### Headers

```
x-ai-token: {AI_SHARED_TOKEN}
```

### Request Body

```json
{
  "device_id": "cap-001",
  "event_type": "risk_sound",
  "sound_type": "car_horn",
  "is_risk": true,
  "direction": "left",
  "confidence": 0.93,
  "metadata": {
    "source": "raspberry-pi"
  }
}
```

---

## 5.3 STT Ingest (소통 모드)

```http
POST /ingest/stt
```

### Headers

```
x-ai-token: {AI_SHARED_TOKEN}
```

### Form Data

* device_id: string
* sound_type: string
* audio: file

### Response

```json
{
  "message": "STT processed and forwarded successfully",
  "stt_text": "안녕하세요",
  "normalized_payload": {
    "device_id": "cap-001",
    "sound_type": "conversation",
    "is_risk": false,
    "direction": "unknown",
    "confidence": 1.0,
    "stt_text": "안녕하세요"
  },
  "backend_response": {
    "id": 1
  }
}
```

---

# 6. 인증 방식

| 구간               | 인증 방식      |
| ---------------- | ---------- |
| Device → AI      | x-ai-token |
| AI → Backend     | x-api-key  |
| Client → Backend | JWT        |

---

# ⚠ 중요

* STT는 ai-service에서 수행합니다.
* backend-service는 STT를 수행하지 않습니다.
* ai-service는 DB, WebSocket, 사용자 인증을 처리하지 않습니다.
* ai-service는 backend-service의 `/alerts` API로만 데이터를 전달합니다.
