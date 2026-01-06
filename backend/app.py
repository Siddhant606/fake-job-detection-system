from flask_cors import CORS
from flask import Flask, request, jsonify
import joblib

from backend.utils.preprocess import clean_text

app = Flask(__name__)
CORS(app)

model = joblib.load('backend/model/fake_job_model.pkl')
vectorizer = joblib.load('backend/model/vectorizer.pkl')

SCAM_KEYWORDS = [
    "registration fee",
    "pay fee",
    "whatsapp",
    "telegram",
    "no experience required",
    "instant joining",
    "work from home",
    "limited slots",
    "earn money fast",
    "pay to receive",
    "contact immediately"
]

def contains_scam_keywords(text: str) -> bool:
    text = text.lower()
    for keyword in SCAM_KEYWORDS:
        if keyword in text:
            return True
    return False


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "UP",
        "message": "Fake Job Detection API is running"
    })


@app.route('/predict', methods=['POST'])
def predict():

    # 1. Validate JSON
    if not request.is_json:
        return jsonify({
            "error": "Invalid request format. JSON expected."
        }), 400

    data = request.get_json()

    # 2. Validate key
    if 'job_description' not in data:
        return jsonify({
            "error": "Missing 'job_description' field."
        }), 400

    job_text = data['job_description']

    # 3. Validate type
    if not isinstance(job_text, str):
        return jsonify({
            "error": "'job_description' must be a string."
        }), 400

    # 4. Validate length
    if len(job_text.strip()) < 20:
        return jsonify({
            "error": "Job description is too short to analyze."
        }), 400

    # 5. ML processing
    cleaned_text = clean_text(job_text)
    vectorized_text = vectorizer.transform([cleaned_text])

    prediction = model.predict(vectorized_text)[0]
    probability = model.predict_proba(vectorized_text)[0].max()

    # 6. Rule-based override
    if contains_scam_keywords(job_text):
        result = "FAKE"
        reason = "Rule-based fraud indicators detected"
    else:
        result = "FAKE" if prediction == 1 else "REAL"
        reason = "ML model prediction"

    # 7. Final response
    return jsonify({
        "prediction": result,
        "confidence": round(float(probability), 2),
        "decision_source": reason
    })



if __name__ == '__main__':
    app.run()
