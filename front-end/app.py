from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd

app = Flask(__name__)
CORS(app)

# Attempt to load the trained model from a pickle file.
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    print("Model loaded successfully.")
except Exception as e:
    print("Error loading model:", e)
    model = None

FEATURES = [
    "Average_Dwell_Time", 
    "Average_Flight_Time", 
    "Flight_Time_Std_Dev", 
    "Human_Like_Typing_Score", 
    "Words_Per_Minute"
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        # Convert each expected feature to float.
        sample = {feature: float(data[feature]) for feature in FEATURES}
    except KeyError as e:
        return jsonify({"error": f"Missing feature: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Error converting features: {str(e)}"}), 400

    try:
        # Create a DataFrame in the expected column order.
        if hasattr(model, "feature_names_in_"):
            sample_df = pd.DataFrame([sample], columns=model.feature_names_in_)
        else:
            sample_df = pd.DataFrame([sample], columns=FEATURES)
    except Exception as e:
        return jsonify({"error": f"Error creating DataFrame: {str(e)}"}), 500

    try:
        # Get prediction probabilities from the model.
        probabilities = model.predict_proba(sample_df)[0]
    except Exception as e:
        return jsonify({"error": f"Error during model prediction: {str(e)}"}), 500

    # Assuming model.classes_ = [0, 1] where 0 = Bot and 1 = Human.
    bot_probability = probabilities[0]
    human_probability = probabilities[1]
    prediction = "Human" if human_probability > bot_probability else "Bot"

    # Print received metrics and prediction to the terminal.
    print("Received metrics:", sample)
    print(f"Prediction: {prediction} | Human Probability: {human_probability:.2f} | Bot Probability: {bot_probability:.2f}")

    return jsonify({
        "prediction": prediction,
        "human_probability": human_probability,
        "bot_probability": bot_probability
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
