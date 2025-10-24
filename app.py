from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# URL of the locally running Ollama model
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"  # You can rename if you use llama3:8b or another variant

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_itinerary', methods=['POST'])
def generate_itinerary():
    try:
        # Collect user inputs from form
        destination = request.form.get('destination')
        budget = request.form.get('budget')
        vibe = request.form.get('vibe')
        preferences = request.form.get('preferences')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        # Construct the AI prompt
        prompt = f"""
        You are an expert travel planner.
        Create a detailed day-by-day itinerary for a trip based on the following details:

        Destination: {destination}
        Total Budget: ₹{budget}
        Travel Dates: {start_date} to {end_date}
        Vibe / Theme: {vibe}
        Preferences: {preferences}

        Include the following in your response:
        - Day-wise plan with short descriptions
        - Estimated flight or travel cost
        - Accommodation suggestions (hotel type and approx. price range)
        - Local attractions and experiences
        - Sustainable or local tips
        - Total estimated cost summary
        - Additional travel tips or safety advice

        Keep it conversational and well-formatted using headings.
        """

        # Send to Llama 3 via Ollama API
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.8
        }

        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()

        # Parse the response text
        result = response.json()
        itinerary_text = result.get("response", "No response received from model.")

        return jsonify({"success": True, "itinerary": itinerary_text})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(port=80)
