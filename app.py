from flask import Flask, render_template, request, jsonify
import requests
import json
import os

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_trip_with_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are an expert AI travel planner who creates detailed, creative, and budget-friendly itineraries."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    return response_data["choices"][0]["message"]["content"] 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_itinerary', methods=['POST'])
def generate_itinerary():
    data=request.json
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
        ai_plan = generate_trip_with_groq(prompt)
        return jsonify({"plan": ai_plan})

    except Exception as e:
        print(f"⚠️ Error while generating trip plan: {e}")
        return jsonify({
            "plan": "Sorry, something went wrong while creating your trip plan. "
                    "Please check your inputs and try again later."
        })
        

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
