from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()
clients = set()

html = """
<!DOCTYPE html>
<html>
<head>
    <title>شات محلي</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial; background: #1a1a1a; color: white; margin: 0; padding: 10px; }
        #messages { height: 80vh; overflow-y: auto; border: 1px solid #444; padding: 10px; margin-bottom: 10px; border-radius: 8px; }
        input { width: 75%; padding: 10px; border-radius: 5px; border: none; }
        button { width: 20%; padding: 10px; background: #4CAF50; color: white; border: none; border-radius: 5px; }
        .msg { margin: 5px 0; }
    </style>
</head>
<body>
    <h3>💬 الشات المحلي</h3>
    <div id="messages"></div>
    <input id="msg" placeholder="اكتب رسالتك...">
    <button onclick="send()">إرسال</button>
    <script>
        let ws = new WebSocket(`ws://${location.host}/ws/guest`);
        let messages = document.getElementById('messages');
        let input = document.getElementById('msg');
        ws.onmessage = (event) => {
            messages.innerHTML += `<div class="msg">${event.data}</div>`;
            messages.scrollTop = messages.scrollHeight;
        };
        function send() {
            if (input.value) {
                ws.send(input.value);
                input.value = '';
            }
        }
        input.addEventListener('keypress', (e) => { if(e.key === 'Enter') send(); });
    </script>
</body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()
    clients.add(websocket)
    try:
        await websocket.send_text(f"✅ أهلا {username} اتصلت بالشات")
        while True:
            data = await websocket.receive_text()
            for client in clients:
                await client.send_text(f"{username}: {data}")
    except WebSocketDisconnect:
        clients.remove(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)