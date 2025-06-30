# adaptive_logger.py
import os, json, time

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "adaptive_mode_history.jsonl")
os.makedirs(LOG_DIR, exist_ok=True)

def log_mode_event(self, lesson_name, mode, confidence, reason=None):
    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "lesson": lesson_name,
        "mode": mode,
        "confidence": round(confidence, 2),
        "reason": reason or [],
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


# style_switcher.py
from PyQt5.QtGui import QFont

def apply_style_mode(self, gui, mode):
    if mode == "analytical":
        gui.sidebar.setMaximumWidth(220)
        gui.content_area.setStyleSheet("font-size: 12px; font-family: Segoe UI; background-color: #1e1e1e;")
        gui.xp_bar.setStyleSheet("color: #66ff99; font-size: 12px; font-family: monospace;")
        gui.streak_label.setText("\U0001F9E0 Analytical Mode")
    elif mode == "creative":
        gui.sidebar.setMaximumWidth(300)
        gui.content_area.setStyleSheet("font-size: 14px; font-family: Comic Sans MS; background-color: #1a1a1a;")
        gui.xp_bar.setStyleSheet("color: #ffcc66; font-size: 14px; font-family: Georgia;")
        gui.streak_label.setText("\U0001F3A8 Creative Mode")
    else:
        gui.sidebar.setMaximumWidth(250)
        gui.content_area.setStyleSheet("font-size: 13px; font-family: Consolas; background-color: #202020;")
        gui.xp_bar.setStyleSheet("color: #aaaaff; font-size: 13px;")
        gui.streak_label.setText("\U0001F300 Flex Mode")

    gui.sidebar.repaint()
    gui.content_area.repaint()
    gui.xp_bar.repaint()
    gui.streak_label.repaint()

