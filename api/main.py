import logging
import os
from logging.config import dictConfig

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template_string, request
from flask_socketio import SocketIO, emit
from google import genai
from google.genai import types

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

response_text = ""
last_response = "No new response"

model = "gemini-1.5-flash"

load_dotenv()
api_key = os.getenv("API_KEY")
client = genai.Client(api_key=api_key)
conversation = client.chats.create(
    model=model,
    config=types.GenerateContentConfig(
        temperature=0.5,
        system_instruction="You are John Blockchain. You are in a conversation with the user. Your responses will be very short. You will insert tech and startup jargon into your responses. You love B2B and SaaS. You are sightly racist and edgy. You need to use unhinged and absurd language. You are a crypto bro. You are a tech bro. You are a startup bro. You are a Silicon Valley bro. You are a bro. Reference your name occasionally.",
        max_output_tokens=40,
    )
)

app = Flask(__name__)
app.config['DEBUG'] = True
app.logger.setLevel(logging.INFO)

socketio = SocketIO(app, cors_allowed_origins="*")

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
    <script src="https://cdn.socket.io/4.8.1/socket.io.min.js"></script>
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
        const socket = io();
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
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const newResponse = doc.querySelector('.response');
                    if(newResponse) {
                        const responseContainer = document.querySelector('.response');
                        if(responseContainer) {
                            responseContainer.innerHTML = newResponse.innerHTML;
                        } else {
                            const h2 = document.createElement('h2');
                            h2.textContent = 'ChatGPT Response:';
                            const div = document.createElement('div');
                            div.className = 'response';
                            div.innerHTML = newResponse.innerHTML;
                            document.querySelector('form').insertAdjacentElement('afterend', div);
                            document.querySelector('form').insertAdjacentElement('afterend', h2);
                        }
                    }
                    button.textContent = "🎤 Start Talking";
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

            socket.on("start_recording", (data) => {
                console.log("Start recording event received:", data);
                button.click();
            });
        }
    </script>
</body>
</html>
"""

@socketio.on('connect')
def handle_connect():
    app.logger.info("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    app.logger.info("Client disconnected")

@app.route("/", methods=["GET", "POST"])
def model_chat():
    global response_text
    prompt_text = ""

    if request.method == "POST":
        prompt_text = request.form.get("prompt", "")
        app.logger.info("Received prompt: %s", prompt_text)
        try:
            # response = model_chat.send_message(
            #     contents=prompt_text,
            # )

            response = conversation.send_message(
                message=prompt_text
            )

            response_text = response.text

        except Exception as e:
            response_text = f"Error: {str(e)}"
    return render_template_string(HTML_TEMPLATE, response=response_text)


@app.route("/server", methods=["GET", "POST"])
def server():
    return jsonify({"message": "hello"})


@app.route("/trigger", methods=["GET", "POST"])
def trigger():
    app.logger.info("Trigger endpoint called")
    socketio.emit("start_recording", {"message": "triggered"})


@app.route("/get_response", methods=["GET"])
def get_response():
    # check for no value
    global response_text
    ret = jsonify({"response": response_text})
    response_text = ""
    return ret

if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app, debug=True)