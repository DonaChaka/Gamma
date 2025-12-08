import mss
from PIL import Image
import io

def capture_screenshot():
    with mss.mss() as sct:
        screenshot = sct.grab(sct.monitors[1])
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return buffer.getvalue()
