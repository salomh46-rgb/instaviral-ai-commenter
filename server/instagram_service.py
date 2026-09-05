import os
import requests
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("instagram_service")

class InstagramGraphAPI:
    def __init__(self, access_token: Optional[str] = None, page_id: Optional[str] = None):
        self.access_token = access_token or os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
        self.page_id = page_id or os.getenv("INSTAGRAM_PAGE_ID", "")
        self.base_url = "https://graph.facebook.com/v19.0"

    @property
    def is_configured(self) -> bool:
        return bool(self.access_token and len(self.access_token) > 20)

    def reply_to_comment(self, comment_id: str, message: str) -> Dict[str, Any]:
        if not self.is_configured:
            logger.info(f"[SIMULATION] Replying to comment {comment_id}: {message}")
            return {
                "success": True,
                "mode": "SIMULATION",
                "id": f"sim_reply_{comment_id}",
                "message": message
            }

        url = f"{self.base_url}/{comment_id}/replies"
        payload = {"message": message, "access_token": self.access_token}
        try:
            resp = requests.post(url, json=payload, timeout=10)
            data = resp.json()
            if resp.status_code == 200 and "id" in data:
                return {"success": True, "mode": "LIVE", "id": data["id"]}
            return {"success": False, "mode": "LIVE", "error": data}
        except Exception as e:
            return {"success": False, "mode": "LIVE", "error": str(e)}

    def send_direct_message(self, recipient_id: str, message: str) -> Dict[str, Any]:
        if not self.is_configured:
            logger.info(f"[SIMULATION] Sending Direct Message to {recipient_id}: {message}")
            return {
                "success": True,
                "mode": "SIMULATION",
                "recipient_id": recipient_id,
                "message": message
            }

        url = f"{self.base_url}/me/messages"
        payload = {
            "recipient": {"id": recipient_id},
            "message": {"text": message},
            "access_token": self.access_token
        }
        try:
            resp = requests.post(url, json=payload, timeout=10)
            data = resp.json()
            if resp.status_code == 200:
                return {"success": True, "mode": "LIVE", "data": data}
            return {"success": False, "mode": "LIVE", "error": data}
        except Exception as e:
            return {"success": False, "mode": "LIVE", "error": str(e)}
