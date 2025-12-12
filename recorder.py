import time
import pyautogui
import pygetwindow as gw
from PIL import Image, ImageChops
import threading
import datetime
import os

class Recorder:
    def __init__(self):
        self.is_recording = False
        self.last_screenshot = None
        self.last_capture_time = 0
        self.captured_data = []
        self.lock = threading.Lock()
        self.min_interval = 10  # seconds

    def start(self):
        self.is_recording = True
        self.captured_data = []
        self.last_screenshot = None
        self.last_capture_time = 0
        threading.Thread(target=self._record_loop, daemon=True).start()

    def stop(self):
        self.is_recording = False

    def _record_loop(self):
        while self.is_recording:
            current_time = time.time()
            
            # Capture current screen
            try:
                screenshot = pyautogui.screenshot()
            except Exception as e:
                print(f"Error capturing screenshot: {e}")
                time.sleep(1)
                continue

            # Get active window title
            try:
                active_window = gw.getActiveWindow()
                window_title = active_window.title if active_window else "Unknown Window"
            except Exception:
                window_title = "Unknown Window"

            should_capture = False
            change_description = ""

            if self.last_screenshot is None:
                should_capture = True
                change_description = "Initial capture"
            elif (current_time - self.last_capture_time) >= self.min_interval:
                # Check for visual changes
                diff = ImageChops.difference(self.last_screenshot, screenshot)
                if diff.getbbox():
                    should_capture = True
                    change_description = f"Screen content changed. Active window: {window_title}"

            if should_capture:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Save screenshot to a temporary file or keep in memory
                # For simplicity and memory management, let's save to a temp folder
                if not os.path.exists("temp_captures"):
                    os.makedirs("temp_captures")
                
                filename = f"temp_captures/capture_{int(current_time)}.png"
                screenshot.save(filename)

                with self.lock:
                    self.captured_data.append({
                        "timestamp": timestamp,
                        "image_path": filename,
                        "description": change_description,
                        "window_title": window_title
                    })
                
                self.last_screenshot = screenshot
                self.last_capture_time = current_time
            
            time.sleep(1) # Check every second, but only capture if interval met

    def get_data(self):
        with self.lock:
            return list(self.captured_data)

    def clear_temp_files(self):
        if os.path.exists("temp_captures"):
            for f in os.listdir("temp_captures"):
                try:
                    os.remove(os.path.join("temp_captures", f))
                except Exception:
                    pass
