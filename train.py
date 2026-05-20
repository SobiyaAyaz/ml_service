from data_generator import generate_training_data
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

def train_model():
    print("Generating training data...")
    data = generate_training_data(500)

    texts = [f"{d['tool']} {d['raw_output']}" for d in data]
    labels = [d["label"] for d in data]

    X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    print("Training model...")
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    print(classification_report(y_test, y_pred))

    os.makedirs("models", exist_ok=True)
    joblib.dump(pipeline, "models/severity_model.pkl")
    print("Model saved to models/severity_model.pkl")

if __name__ == "__main__":
    train_model()