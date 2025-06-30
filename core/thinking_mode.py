# thinking_mode.py
import time
import json
import os

LOG_FILE = "logsos.path.join(os.sep, 'neuroflex.log')"
os.makedirs("logs", exist_ok=True)

def detect_mode(self, answer_text, start_time, end_time, content_type="text"):
    elapsed = end_time - start_time
    word_count = len(answer_text.strip().split())
    mode = "flex"
    confidence = 0.5
    reason = []

    if word_count < 10 and elapsed < 15:
        mode = "analytical"
        confidence = 0.75
        reason.append("short and fast")
    elif word_count > 40 and elapsed > 45:
        mode = "creative"
        confidence = 0.8
        reason.append("long and slow")
    elif "video" in content_type:
        mode = "creative"
        confidence = 0.7
        reason.append("video-based")
    else:
        reason.append("ambiguous pattern")

    log_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "mode": mode,
        "confidence": round(confidence, 2),
        "word_count": word_count,
        "elapsed_sec": round(elapsed, 1),
        "content_type": content_type,
        "reason": reason
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    return mode, confidence
