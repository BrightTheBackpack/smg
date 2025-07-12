from flask import Flask, request, render_template_string
import requests
import json
import pywemo

app = Flask(__name__)

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

            button.onclick = () => {
                button.textContent = "🎤 Listening...";
                recognition.start();
            };

            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                promptInput.value = transcript;
                form.submit();
            };

            recognition.onend = () => {
                button.textContent = "🎤 Start Talking";
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
        try:
            # Send to Hack Club's GPT API
            url = "https://ai.hackclub.com/chat/completions"
            headers = {"Content-Type": "application/json"}
            data = {
                "messages": [{"role": "user", "content": prompt_text}]
            }

            res = requests.post(url=url, headers=headers, json=data)
            res.raise_for_status()
            response_text = res.json().get("choices", [{}])[0].get("message", {}).get("content", "No response")

            # Handle WeMo based on response
            #wemo_result = control_wemo_from_response(response_text)
            #response_text += f"\n\n➡️ {wemo_result}"

        except Exception as e:
            response_text = f"Error: {str(e)}"

    return response_text

@app.route("/server", methods=["GET", "POST"])
def server():
    return "hello"

if __name__ == "__main__":
    app.run(debug=True)
