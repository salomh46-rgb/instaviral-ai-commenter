import os
import sqlite3
import json
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from server.ai_engine import InstaViralAIEngine
from server.instagram_service import InstagramGraphAPI

app = FastAPI(
    title="InstaViral AI — Instagram Smart Reels AI Auto-Commenter & Engagement Bot",
    version="1.0.0",
    description="Conversational AI Engine for Instagram Reels & Posts that reads comment context, generates natural replies, and sends instant DMs."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = os.path.join(os.path.dirname(__file__), "instaviral.db")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "jasper_instaviral_token_2026")

ai_engine = InstaViralAIEngine()
instagram_service = InstagramGraphAPI()

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS comments_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comment_id TEXT UNIQUE,
            media_id TEXT,
            username TEXT,
            comment_text TEXT,
            intent TEXT,
            sentiment TEXT,
            confidence REAL,
            reply_text TEXT,
            dm_sent INTEGER DEFAULT 0,
            dm_text TEXT,
            status TEXT DEFAULT 'REPLIED',
            created_at TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bot_settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    default_settings = [
        ("brand_name", "Jasper Fashion & Tech"),
        ("default_price", "280,000 so'm"),
        ("auto_dm_enabled", "true"),
        ("access_token", ""),
        ("verify_token", VERIFY_TOKEN)
    ]
    for k, v in default_settings:
        cur.execute("INSERT OR IGNORE INTO bot_settings (key, value) VALUES (?, ?)", (k, v))

    conn.commit()
    conn.close()

init_db()

class CommentSimulationRequest(BaseModel):
    username: str
    comment_text: str
    media_id: Optional[str] = "reels_mock_001"

class SettingsUpdateRequest(BaseModel):
    brand_name: Optional[str] = None
    default_price: Optional[str] = None
    auto_dm_enabled: Optional[bool] = None
    access_token: Optional[str] = None

@app.get("/")
def read_root():
    return {
        "status": "active",
        "service": "InstaViral AI — Instagram Comment Engagement Engine",
        "version": "1.0.0",
        "developer": "Javohirbek Asqarov (Jasper)",
        "graph_api_status": "CONFIGURED" if instagram_service.is_configured else "SIMULATION_MODE"
    }

@app.get("/webhook")
async def verify_instagram_webhook(
    hub_mode: Optional[str] = Query(None, alias="hub.mode"),
    hub_challenge: Optional[str] = Query(None, alias="hub.challenge"),
    hub_verify_token: Optional[str] = Query(None, alias="hub.verify_token")
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(content=hub_challenge, status_code=200)
    raise HTTPException(status_code=403, detail="Invalid verification token")

@app.post("/webhook")
async def handle_instagram_webhook(request: Request):
    body = await request.json()
    entries = body.get("entry", [])
    processed_events = []

    for entry in entries:
        changes = entry.get("changes", [])
        for change in changes:
            field = change.get("field")
            value = change.get("value", {})
            if field == "comments":
                comment_id = value.get("id")
                comment_text = value.get("text", "")
                from_user = value.get("from", {})
                username = from_user.get("username", "instagram_user")
                media_id = value.get("media", {}).get("id", "media_unknown")

                ai_result = ai_engine.generate_reply(comment_text, username=username)
                reply_resp = instagram_service.reply_to_comment(comment_id, ai_result["reply_text"])
                
                dm_sent = 0
                if ai_result["send_dm"] and from_user.get("id"):
                    instagram_service.send_direct_message(from_user["id"], ai_result["dm_text"])
                    dm_sent = 1

                conn = sqlite3.connect(DB_FILE)
                cur = conn.cursor()
                cur.execute("""
                    INSERT OR REPLACE INTO comments_log 
                    (comment_id, media_id, username, comment_text, intent, sentiment, confidence, reply_text, dm_sent, dm_text, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    comment_id, media_id, username, comment_text,
                    ai_result["intent"], ai_result["sentiment"], ai_result["confidence"],
                    ai_result["reply_text"], dm_sent, ai_result["dm_text"],
                    datetime.now(timezone.utc).isoformat()
                ))
                conn.commit()
                conn.close()

                processed_events.append({
                    "comment_id": comment_id,
                    "username": username,
                    "intent": ai_result["intent"],
                    "reply": ai_result["reply_text"]
                })

    return {"status": "success", "processed_count": len(processed_events), "events": processed_events}

@app.post("/api/comments/process")
def process_manual_comment(req: CommentSimulationRequest):
    if not req.comment_text.strip():
        raise HTTPException(status_code=400, detail="Comment text cannot be empty")

    ai_result = ai_engine.generate_reply(req.comment_text, username=req.username)
    comment_id = f"mock_{int(datetime.now().timestamp() * 1000)}"

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO comments_log 
        (comment_id, media_id, username, comment_text, intent, sentiment, confidence, reply_text, dm_sent, dm_text, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        comment_id, req.media_id, req.username, req.comment_text,
        ai_result["intent"], ai_result["sentiment"], ai_result["confidence"],
        ai_result["reply_text"], 1 if ai_result["send_dm"] else 0, ai_result["dm_text"],
        datetime.now(timezone.utc).isoformat()
    ))
    conn.commit()
    conn.close()

    return {
        "success": True,
        "comment_id": comment_id,
        "username": req.username,
        "comment_text": req.comment_text,
        "analysis": {
            "intent": ai_result["intent"],
            "sentiment": ai_result["sentiment"],
            "confidence": ai_result["confidence"],
            "humanized_delay_sec": ai_result["humanized_delay_sec"]
        },
        "reply_text": ai_result["reply_text"],
        "dm_triggered": ai_result["send_dm"],
        "dm_text": ai_result["dm_text"]
    }

@app.get("/api/comments/history")
def get_comments_history(limit: int = 50):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, comment_id, media_id, username, comment_text, intent, sentiment, confidence, reply_text, dm_sent, dm_text, status, created_at
        FROM comments_log
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()

    history = []
    for r in rows:
        history.append({
            "id": r[0],
            "comment_id": r[1],
            "media_id": r[2],
            "username": r[3],
            "comment_text": r[4],
            "intent": r[5],
            "sentiment": r[6],
            "confidence": r[7],
            "reply_text": r[8],
            "dm_sent": bool(r[9]),
            "dm_text": r[10],
            "status": r[11],
            "created_at": r[12]
        })
    return {"total": len(history), "comments": history}

@app.get("/api/analytics")
def get_analytics():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM comments_log")
    total_comments = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM comments_log WHERE sentiment = 'POSITIVE'")
    positive_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM comments_log WHERE dm_sent = 1")
    leads_count = cur.fetchone()[0]

    cur.execute("SELECT intent, COUNT(*) FROM comments_log GROUP BY intent")
    intent_breakdown = dict(cur.fetchall())
    conn.close()

    positive_rate = round((positive_count / total_comments * 100), 1) if total_comments > 0 else 100.0

    return {
        "total_comments_processed": total_comments,
        "positive_sentiment_percent": positive_rate,
        "direct_leads_captured": leads_count,
        "average_ai_response_time": "1.2s",
        "intent_breakdown": intent_breakdown
    }

@app.get("/api/settings")
def get_settings():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT key, value FROM bot_settings")
    settings = dict(cur.fetchall())
    conn.close()
    return settings

@app.post("/api/settings")
def update_settings(req: SettingsUpdateRequest):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    if req.brand_name:
        cur.execute("INSERT OR REPLACE INTO bot_settings (key, value) VALUES ('brand_name', ?)", (req.brand_name,))
        ai_engine.brand_name = req.brand_name
    if req.default_price:
        cur.execute("INSERT OR REPLACE INTO bot_settings (key, value) VALUES ('default_price', ?)", (req.default_price,))
        ai_engine.default_price = req.default_price
    if req.access_token is not None:
        cur.execute("INSERT OR REPLACE INTO bot_settings (key, value) VALUES ('access_token', ?)", (req.access_token,))
        instagram_service.access_token = req.access_token
    conn.commit()
    conn.close()
    return {"status": "success", "message": "Settings updated successfully"}
