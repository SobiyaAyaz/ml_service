import json
import random

def generate_training_data(n=200):
    """
    Generates synthetic scan data for training the severity classifier.
    """
    data = []

    for _ in range(n):
        tool = random.choice(["clamav", "virustotal", "nmap"])

        if tool == "clamav":
            label = random.choice(["Low", "Medium", "High", "Critical"])
            text = {
                "Low": "ClamAV scan result: OK",
                "Medium": "ClamAV scan result: Suspicious.Generic detected",
                "High": "ClamAV scan result: Trojan.Agent found",
                "Critical": "ClamAV scan result: Ransomware.WannaCry FOUND"
            }[label]

        elif tool == "virustotal":
            malicious = {"Low": 0, "Medium": 2, "High": 7, "Critical": 15}
            label = random.choice(["Low", "Medium", "High", "Critical"])
            count = malicious[label]
            text = json.dumps({"data": {"attributes": {"last_analysis_stats": {"malicious": count}}}})

        else:
            label = random.choice(["Low", "Medium", "High", "Critical"])
            ports = {
                "Low": "No open ports found",
                "Medium": "Port 80 open (http)",
                "High": "Port 22 open (ssh)",
                "Critical": "Port 445 open (microsoft-ds), Port 3389 open (rdp)"
            }[label]
            text = ports

        data.append({"tool": tool, "raw_output": text, "label": label})

    return data