import json

def score_severity(tool: str, raw_output: str) -> str:
    text = raw_output.lower()

    if tool == "clamav":
        if "ransomware" in text or "trojan" in text:
            return "Critical"
        elif "found" in text and "ok" not in text:
            return "High"
        elif "suspicious" in text:
            return "Medium"
        else:
            return "Low"

    elif tool == "virustotal":
        try:
            data = json.loads(raw_output)
            malicious = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {}).get("malicious", 0)
            if malicious >= 10:
                return "Critical"
            elif malicious >= 5:
                return "High"
            elif malicious >= 1:
                return "Medium"
            else:
                return "Low"
        except Exception:
            return "High" if "malicious" in text or "phishing" in text else "Low"

    elif tool == "nmap":
        if any(p in text for p in ["445", "3389", "23", "4444"]):
            return "Critical"
        elif any(p in text for p in ["22", "3306", "5432", "6379"]):
            return "High"
        elif "open" in text:
            return "Medium"
        else:
            return "Low"

    return "Low"