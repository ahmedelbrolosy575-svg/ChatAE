import flet as ft
import asyncio
import websockets

ws = None

async def main(page: ft.Page):
    page.title = "Chat AE"
    page.window_width = 400
    page.window_height = 700
    
    chat = ft.ListView(expand=True, spacing=10, auto_scroll=True)
    msg_input = ft.TextField(hint_text="اكتب رسالتك...", expand=True)
    user_input = ft.TextField(label="اسمك في Chat AE", value="Ahmed")
    
    async def send_msg(e):
        global ws
        if msg_input.value and ws:
            await ws.send(msg_input.value)
            chat.controls.append(ft.Text(f"أنا: {msg_input.value}"))
            msg_input.value = ""
            page.update()
    
    async def connect():
        global ws
        try:
            uri = f"ws://192.168.100.11:8000/ws/{user_input.value}"
            ws = await websockets.connect(uri)
            chat.controls.append(ft.Text("✅ اتصلت بالسيرفر", color="green"))
            page.update()
            async for message in ws:
                chat.controls.append(ft.Text(message))
                page.update()
        except Exception as e:
            chat.controls.append(ft.Text(f"❌ خطأ: {e}", color="red"))
            page.update()
    
    send_btn = ft.ElevatedButton("إرسال", on_click=send_msg)
    page.add(user_input, chat, ft.Row([msg_input, send_btn]))
    asyncio.create_task(connect())

ft.app(target=main)