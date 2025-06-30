# voice_engine.py
import threading
import time
import queue
import traceback
import pyaudio

class VoiceEngine:
    def __init__(self, wake_word="Hey Celeste", device_index=0):
        self.is_muted = False
        self.running = False
        self.voice_queue = queue.Queue()
        self.device_index = device_index
        self.wake_word = wake_word
        self.listener_thread = None
        self.error_log = "voice_errors.log"

    def toggle_mute(self):
        self.is_muted = not self.is_muted
        self.log(f"[Voice] Mute toggled: {self.is_muted}")

    def start(self):
        if self.listener_thread and self.listener_thread.is_alive():
            self.log("[Voice] Already running.")
            return
        self.running = True
        self.listener_thread = threading.Thread(target=self.listen_loop, daemon=True)
        self.listener_thread.start()
        self.log("[Voice] Listening thread started.")

    def stop(self):
        self.running = False
        if self.listener_thread:
            self.listener_thread.join(timeout=1)
        self.log("[Voice] Listening thread stopped.")

    def listen_loop(self):
        try:
            while self.running:
                if self.is_muted:
                    time.sleep(0.2)
                    continue

                # Simulate input for wake word detection (replace with real VAD/whisper later)
                self.log("[Voice] Listening... (simulated wake word check)")
                time.sleep(5)
                self.voice_queue.put("Hey Celeste")
        except Exception as e:
            self.log_error(f"[VoiceLoop Error] {e}")
            self.log_error(traceback.format_exc())

    def run(self):
        try:
            if not self.voice_queue.empty():
                phrase = self.voice_queue.get()
                if self.wake_word.lower() in phrase.lower():
                    self.log(f"[Voice] Wake word detected: {phrase}")
                    # Trigger agent or GUI reaction here
        except Exception as e:
            self.log_error(f"[VoiceRun Error] {e}")
            self.log_error(traceback.format_exc())

    def log(self, message):
        print(message)
        with open("voice.log", "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {message}\n")

    def log_error(self, message):
        print(f"[ERROR] {message}")
        with open(self.error_log, "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} ERROR: {message}\n")
