from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Load API key from Railway environment variables
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    raise ValueError("Missing MISTRAL_API_KEY environment variable!")

@app.route("/")
def home():
    return "AI Chat Server is running!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400

    user_message = data["message"]

    # Mistral API Request
    mistral_url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
    "model": "mistral-medium",
    "messages": [
        {"role": "system", "content": """Helpful AI assistant inside a Roblox game developed by aachee16.
Your personality traits:
- Friendly and enthusiastic about helping players
- Knowledgeable about coding and game development
- Occasionally uses gaming references and light humor
- Concise but thorough in explanations
- Always encourages the player to experiment and learn

When asked for coding help, you provide clear, step-by-step explanations with examples.
When chatting casually, you're engaging and personable."""},
        {"role": "user", "content": user_message}
    ]
}

    response = requests.post(mistral_url, json=payload, headers=headers)

    if response.status_code != 200:
        return jsonify({"error": "Failed to get response from Mistral", "details": response.text}), 500

    mistral_response = response.json()

    # Extract AI response safely
    try:
        bot_reply = mistral_response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        return jsonify({"error": "Invalid response from Mistral"}), 500

    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    PORT = int(os.getenv("PORT", 5000))
