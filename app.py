from flask import Flask, request, render_template, session, url_for, redirect

import joblib
import random
import json

# Load model and vectorizer
model = joblib.load("model/emotion_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")

# Load responses
with open("emotion_responses.json", "r", encoding="utf-8") as f:
    emotion_responses = json.load(f)

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Needed to use session

def get_response(user_input):
    x = vectorizer.transform([user_input])
    predicted_emotion = model.predict(x)[0]
    responses = emotion_responses.get(predicted_emotion, emotion_responses["default"])
    response = random.choice(responses)

    # Map emotions to emojis
    emoji_map = {
        "sadness": "😢",
        "joy": "😊",
        "anger": "😠",
        "fear": "😨",
        "love": "❤️",
        "surprise": "😲",
        "default": "💬"
    }

    emoji = emoji_map.get(predicted_emotion, emoji_map["default"])
    return f"{response} {emoji}"


@app.route("/", methods=["GET", "POST"])
def index():
    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST":
        user_message = request.form["message"]
        bot_response = get_response(user_message)

        # Save to chat history
        session["chat_history"].append({"user": user_message, "bot": bot_response})
        session.modified = True

    return render_template("index.html", chat_history=session["chat_history"])
@app.route("/clear", methods=["POST"])
def clear():
    session.pop("chat_history", None)  # Clear session
    return redirect(url_for("index"))  # Redirect to main page

if __name__ == "__main__":
    app.run(debug=True)
