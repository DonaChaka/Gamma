from flask import Flask, render_template, request, jsonify, Response
import json
import threading
from ollama.run_ollama import OllamaClient
from store.db import init_db, add_message, get_history, clear_history

app = Flask(__name__)
ollama_client = OllamaClient(model_name="qwen3-vl:2b-instruct")
ollama_client.start()

# Initialize database on startup
init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data.get("message", "")

    # Save user message immediately
    add_message("user", prompt)

    def generate():
        response_chunks = []
        for chunk in ollama_client.ask(prompt):
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
    return render_template("settings.html", current_model=ollama_client.get_model())

@app.route("/set_model", methods=["POST"])
def set_model_route():
    data = request.get_json()
    model = data.get("model")
    if model:
        ollama_client.set_model(model)
        return jsonify({"status": "success", "model": model})
    return jsonify({"status": "error", "message": "No model provided"}), 400


if __name__ == "__main__":
    app.run(debug=True)