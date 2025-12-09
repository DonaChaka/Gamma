import psutil
import subprocess
import requests
import base64
import json
from utils.capture_screenshot import capture_screenshot

class OllamaClient:
    def __init__(self,
                 config_path=None):
        """
        Initialize OllamaClient. If config_path is provided, load parameters from JSON config file.
        """
        self.load_config(config_path)

    def load_config(self, path):
        """Load parameters from a JSON config file."""
        with open(path, "r", encoding="utf-8") as f:
            cfg = json.load(f)

        self.model_name = cfg.get("model_name")
        self.url = cfg.get("url")
        self.system_prompt = cfg.get("system_prompt", None)
        self.len_history = cfg.get("len_history", None)
        self.options = cfg.get("options", {})

    def set_model(self, model_name):
        """Change the active model."""
        self.model_name = model_name
        print(f"Model switched to: {self.model_name}")

    def get_model(self):
        return self.model_name

    def start(self):
        """Start Ollama if it's not already running."""
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            if 'ollama' in proc.info['name'].lower():
                print("Ollama is already running.")
                return True

        print(f"Starting Ollama with model {self.model_name}...")
        subprocess.Popen(
            [r"C:\Users\Work.LAPTOP-JOMS87TS\AppData\Local\Programs\Ollama\ollama.exe", "run", self.model_name],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return True

    def ask(self, prompt, include_image=True):
        """Send prompt (+ optional screenshot) to Ollama and yield streamed response chunks."""
        image_data = capture_screenshot() if include_image else None
        image_base64 = base64.b64encode(image_data).decode("utf-8") if image_data else None

        if self.len_history and self.len_history > 0:
            from store.db import get_history
            history = get_history(limit=self.len_history)
            if history:
                conversation = ""
                for msg in history:
                    role = msg["role"]
                    text = msg["text"]
                    if role == "user":
                        conversation += f"User: {text}\n"
                    else:
                        conversation += f"AI: {text}\n"
                
                prompt = conversation + f"User: {prompt}\nAI:"


        payload = {
            "model": self.model_name,
            "prompt": prompt,
        }
        if self.system_prompt:
            payload["system"] = self.system_prompt
        if self.options:
            payload["options"] = self.options
        if image_base64:
            payload["images"] = [image_base64]

        response = requests.post(self.url, json=payload, stream=True)
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line.decode("utf-8"))
                    if chunk.get("response"):
                        yield chunk["response"]
                except Exception:
                    continue