import os
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
app = FastAPI
clients = set()
@app.get("/")
def home():
    return {"status": "ChatAE شغال ✅"}

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()
    clients.add(websocket)
    try:
        await websocket.send_text(f"✅ اهلا {username} اتصلت بالشات")
        while True:
            data = await websocket.receive_text()
            for client in clients:
                await client.send_text(f"{username}: {data}")
    except WebSocketDisconnect:
        clients.remove(websocket)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
