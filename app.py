from flask import Flask, request, render_template
import pickle
import os

app = Flask(__name__)

# Load model safely
try:
    model = pickle.load(open('model.pkl', 'rb'))
    print("Model loaded successfully")
except Exception as e:
    print("Error loading model:", e)
    model = None


# Home route
@app.route('/')
def home():
    return '''
    <h2>Fake Job Scam Detection</h2>
    <form action="/predict" method="post">
        <textarea name="job_description" placeholder="Enter job description" rows="5" cols="40"></textarea><br><br>
        <button type="submit">Analyze Job</button>
    </form>
    '''


# Prediction route (FIXED)
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            input_text = request.form.get('job_description')

            if not input_text:
                return "Please enter job description"

            # Simple feature (length-based dummy input)
            input_data = [[len(input_text)]]

            if model is not None:
                result = model.predict(input_data)[0]
                output = "🚨 Fake Job" if result == 1 else "✅ Real Job"
            else:
                output = "Model not loaded"

            return f"<h3>Result: {output}</h3><br><a href='/'>Go Back</a>"

        except Exception as e:
            return f"Error: {e}"

    return "Use form to submit data"


# Run app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)