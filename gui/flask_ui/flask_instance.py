from flask import Flask, render_template, request, jsonify, Response
import json
import threading
from ollama.run_ollama import OllamaClient
from store.db import init_db, add_message, get_history, clear_history

app = Flask(__name__)

'''
VLM Configuration example:
{
    "model_name": "qwen3-vl:2b-instruct",
    "url": "http://localhost:11434/api/generate",
    "system_prompt": "You are Gamma, a physics tutor. Always explain equations first, then text. Provide one concise explanation and then stop.",
    "options": {
            "temperature": 0.7,
            "top_p": 0.9
    },
    "len_history": 0
}
len_history => How many previous exchanges to keep in context. 0 means no history.
top_p => Nucleus sampling parameter. Indicates the cumulative probability threshold for token selection.
temperature => Controls randomness in output

'''
config_path = r"C:\Users\Work.LAPTOP-JOMS87TS\Documents\Projects\Gamma\config\vlm_config.json"
vlm_client = OllamaClient(config_path=config_path)
vlm_client.start()

# Initialize database on startup
init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data.get("message", "")
    include_image = data.get("include_image", True) 

    # Save user message immediately
    add_message("user", prompt)

    def generate():
        response_chunks = []
        for chunk in vlm_client.ask(prompt, include_image=include_image):
            response_chunks.append(chunk)
            # Stream each chunk to client as SSE
            yield f"data: {json.dumps({'response': chunk})}\n\n"

        # After streaming completes, save final response
        final_response = "".join(response_chunks)
        add_message("ai", final_response)

    return Response(generate(), mimetype="text/event-stream")

@app.route("/history")
def history():
    chat_history = get_history()
    return jsonify(chat_history)

@app.route("/clear_history", methods=["POST"])
def clear_history_route():
    clear_history()
    return jsonify({"status": "success"})

@app.route("/settings")
def settings():
    return render_template("settings.html", current_model=vlm_client.get_model())

@app.route("/set_model", methods=["POST"])
def set_model_route():
    data = request.get_json()
    model = data.get("model")
    if model:
        vlm_client.set_model(model)
        return jsonify({"status": "success", "model": model})
    return jsonify({"status": "error", "message": "No model provided"}), 400


if __name__ == "__main__":
    app.run(debug=True)