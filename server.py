from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Load API key from Railway environment variables
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Mistral API Request
    mistral_url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
    payload = {
        "model": "mistral-medium",  # Use "mistral-large" for a better response
        "messages": [{"role": "user", "content": user_message}],
    }

    response = requests.post(mistral_url, json=payload, headers=headers)
    
    if response.status_code != 200:
        return jsonify({"error": "Failed to get response from Mistral"}), 500
    
    mistral_response = response.json()
    bot_reply = mistral_response["choices"][0]["message"]["content"]
    
    return jsonify({"reply": bot_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
