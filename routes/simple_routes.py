# routes/simple_routes.py
from fastapi import APIRouter,WebSocket
import asyncio


router = APIRouter(prefix="/simple", tags=["simple Router"])

@router.get("/run")
def root():
    return {"message": "FastAPI server is running!"}

@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.websocket("/ws/audio")
async def websocket_audio(websocket: WebSocket):
    await websocket.accept()
    # Har client ke liye nayi file create karna (optional)
    try:
        while True:
            chunk = await websocket.receive_bytes()
            translated_text = "hello hello"
            try:
                for char in translated_text:
                    await websocket.send_text(char)
                    await asyncio.sleep(0.1)
            except:
                print("Client disconnected while sending")
                break
    except Exception:
        print("Client disconnected")
    finally:
        await websocket.close()

