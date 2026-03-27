from flask import Flask, render_template, request

app = Flask(__name__)

def detect_scam(text):
    text = text.lower()

    scam_keywords = [
        "pay registration fee",
        "earn money fast",
        "work from home",
        "no interview",
        "whatsapp only",
        "send money",
        "urgent hiring",
        "limited seats",
        "easy money",
        "investment required"
    ]

    score = sum(1 for word in scam_keywords if word in text)
    probability = min(score * 15, 100)

    if probability > 60:
        result = "❌ High Risk – Likely Scam!"
    elif probability > 30:
        result = "⚠️ Medium Risk – Be Careful!"
    else:
        result = "✅ Low Risk – Seems Legitimate"

    return result, probability


@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    probability = 0

    if request.method == "POST":
        job_text = request.form["job_text"]
        prediction, probability = detect_scam(job_text)

    return render_template("index.html",
                           prediction=prediction,
                           probability=probability)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)