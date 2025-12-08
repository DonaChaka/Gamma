import psutil
import subprocess
import requests
import base64
import json
from utils.capture_screenshot import capture_screenshot

class OllamaClient:
    def __init__(self, model_name="llava:7b", url="http://localhost:11434/api/generate"):
        self.model_name = model_name
        self.url = url

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

    def ask(self, prompt, update_callback):
        """Send prompt + screenshot to Ollama and stream response."""
        image_data = capture_screenshot()
        image_base64 = base64.b64encode(image_data).decode("utf-8")

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "images": [image_base64]
        }

        response = requests.post(self.url, json=payload, stream=True)
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line.decode("utf-8"))
                    update_callback(chunk.get("response", ""))
                except Exception:
                    pass