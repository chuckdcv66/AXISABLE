# /core/score_tracker.py
import os
import json
from datetime import datetime

PROFILE_FILE = "active_user.json"

def get_active_user(self, ):
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, 'r') as f:
            data = json.load(f)
            return data.get("user", "Riley")
    return "Riley"

def get_score_file(self, ):
    user = get_active_user()
    dir_path = os.path.join("data", user)
    os.makedirs(dir_path, exist_ok=True)
    return os.path.join(dir_path, "scores.json")

def save_score(self, lesson_name, score, quiz_answer=None, mode=None, confidence=None):
    score_file = get_score_file()
    scores = []
    if os.path.exists(score_file):
        with open(score_file, 'r') as f:
            try:
                scores = json.load(f)
            except:
                scores = []

    entry = {
        "lesson": lesson_name,
        "score": score,
        "answer": quiz_answer,
        "timestamp": datetime.now().isoformat()
    }

    if mode:
        entry["mode"] = mode
    if confidence is not None:
        entry["confidence"] = round(confidence, 2)

    scores.append(entry)

    with open(score_file, 'w') as f:
        json.dump(scores, f, indent=2)

def get_scores(self, ):
    score_file = get_score_file()
    if os.path.exists(score_file):
        with open(score_file, 'r') as f:
            return json.load(f)
    return []

def get_summary(self, ):
    scores = get_scores()
    if not scores:
        return {
            "average": 0,
            "completed": 0,
            "last_lesson": None
        }
    total = sum(s.get("score", 0) for s in scores)
    avg = total / len(scores)
    return {
        "average": round(avg, 2),
        "completed": len(scores),
        "last_lesson": scores[-1]["lesson"] if scores else None
    }

if __name__ == "__main__":
    print("Summary:", get_summary())

