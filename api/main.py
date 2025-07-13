from flask import Flask, request, jsonify, render_template_string
import requests
import json
import pywemo
from google import genai
from dotenv import load_dotenv
import os
import logging
from logging.config import dictConfig
import sys
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


load_dotenv()
api_key = os.getenv("API_KEY")
client = genai.Client(api_key=api_key)

app = Flask(__name__)
app.config['DEBUG'] = True
app.logger.setLevel(logging.INFO)

# Discover WeMo devices
devices = pywemo.discover_devices()
wemo_switch = next((d for d in devices if d.device_type == "Switch"), None)


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SMG Web Server</title>
    <style>
        body { font-family: sans-serif; margin: 40px; }
        #mic-button { padding: 10px 20px; font-size: 16px; }
        .response { white-space: pre-wrap; background: #f0f0f0; padding: 1em; border-radius: 8px; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>🎤 Voice-Controlled WeMo with GPT</h1>
    <form method="POST" id="voice-form">
        <input type="hidden" name="prompt" id="prompt">
        <button type="button" id="mic-button">🎤 Start Talking</button>
    </form>

    {% if response %}
        <h2>ChatGPT Response:</h2>
        <div class="response">{{ response }}</div>
    {% endif %}

    <script>
        const button = document.getElementById("mic-button");
        const promptInput = document.getElementById("prompt");
        const form = document.getElementById("voice-form");

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            alert("Speech recognition not supported in this browser.");
        } else {
            const recognition = new SpeechRecognition();
            recognition.lang = 'en-US';
            recognition.interimResults = false;
            recognition.continuous = false;

            button.onclick = () => {
                button.textContent = "🎤 Listening...";
                recognition.start();
            };

            recognition.onresult = (event) => {
                console.log("ONRESULT", event);
                button.textContent = "🎤 Processing...";
                const transcript = event.results[0][0].transcript;
                promptInput.value = transcript;
                console.log("ONRESULT");

                fetch('/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `prompt=${encodeURIComponent(transcript)}`
                })
                .then(response => response.text())
                .then(html => {
                    document.documentElement.innerHTML = html;
                })
                .catch(error => {
                    console.error('Error:', error);
                    button.textContent = "Error!";
                });
            };

            recognition.onend = () => {
                button.textContent = "🎤 Start Talking";
                button.textContent = "please work";
                console.log("ONEND");
            };
        }
    </script>
</body>
</html>
"""

def control_wemo_from_response(text):
    """Check text for control commands and toggle WeMo switch accordingly."""
    if not wemo_switch:
        return "No WeMo switch found."

    lowered = text.lower()
    if "turn on" in lowered or "switch on" in lowered:
        wemo_switch.on()
        return "WeMo turned ON."
    elif "turn off" in lowered or "switch off" in lowered:
        wemo_switch.off()
        return "WeMo turned OFF."
    return "No WeMo command detected."

@app.route("/", methods=["GET", "POST"])
def chat():
    prompt_text = ""
    response_text = ""

    if request.method == "POST":
        prompt_text = request.form.get("prompt", "")
        app.logger.info("Received prompt: %s", prompt_text)
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt_text,
            )

            response_text = response.text

            # Handle WeMo based on response
            #wemo_result = control_wemo_from_response(response_text)
            #response_text += f"\n\n➡️ {wemo_result}"

        except Exception as e:
            response_text = f"Error: {str(e)}"

    # return response_text
    return render_template_string(HTML_TEMPLATE, response=response_text)

@app.route("/server", methods=["GET", "POST"])
def server():
    return jsonify({"message": "hello"})

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/version")
def version():
    return f"Python {sys.version}"
