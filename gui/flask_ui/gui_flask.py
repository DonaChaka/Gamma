import ctypes
import threading
import webview
from gui.flask_ui.flask_instance import app

def run_flask():
    app.run(host="127.0.0.1", port=5000, debug=False)

def start_gui():
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    window_width = 470
    window_height = screen_height
    x = screen_width - window_width
    y = 0

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Create window
    webview.create_window(
        "Gamma",
        "http://127.0.0.1:5000",
        width=window_width,
        height=window_height,
        x=x,
        y=y,
        resizable=True
    )

    webview.start()