import ctypes
from ctypes import wintypes
import threading
import webview
from gui.flask_ui.flask_instance import app

def run_flask():
    app.run(host="127.0.0.1", port=5000, debug=False)

def start_gui():
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    # Work area (excludes taskbar)
    rect = wintypes.RECT()
    SPI_GETWORKAREA = 0x0030
    user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0)

    # Work width and height with (10, 20) padding
    work_width = 10 + rect.right - rect.left
    work_height = 20 + rect.bottom - rect.top

    window_width = 470
    window_height = work_height
    x = work_width - window_width
    y = rect.top

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