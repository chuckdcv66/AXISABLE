import os
import json
from types import SimpleNamespace

LESSON_DIR = os.path.join("curriculum", "lessons")

class Lesson:
    def __init__(self, name, title, content, video_id=None, video_path=None):
        self.name = name
        self.title = title
        self.content = content
        self.video_id = video_id
        self.video_path = video_path

    def __repr__(self):
        return f"Lesson({self.name})"

def load_lessons(self, ):
    lessons = []
    if not os.path.exists(LESSON_DIR):
        print(f"[LESSON LOADER] Directory missing: {LESSON_DIR}")
        return lessons

    for filename in sorted(os.listdir(LESSON_DIR)):
        if filename.endswith(".json"):
            path = os.path.join(LESSON_DIR, filename)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    lesson = Lesson(
                        name=data.get("name", filename[:-5]),
                        title=data.get("title", "Untitled"),
                        content=data.get("content", ""),
                        video_id=data.get("video_id"),
                        video_path=data.get("video_path")
                    )
                    lessons.append(lesson)
            except Exception as e:
                print(f"[ERROR] Failed to load {filename}: {e}")

    print(f"[LESSON LOADER] Loaded {len(lessons)} lessons")
    return lessons

def get_recent_lessons(self, limit=5):
    all_lessons = load_lessons()
    return all_lessons[-limit:] if len(all_lessons) > limit else all_lessons
