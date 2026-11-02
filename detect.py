# detect.py
import sys
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

FEATURES = ["pps", "syn_ack_ratio", "unique_src", "src_entropy",
            "avg_size", "udp_ratio", "icmp_ratio"]
MODEL_PATH = "model.pkl"


def train(csv="data/dataset.csv"):
    df = pd.read_csv(csv)
    X, y = df[FEATURES], df["label"]
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_tr, y_tr)
    print(classification_report(y_te, model.predict(X_te),
                                target_names=["normal", "attack"]))
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
    return model


def load():
    return joblib.load(MODEL_PATH)


def predict(model, row):
    """row: dict with the 7 FEATURES. Returns (label, confidence)."""
    X = pd.DataFrame([row])[FEATURES]
    proba = model.predict_proba(X)[0]
    label = int(proba.argmax())
    return label, float(proba[label])


if __name__ == "__main__":
    train()
