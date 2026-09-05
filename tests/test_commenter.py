import unittest
from fastapi.testclient import TestClient
from server.main import app
from server.ai_engine import InstaViralAIEngine

class TestInstaViralAI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.engine = InstaViralAIEngine(brand_name="Jasper Store", default_price="300,000 so'm")

    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "active")
        self.assertIn("InstaViral AI", data["service"])

    def test_pricing_intent_classification(self):
        res = self.engine.generate_reply("Assalomu alaykum narxi qancha?", username="ali_99")
        self.assertEqual(res["intent"], "PRICING")
        self.assertTrue(res["send_dm"])
        self.assertIn("300,000 so'm", res["reply_text"])
        self.assertIn("@ali_99", res["reply_text"])

    def test_compliment_intent_classification(self):
        res = self.engine.generate_reply("Video daxshat chiqibdi zo'r 🔥", username="dilnoza")
        self.assertEqual(res["intent"], "COMPLIMENT")
        self.assertEqual(res["sentiment"], "POSITIVE")
        self.assertIn("@dilnoza", res["reply_text"])

    def test_shipping_intent_classification(self):
        res = self.engine.generate_reply("Samarqandga dastavka bormi?", username="jasur")
        self.assertEqual(res["intent"], "SHIPPING_LOCATION")
        self.assertIn("yetkazib", res["reply_text"].lower())

    def test_process_comment_api(self):
        payload = {
            "username": "shoxrux_pro",
            "comment_text": "Qayerdan sotib olsak bo'ladi?",
            "media_id": "reels_123"
        }
        response = self.client.post("/api/comments/process", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("analysis", data)
        self.assertEqual(data["analysis"]["intent"], "PURCHASE_INTENT")

    def test_webhook_verification_handshake(self):
        response = self.client.get("/webhook?hub.mode=subscribe&hub.challenge=test_12345&hub.verify_token=jasper_instaviral_token_2026")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "test_12345")

    def test_analytics_api(self):
        response = self.client.get("/api/analytics")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("total_comments_processed", data)
        self.assertIn("positive_sentiment_percent", data)

if __name__ == "__main__":
    unittest.main()
