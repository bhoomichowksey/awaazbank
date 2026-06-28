# 🎙 AwaazBank
### *Vernacular Agentic AI for Rural Banking on WhatsApp*

> **"Awaaz uthao, account banao"** — Raise your voice, open your account.

Built for **SBI Hackathon @ GFF 2026** | Theme: Agentic AI & Emerging Tech | Problem: Customer Acquisition

---

## 🧠 What is AwaazBank?

AwaazBank lets any rural Indian citizen send a **WhatsApp voice note in their own language** — Bhojpuri, Marathi, Odia, Bengali, and 10+ more — and get fully onboarded into SBI without:
- Visiting a branch
- Typing anything
- Downloading an app

The AI agent handles everything autonomously: it listens, understands, responds in voice, verifies identity via Aadhaar, and opens the account — end to end.

---

## 🚀 Key Features

| Feature | Description |
|---|---|
| 🎙 Voice-first | Accepts WhatsApp voice notes in 10+ Indian languages |
| 🇮🇳 Bhashini-powered | Uses India's sovereign NLP platform — data never leaves India |
| 🤖 Fully Agentic | LangChain agent autonomously drives the full KYC flow |
| 🔐 RBI-compliant KYC | Aadhaar OTP + liveness check via AWS Rekognition |
| 🔁 Drop-off recovery | Agent follows up in 24hrs if user stops midway |
| 📊 Branch dashboard | Real-time Streamlit dashboard for branch managers |

---

## 🏗️ Architecture

```
User sends WhatsApp voice note (any Indian language)
        ↓
WhatsApp Business API → AwaazBank webhook
        ↓
Bhashini STT → text transcription + dialect detection
        ↓
LangChain Agent → intent understanding + step decision
        ↓
KYC Flow: Account type → Aadhaar OTP → Selfie liveness
        ↓
SBI Core Banking API → Account created
        ↓
Bhashini TTS → Voice confirmation sent back on WhatsApp
        ↓
Drop-off? → Follow-up agent triggers after 24hrs
        ↓
Streamlit dashboard updated in real time
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Channel | WhatsApp Business API (Meta) |
| Voice STT/TTS | Bhashini API (Govt of India) |
| Language Detection | langdetect + custom dialect classifier |
| Agentic Core | LangChain Agents |
| LLM | Claude Sonnet / GPT-4o |
| KYC | Aadhaar OTP API + AWS Rekognition |
| Backend | FastAPI (Python) |
| Database | PostgreSQL + Redis |
| Dashboard | Streamlit |
| Hosting | AWS |

---

## 📁 Project Structure

```
awaazbank/
├── README.md
├── requirements.txt
├── agent/
│   └── agent.py          # LangChain agentic KYC flow
├── stt/
│   └── bhashini_stt.py   # Bhashini STT + TTS integration
├── whatsapp/
│   └── webhook.py        # FastAPI WhatsApp webhook handler
├── kyc/
│   └── kyc_handler.py    # Aadhaar OTP + liveness check
├── dashboard/
│   └── app.py            # Streamlit branch manager dashboard
└── demo/
    └── sample_flow.txt   # Example conversation flow
```

---

## ⚙️ Setup

```bash
git clone https://github.com/yourusername/awaazbank.git
cd awaazbank
pip install -r requirements.txt
```

Set environment variables:
```bash
export WHATSAPP_TOKEN=your_token
export BHASHINI_API_KEY=your_key
export OPENAI_API_KEY=your_key         # or Anthropic key
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_key
```

Run the webhook server:
```bash
uvicorn whatsapp.webhook:app --reload --port 8000
```

Run the dashboard:
```bash
streamlit run dashboard/app.py
```

---

## 💼 Business Impact

- **95% cost reduction** — ₹30 per onboarding vs ₹1,000+ at branch
- **400M+ addressable users** — India's unbanked/underbanked population
- **Zero app download** — works on WhatsApp which rural India already uses
- **Jan Dhan aligned** — directly supports India's financial inclusion mandate

---

## 👤 Team

Solo submission | SBI Hackathon @ GFF 2026

---

## 📄 License

MIT License
