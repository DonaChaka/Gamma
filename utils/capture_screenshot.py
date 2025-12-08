import mss
from PIL import Image, ImageDraw
import io
import ctypes
from ctypes import wintypes

# Capture full screen and mask out your app window
def capture_screenshot(app_title="Gamma"):
    # Find your app window by title
    user32 = ctypes.windll.user32
    hwnd = user32.FindWindowW(None, app_title)

    # Get window rect if found
    rect = wintypes.RECT()
    if hwnd:
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
        app_rect = (rect.left, rect.top, rect.right, rect.bottom)
    else:
        app_rect = None

    # Capture full screen
    with mss.mss() as sct:
        screenshot = sct.grab(sct.monitors[1])
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

    # Mask out your app window
    if app_rect:
        draw = ImageDraw.Draw(img)
        draw.rectangle(app_rect, fill=(0, 0, 0))  # black out your app

    # Return bytes
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()


# Capture full screen without masking app window
def capture_screenshot_no_mask():
    with mss.mss() as sct:
        screenshot = sct.grab(sct.monitors[1])
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return buffer.getvalue()
