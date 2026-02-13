import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import sys
import os
import numpy as np

# ----------------------------
# 1️⃣ SET RANDOM SEED
# ----------------------------
np.random.seed(42)

# ----------------------------
# 2️⃣ ADD PROJECT ROOT
# ----------------------------
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
sys.path.append(PROJECT_ROOT)

from preprocessing.preprocess import preprocess_dataset

# ----------------------------
# 3️⃣ LOAD & PREPROCESS DATA
# ----------------------------
DATASET_PATH = os.path.join(PROJECT_ROOT, "dataset", "ADHD.csv")
df = preprocess_dataset(DATASET_PATH)

FEATURES = [
    "Age", "Gender", "EducationStage",
    "InattentionScore", "HyperactivityScore", "ImpulsivityScore",
    "SymptomSum", "Daydream", "SleepHours", "ScreenTime", "FamilyHistory"
]

X = df[FEATURES]
y = df["ADHD"]

# ----------------------------
# 4️⃣ TRAIN-TEST SPLIT
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ----------------------------
# 5️⃣ SCALING (IMPORTANT)
# ----------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # 🔧 FIXED

# ----------------------------
# 6️⃣ MODEL TRAINING
# ----------------------------
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train_scaled, y_train)

# ----------------------------
# 7️⃣ SAVE MODEL & SCALER
# ----------------------------
MODEL_DIR = os.path.join(PROJECT_ROOT, "backend", "model")
os.makedirs(MODEL_DIR, exist_ok=True)

joblib.dump(model, os.path.join(MODEL_DIR, "adhd_model.pkl"))
joblib.dump(scaler, os.path.join(MODEL_DIR, "scaler.pkl"))

print("✅ Model trained and saved successfully.")
