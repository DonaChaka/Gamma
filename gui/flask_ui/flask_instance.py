from flask import Flask, render_template, request, jsonify
import threading
from ollama.run_ollama import OllamaClient
from store.db import init_db, add_message, get_history, clear_history

app = Flask(__name__)
ollama_client = OllamaClient()
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

    '''Contextual chat history (currently disabled). 
    LLava:7b couldn't respond for current screen correctly. 
    But the code is here if needed in the future. Try for other models.
    
    history = get_history(limit=20)  # get last 20 messages
    context = "\n".join([f"{m['role']}: {m['text']}" for m in history])
    full_prompt = f"{context}\nuser: {prompt}\nassistant:"

    Pass full_prompt to thread (ollama) instead of prompt.
    '''

    response_chunks = []
    def update_callback(chunk):
        response_chunks.append(chunk)

    # Run ask_model in a separate thread so Flask doesn’t block
    thread = threading.Thread(target=ollama_client.ask, args=(prompt, update_callback))
    thread.start()
    thread.join()  # wait until streaming finishes

    # Combine chunks into one string
    final_response = "".join(response_chunks)

    add_message("user", prompt)
    add_message("ai", final_response)

    return jsonify({"reply": final_response})

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