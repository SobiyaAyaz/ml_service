# 🛡️ SME CyberShield — AI/ML Microservice
**Sobiya | FastAPI + Gemini AI**

Receives raw scan results from the backend and returns plain-English explanations for the dashboard.

---

## 📁 Files
```
ml_service/
├── ai_service.py       # FastAPI app — 4 endpoints
├── ai_client.py        # Gemini API integration
├── prompts.py          # Prompt templates
├── severity.py         # Severity scorer
├── upi_matcher.py      # UPI fraud detector
├── train.py            # Train ML model
├── predict.py          # ML predictions
├── data_generator.py   # Synthetic training data
├── test_endpoints.py   # Test all endpoints
├── .env                # API key (do not commit)
└── requirements.txt
```

---

## ⚙️ Setup

```powershell
pip install -r requirements.txt
python train.py
uvicorn ai_service:app --reload --port 8000
```

Add your Gemini API key to `.env`:
```
GEMINI_API_KEY=your_key_here
```
Get it free from: https://aistudio.google.com/app/apikey

---

## 🔌 Endpoints

| Method | Endpoint | Tool |
|--------|----------|------|
| POST | `/ai/explain/file` | ClamAV |
| POST | `/ai/explain/url` | VirusTotal |
| POST | `/ai/explain/network` | Nmap |
| POST | `/ai/explain/email` | Email Header |

All endpoints return:
```json
{
  "summary": "Plain English explanation.",
  "severity": "Critical",
  "threat_type": "ransomware",
  "actions": ["Action 1", "Action 2", "Action 3"]
}
```

---

## 🧪 Test
```powershell
python test_endpoints.py
```
Or open: `http://localhost:8000/docs`

---

## 👩‍💻 Built By
**Sobiya** — AI & ML Integration  
Team: Noor · Sireen · Sobiya · Nayef · Ameen
