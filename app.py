from flask import Flask, request, render_template
import pickle
import os
import nltk

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

# Load model safely
try:
    model = pickle.load(open('model.pkl', 'rb'))
    print("Model loaded successfully")
except Exception as e:
    print("Error loading model:", e)
    model = None


# Home page
@app.route('/')
def home():
    return render_template('index.html')


# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input text
        input_text = request.form.get('job_description')

        if not input_text:
            return "No input provided"

        # Dummy processing (since real preprocessing not added here)
        input_data = [len(input_text)]  # simple feature

        # Prediction
        if model is not None:
            result = model.predict([input_data])[0]
            output = "Fake Job" if result == 1 else "Real Job"
        else:
            output = "Model not loaded"

        return render_template('index.html', prediction_text=output)

    except Exception as e:
        return f"Error occurred: {e}"


# Run app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)