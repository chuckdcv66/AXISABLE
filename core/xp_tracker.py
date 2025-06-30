# xp_tracker.py
import os, json

def get_xp_file(self, user="Riley"):
    path = os.path.join("data", user, "xp.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path

def load_xp(self, user="Riley"):
    path = get_xp_file(user)
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f).get("xp", 0)
    return 0

def save_xp(self, new_xp, user="Riley"):
    path = get_xp_file(user)
    with open(path, "w") as f:
        json.dump({"xp": new_xp}, f)

def add_xp(self, amount, user="Riley"):
    xp = load_xp(user)
    xp += amount
    save_xp(xp, user)
    return xp
