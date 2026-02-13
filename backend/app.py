from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys

# ----------------------------
# ADD PROJECT ROOT
# ----------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from scoring.inattention import calculate_inattention
from scoring.impulsivity import calculate_impulsivity
from scoring.hyperactivity import calculate_hyperactivity
from backend.prediction.predict import predict_adhd

# ----------------------------
# FLASK CONFIG
# ----------------------------
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")

app = Flask(
    __name__,
    static_folder=STATIC_DIR,
    template_folder=FRONTEND_DIR
)

CORS(app)

# ----------------------------
# AUTO OPEN BROWSER
# ----------------------------


# ----------------------------
# FRONTEND ROUTES
# ----------------------------
@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:filename>")
def serve_pages(filename):
    return send_from_directory(FRONTEND_DIR, filename)

# ----------------------------
# API ROUTE
# ----------------------------
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)

    user = data.get("user", {})
    pilot = data.get("adaptive_pilot", {})
    reaction = data.get("flash_reaction", {})
    shield = data.get("steady_shield", {})

    inattention = calculate_inattention(pilot)
    impulsivity = calculate_impulsivity(reaction)
    hyperactivity = calculate_hyperactivity(shield)
    symptom_sum = inattention + impulsivity + hyperactivity

    features = {
        "Age": user.get("Age", 0),
        "Gender": user.get("Gender", "Male"),
        "EducationStage": user.get("EducationStage", "Teen"),
        "InattentionScore": inattention,
        "HyperactivityScore": hyperactivity,
        "ImpulsivityScore": impulsivity,
        "SymptomSum": symptom_sum,
        "Daydream": user.get("Daydream", 0),
        "SleepHours": user.get("SleepHours", 0),
        "ScreenTime": user.get("ScreenTime", 0),
        "FamilyHistory": user.get("FamilyHistory", 0)
    }

    prob, label = predict_adhd(features)
    return jsonify({
        "probability": round(prob * 100, 1),
        "label": int(label),

        "scores": {
            "inattention": inattention,
            "hyperactivity": hyperactivity,
            "impulsivity": impulsivity
        },

        "symptom_sum": symptom_sum,

        "result_text": (
            "ADHD Likely (High correlation with behavioral patterns)"
            if label == 1
            else "No ADHD Likely"
        ),

        "disclaimer": (
            "⚠️ This is an AI-based screening tool and NOT a clinical diagnosis. "
            "Please consult a qualified medical professional for an official assessment."
        )
    })


# ----------------------------
# RUN APP
# ----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

