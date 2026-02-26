from flask import Flask, render_template, request

app = Flask(__name__)

# Simple keyword-based prediction function
def predict(job_text):
    job_text = job_text.lower()

    scam_keywords = [
        "work from home",
        "earn money fast",
        "no experience required",
        "investment required",
        "registration fee",
        "urgent hiring",
        "click here",
        "limited seats"
    ]

    score = 0

    for word in scam_keywords:
        if word in job_text:
            score += 1

    probability = min(score * 15, 100)

    if probability > 50:
        prediction = "⚠ High Risk – This job may be a scam!"
    else:
        prediction = "✅ Low Risk – This job seems legitimate."

    return prediction, probability


@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    probability = 0

    if request.method == "POST":
        job_text = request.form["job_text"]
        prediction, probability = predict(job_text)

    return render_template(
        "index.html",
        prediction=prediction,
        probability=probability
    )


if __name__ == "__main__":
    if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
