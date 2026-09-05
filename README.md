# InstaViral AI — Instagram Smart Reels & Post AI Auto-Commenter 🚀

> **Conversational AI Engagement Autopilot for Instagram Reels & Posts** that semantically analyzes viewer comments in real-time, generates humanized, context-aware responses, and automates Direct Message (DM) lead generation with anti-ban delay protection.

Developed by **Javohirbek Asqarov (Jasper)**.

---

## ✨ Features

- 🧠 **Context-Aware Semantic & Sentiment AI Engine**:
  - **Pricing & Inquiries**: Automatically extracts pricing questions (*"Narxi qancha?", "Nechpul?", "How much?"*) and replies with exact rates while triggering instant DM links.
  - **Praise & Compliments**: Detects positive vibes (*"Zo'r video 🔥", "Daxshat", "Super"*) and engages with warm, appreciative brand personality.
  - **Delivery & Locations**: Answers shipping terms (*"Dastavka bormi?", "Yetkazib berish"*), regional timelines, and store addresses.
  - **Order Intents**: Converts interest (*"Sotib olmoqchiman", "Buyurtma"*) directly into sales with CTAs.
- 🛡️ **Anti-Ban Humanized Delay & AI Variation Engine**: Randomizes response delays (3-9s) and rotates natural paraphrased replies to safeguard Instagram accounts.
- 📱 **Interactive Instagram Reels Simulator & Dashboard**: Built-in interactive mobile Reels UI with live comment simulation, real-time typing indicators, and instant Auto-DM toast notifications.
- 🔗 **Instagram Graph API & Webhook Handshake**: Official Meta Webhook verification (`GET /webhook`) and event listener (`POST /webhook`) ready for live Instagram Professional / Creator accounts.
- 📊 **Real-Time Analytics & CRM Log**: Tracks total comments, sentiment ratios, direct leads captured, and response speed.
- 🧪 **100% Automated Test Coverage**: Comprehensive unittest suite verifying all intents, webhook handshakes, and API endpoints.

---

## 🚀 Quick Start (Local Setup)

### 1. Run the Backend API:
```bash
cd instaviral_ai_commenter
pip install -r server/requirements.txt
python -m uvicorn server.main:app --port 8000 --reload
```
API Documentation will be live at: `http://127.0.0.1:8000/docs`

### 2. Launch the Interactive Instagram Simulator:
Open `client/index.html` (or `index.html`) directly in your browser.

---

## 🧪 Run Automated Tests

```bash
python -m unittest discover tests/
```

---

## 🛠️ How to Connect Your Live Instagram Account:

1. Switch your Instagram account to **Professional (Creator or Business)** and link it to a **Facebook Page**.
2. Go to [developers.facebook.com](https://developers.facebook.com/) and create a Meta App.
3. Add the **Instagram Graph API** product and generate a User / Page Access Token with `instagram_manage_comments` and `instagram_manage_messages` permissions.
4. Set your Webhook URL to: `https://your-domain.com/webhook` with the verify token `jasper_instaviral_token_2026`.
5. Enter your Access Token in the dashboard settings — the AI will now automatically reply to real comments on your Instagram videos!

---

## 📄 License
MIT License. Created with ❤️ by **Javohirbek Asqarov (Jasper)**.
