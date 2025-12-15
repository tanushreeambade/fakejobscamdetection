from flask import Flask, render_template, request

app = Flask(__name__)

SCAM_KEYWORDS = [
    "registration fee", "pay", "urgent", "no interview",
    "whatsapp", "telegram", "limited seats",
    "work from home", "quick money"
]

FREE_EMAILS = ["gmail.com", "yahoo.com", "outlook.com"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check():
    title = request.form['title'].lower()
    company = request.form['company'].lower()
    description = request.form['description'].lower()
    email = request.form['email'].lower()
    salary = request.form['salary']

    score = 0
    reasons = []

    # 1️⃣ Keyword analysis
    for word in SCAM_KEYWORDS:
        if word in description:
            score += 15
            reasons.append(f"Suspicious phrase detected: '{word}'")

    # 2️⃣ Email authenticity
    domain = email.split("@")[-1]
    if domain in FREE_EMAILS:
        score += 25
        reasons.append("Free email provider used instead of official company email")

    # 3️⃣ Unrealistic salary
    try:
        sal = int(salary)
        if sal > 80000:
            score += 20
            reasons.append("Unrealistically high salary for entry-level job")
    except:
        pass

    # 4️⃣ Short / vague description
    if len(description.split()) < 30:
        score += 15
        reasons.append("Very short or vague job description")

    # 5️⃣ No company mention in email
    if company not in email:
        score += 10
        reasons.append("Email does not match company name")

    score = min(score, 100)

    return render_template(
        "result.html",
        score=score,
        reasons=reasons
    )

if __name__ == "__main__":
    app.run(debug=True)
