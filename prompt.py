
def build_clamav_prompt(data: dict) -> str:
    return f"""
You are a cybersecurity assistant helping Indian small business owners 
understand threats in simple language. No technical jargon.

A file scan has returned this result:
- File: {data['file']}
- Verdict: {data['verdict']}
- Threat name: {data['threat_name']}
- Threat type: {data['threat_type']}
- Severity: {data['severity']}

Write a response in this exact JSON format:
{{
  "summary": "2-3 sentences explaining what was found and why it is dangerous for a small business. No jargon.",
  "severity": "{data['severity']}",
  "threat_type": "{data['threat_type']}",
  "actions": ["Action 1", "Action 2", "Action 3"]
}}

Rules:
- If threat_type is ransomware → actions MUST include: disconnect from network, do not pay ransom, restore from backup
- If threat_type is trojan → actions MUST include: delete file, change all passwords, run full scan
- If verdict is CLEAN → summary says file is safe, actions is empty list []
- Keep summary under 3 sentences
- Speak directly to the business owner — use "your business", "your files"
- Return only valid JSON, nothing else. No extra text before or after.
"""


def build_virustotal_prompt(data: dict) -> str:
    total_engines = data['malicious'] + data['suspicious'] + data['clean']

    upi_keywords = [
        "paytm", "phonepe", "bhim", "upi", "sbi", "hdfc",
        "icici", "axis", "npci", "irctc", "gpay", "wallet",
        "netbanking", "kyc", "verify", "payment"
    ]
    url_lower = data['url'].lower()
    is_upi_fraud = any(kw in url_lower for kw in upi_keywords) and data['verdict'] == "MALICIOUS"
    threat_type = "upi_fraud" if is_upi_fraud else "phishing"

    return f"""
You are a cybersecurity assistant helping Indian small business owners 
understand threats in simple language. No technical jargon.

A URL scan has returned this result:
- URL: {data['url']}
- Verdict: {data['verdict']}
- Flagged by: {data['malicious']} out of {total_engines} security engines
- Suspicious flags: {data['suspicious']}
- UPI Fraud detected: {is_upi_fraud}

Write a response in this exact JSON format:
{{
  "summary": "2-3 sentences explaining what this URL is and why it is dangerous. Mention how many engines flagged it.",
  "severity": "High",
  "threat_type": "{threat_type}",
  "actions": ["Action 1", "Action 2", "Action 3"]
}}

Rules:
- If UPI Fraud is True → summary MUST mention this page is impersonating an Indian payment service. Actions MUST include: do not enter UPI PIN, do not enter OTP, report to cybercrime.gov.in
- If verdict is MALICIOUS → severity is High
- If verdict is SUSPICIOUS → severity is Medium
- If verdict is CLEAN → summary says URL appears safe, actions is empty list []
- Return only valid JSON, nothing else. No extra text before or after.
"""


def build_nmap_prompt(data: dict) -> str:
    ports_text = "\n".join([
        f"- Port {p['port']} ({p['service']}): Risk={p['risk']}, Reason={p['reason']}"
        for p in data['ports']
    ])

    severity = "Low"
    for p in data['ports']:
        if p['risk'] == "Critical":
            severity = "Critical"
            break
        elif p['risk'] == "High":
            severity = "High"
        elif p['risk'] == "Medium" and severity == "Low":
            severity = "Medium"

    return f"""
You are a cybersecurity assistant helping Indian small business owners 
understand network risks in simple language. No technical jargon.

A network scan of {data['target']} found {data['total_open_ports']} open port(s):
{ports_text}

Write a response in this exact JSON format:
{{
  "summary": "2-3 sentences explaining the overall network risk in simple terms. Mention the most dangerous port specifically.",
  "severity": "{severity}",
  "threat_type": "network_exposure",
  "actions": ["Action 1", "Action 2", "Action 3"]
}}

Rules:
- If port 445 is open → summary MUST mention WannaCry ransomware risk specifically
- If port 3389 is open → summary MUST mention remote desktop hijacking risk
- If port 3306 is open → summary MUST mention database exposed to internet
- If port 22 is open → actions MUST include: restrict SSH to trusted IP addresses only
- If no open ports → summary says network looks secure
- Never say just "port is open" — always explain what an attacker can do with it
- Return only valid JSON, nothing else. No extra text before or after.
"""


def build_email_prompt(data: dict) -> str:
    return f"""
You are a cybersecurity assistant helping Indian small business owners 
understand email phishing threats in simple language. No technical jargon.

An email header analysis returned this result:
- Subject: {data['subject']}
- From domain: {data['from_domain']}
- Actual sending domain: {data['sending_domain']}
- SPF check: {data['spf_status']}
- DKIM check: {data['dkim_status']}
- DMARC check: {data['dmarc_status']}
- Domain mismatch: {data['domain_mismatch']}
- Sender spoofed: {data['spoofed']}
- Indian brand being impersonated: {data['upi_brand_targeted']}
- Verdict: {data['verdict']}

Write a response in this exact JSON format:
{{
  "summary": "2-3 sentences explaining whether this email is safe or dangerous and why. Mention the brand being impersonated if any.",
  "severity": "{data['severity']}",
  "threat_type": "phishing",
  "actions": ["Action 1", "Action 2", "Action 3"]
}}

Rules:
- If spoofed is True and upi_brand_targeted is not null → summary MUST say the email is pretending to be that brand and the sender address is fake
- If verdict is PHISHING → actions MUST include: do not click any links, do not enter OTP or UPI PIN, delete the email, report to cybercrime.gov.in
- If verdict is CLEAN → summary says email appears legitimate, actions is empty list []
- Explain SPF/DKIM failures in plain English — e.g. "The email failed security checks that prove the sender is who they claim to be"
- Return only valid JSON, nothing else. No extra text before or after.
"""