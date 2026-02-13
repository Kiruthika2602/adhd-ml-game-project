import pandas as pd
import joblib
import os

# ----------------------------
# 1️⃣ RESOLVE ABSOLUTE PATHS
# ----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "adhd_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "model", "scaler.pkl")

if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
    raise FileNotFoundError("Model or scaler file not found. Train the model first.")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# ----------------------------
# 2️⃣ ENCODING MAPS
# ----------------------------
EDU_MAP = {"child": 0, "teen": 1, "undergrad": 2, "adult": 3}
GENDER_MAP = {"male": 1, "female": 0}

FEATURE_ORDER = [
    "Age", "Gender", "EducationStage",
    "InattentionScore", "HyperactivityScore", "ImpulsivityScore",
    "SymptomSum", "Daydream", "SleepHours", "ScreenTime", "FamilyHistory"
]

# ----------------------------
# 3️⃣ PREDICTION FUNCTION
# ----------------------------
def predict_adhd(features: dict):
    processed = features.copy()

    # Safe encoding
    processed["Gender"] = GENDER_MAP.get(
        str(processed.get("Gender", "male")).strip().lower(), 1
    )
    processed["EducationStage"] = EDU_MAP.get(
        str(processed.get("EducationStage", "teen")).strip().lower(), 1
    )

    # Build dataframe safely
    df = pd.DataFrame([{k: processed.get(k, 0) for k in FEATURE_ORDER}])
    df_scaled = scaler.transform(df)

    prob = model.predict_proba(df_scaled)[0][1]
    label = int(prob >= 0.65)

    return float(prob), label
