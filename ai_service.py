from fastapi import FastAPI, HTTPException
from ai_client import call_ai
from prompt import build_clamav_prompt, build_virustotal_prompt, build_nmap_prompt, build_email_prompt

app = FastAPI(title="SME CyberShield AI Service")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ai/explain/file")
async def explain_file(data: dict):
    try:
        prompt = build_clamav_prompt(data)
        return call_ai(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ai/explain/url")
async def explain_url(data: dict):
    try:
        prompt = build_virustotal_prompt(data)
        return call_ai(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ai/explain/network")
async def explain_network(data: dict):
    try:
        prompt = build_nmap_prompt(data)
        return call_ai(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ai/explain/email")
async def explain_email(data: dict):
    try:
        prompt = build_email_prompt(data)
        return call_ai(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))