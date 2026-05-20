import joblib
import os

MODEL_PATH = "models/severity_model.pkl"

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model not found. Run train.py first.")
    return joblib.load(MODEL_PATH)

def predict_severity(tool: str, raw_output: str) -> str:
    model = load_model()
    text = f"{tool} {raw_output}"
    prediction = model.predict([text])[0]
    return prediction

if __name__ == "__main__":
    # Quick test
    print(predict_severity("clamav", "Ransomware.WannaCry FOUND"))
    print(predict_severity("nmap", "Port 445 open microsoft-ds"))
    print(predict_severity("virustotal", '{"data": {"attributes": {"last_analysis_stats": {"malicious": 12}}}}'))