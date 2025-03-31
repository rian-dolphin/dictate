import subprocess
import threading
import time
import os
import platform

class LoadingIndicator:
    def __init__(self):
        self._notification_shown = False
        self._stop_event = threading.Event()
        self._thread = None
        
    def show(self, message="Processing your request..."):
        if self._thread is not None:
            return
            
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._show_notification, args=(message,))
        self._thread.daemon = True
        self._thread.start()
    
    def hide(self):
        if self._thread is not None:
            self._stop_event.set()
            self._thread.join()
            self._thread = None
            
    def _show_notification(self, message):
        try:
            system = platform.system()
            
            if system == "Linux":
                # Show notification on Linux
                subprocess.run([
                    "notify-send", 
                    "--icon=info", 
                    "VibeVoice", 
                    message,
                    "--expire-time=10000"  # 10 seconds
                ])
            elif system == "Darwin":  # macOS
                # Show notification on macOS
                subprocess.run([
                    "osascript", 
                    "-e", 
                    f'display notification "{message}" with title "VibeVoice"'
                ])
            elif system == "Windows":
                # Show notification on Windows (requires win10toast or similar)
                try:
                    from win10toast import ToastNotifier
                    toaster = ToastNotifier()
                    toaster.show_toast("VibeVoice", 
                                      message, 
                                      duration=10,
                                      threaded=True)
                except ImportError:
                    # Fallback to print if win10toast not installed
                    print("Processing request (install win10toast for notifications)...")
            
            # Wait until stop event or timeout
            self._stop_event.wait(10)  # Wait up to 10 seconds
            
        except Exception as e:
            print(f"Error showing notification: {e}") 