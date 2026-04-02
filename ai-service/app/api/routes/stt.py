from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException
from app.api.deps import require_ai_token
from app.schemas.stt import STTResultOut
from app.services.file_store import FileStoreService
from app.services.pipeline import PipelineService
import time

router = APIRouter(prefix="/ingest/stt", tags=["stt"])
pipeline = PipelineService()
file_store = FileStoreService()


@router.post("", response_model=STTResultOut, dependencies=[Depends(require_ai_token)])
async def ingest_stt(
    device_id: str = Form(...),
    sound_type: str = Form("conversation"),
    direction: str = Form("unknown"),
    confidence: float = Form(1.0),
    audio: UploadFile = File(...),
):
    api_start = time.perf_counter()

    print("[API] /ingest/stt 요청 도착")
    print(f"[API] device_id={device_id}, sound_type={sound_type}, filename={audio.filename}")

    save_start = time.perf_counter()
    file_path = await file_store.save_upload(audio)
    save_elapsed = time.perf_counter() - save_start

    print(f"[API] 업로드 저장 완료: {file_path}")
    print(f"[API] 파일 저장 시간: {save_elapsed:.4f}s")

    try:
        stt_text, normalized, backend_response, timing = await pipeline.process_stt_file(
            file_path=file_path,
            device_id=device_id,
            sound_type=sound_type,
            direction=direction,
            confidence=confidence,
            metadata={"filename": audio.filename},
        )

        api_total_elapsed = time.perf_counter() - api_start

        final_timing = {
            "save_sec": round(save_elapsed, 4),
            **timing,
            "api_total_sec": round(api_total_elapsed, 4),
        }

        print(f"[API] 전체 응답 시간: {api_total_elapsed:.4f}s")

        return STTResultOut(
            message="STT processed and forwarded successfully",
            stt_text=stt_text,
            normalized_payload=normalized,
            backend_response=backend_response,
            timing=final_timing,
        )
    except Exception as e:
        print(f"[API] STT 처리 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        file_store.delete_file(file_path)
        print(f"[API] 임시 파일 삭제 완료: {file_path}")