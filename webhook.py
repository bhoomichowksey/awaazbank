"""
AwaazBank — WhatsApp Business API Webhook
Receives incoming voice messages, routes to the AI agent,
and sends voice replies back to the user.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx
import base64
import os
import asyncio

from stt.bhashini_stt import audio_to_text, text_to_audio, detect_language
from agent.agent import build_agent

app = FastAPI(title="AwaazBank Webhook")

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID", "")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "awaazbank_verify")

# In-memory session store (use Redis in production)
user_sessions: dict = {}


# ── Webhook verification (Meta requirement) ──────────────────────────────────

@app.get("/webhook")
async def verify_webhook(request: Request):
    params = dict(request.query_params)
    if (
        params.get("hub.mode") == "subscribe"
        and params.get("hub.verify_token") == VERIFY_TOKEN
    ):
        return int(params["hub.challenge"])
    raise HTTPException(status_code=403, detail="Verification failed")


# ── Incoming message handler ─────────────────────────────────────────────────

@app.post("/webhook")
async def receive_message(request: Request):
    body = await request.json()

    try:
        entry = body["entry"][0]["changes"][0]["value"]
        message = entry["messages"][0]
        phone_number = message["from"]
        msg_type = message["type"]

        if msg_type == "audio":
            # Download the voice note
            audio_id = message["audio"]["id"]
            audio_base64 = await download_whatsapp_audio(audio_id)

            # Transcribe using Bhashini STT
            stt_result = audio_to_text(audio_base64)
            transcribed_text = stt_result["text"]
            language = detect_language(transcribed_text)

            # Get or create agent session for this user
            if phone_number not in user_sessions:
                user_sessions[phone_number] = {
                    "agent": build_agent(language_code=language),
                    "language": language,
                }

            session = user_sessions[phone_number]
            agent = session["agent"]

            # Run agent
            response = agent.invoke({"input": transcribed_text})
            reply_text = response["output"]

            # Convert reply to voice and send back
            reply_audio = text_to_audio(reply_text, target_language=language)
            await send_whatsapp_audio(phone_number, reply_audio)

        elif msg_type == "text":
            # Fallback: handle text messages too
            text = message["text"]["body"]
            if phone_number not in user_sessions:
                user_sessions[phone_number] = {
                    "agent": build_agent(),
                    "language": "hi",
                }
            session = user_sessions[phone_number]
            response = session["agent"].invoke({"input": text})
            await send_whatsapp_text(phone_number, response["output"])

    except (KeyError, IndexError):
        pass  # Ignore non-message webhooks (status updates, etc.)

    return JSONResponse(content={"status": "ok"})


# ── WhatsApp API helpers ─────────────────────────────────────────────────────

async def download_whatsapp_audio(audio_id: str) -> str:
    """Download audio from WhatsApp and return as base64."""
    async with httpx.AsyncClient() as client:
        # Get media URL
        url_resp = await client.get(
            f"https://graph.facebook.com/v18.0/{audio_id}",
            headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
        )
        media_url = url_resp.json()["url"]

        # Download audio
        audio_resp = await client.get(
            media_url,
            headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
        )
        return base64.b64encode(audio_resp.content).decode()


async def send_whatsapp_audio(phone_number: str, audio_base64: str):
    """Send voice note back to user on WhatsApp."""
    # TODO: Upload audio to WhatsApp media and send
    print(f"[→ WhatsApp {phone_number}] Sending voice reply")


async def send_whatsapp_text(phone_number: str, text: str):
    """Send text message to user on WhatsApp."""
    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_ID}/messages",
            headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}"},
            json={
                "messaging_product": "whatsapp",
                "to": phone_number,
                "type": "text",
                "text": {"body": text},
            }
        )


# ── Run ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
