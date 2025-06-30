import os, json, time
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

from thinking_mode import detect_mode
from adaptive_logger import log_mode_event
from xp_tracker import add_xp
from score_tracker import save_score

PROFILE_FILE = "active_user.json"
def get_active_user(self, ):
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, 'r') as f:
            return json.load(f).get("user", "Riley")
    return "Riley"

PROFILE_DIR = os.path.join("data", get_active_user())
os.makedirs(PROFILE_DIR, exist_ok=True)

def update_streak(self, ):
    import datetime
    today = datetime.date.today()
    streak_file = os.path.join(PROFILE_DIR, "user_streak.log")
    streak = 1
    if os.path.exists(streak_file):
        with open(streak_file) as f:
            last = f.read().strip()
            if last:
                last_date = datetime.datetime.strptime(last, "%Y-%m-%d").date()
                if (today - last_date).days == 1:
                    streak += 1
    with open(streak_file, 'w') as f:
        f.write(str(today))
    return streak

class LessonWindow(QWidget):
    def __init__(self, lesson, agent_manager):
        super().__init__()
        self.lesson = lesson
        self.agent_manager = agent_manager
        self.setStyleSheet("background-color: #1e1e1e; color: white; font-family: Consolas;")
        self.setWindowTitle(lesson.name)
        self.start_time = time.time()

        layout = QVBoxLayout()

        video_id = getattr(lesson, 'video_id', None)
        mp4_path = getattr(lesson, 'video_path', None)

        if video_id:
            web = QWebEngineView()
            web.setUrl(QUrl(f"httpos.path.join('s:\', 'www.youtube-nocookie.com', 'embed', '{video_id}?autoplay=1')"))
            web.setMinimumHeight(360)
            layout.addWidget(web)
        elif mp4_path:
            self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
            vw = QVideoWidget()
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(mp4_path)))
            self.player.setVideoOutput(vw)
            vw.setMinimumHeight(360)
            layout.addWidget(vw)
            self.player.play()

        self.content = QTextEdit(getattr(lesson, 'content', str(lesson)))
        self.content.setReadOnly(True)
        layout.addWidget(self.content)

        self.quiz_label = QLabel("Quiz: Answer to complete lesson")
        layout.addWidget(self.quiz_label)

        self.quiz_input = QTextEdit()
        self.quiz_input.setFixedHeight(80)
        layout.addWidget(self.quiz_input)

        self.submit_btn = QPushButton("Submit Answer")
        self.submit_btn.clicked.connect(self.mark_complete)
        layout.addWidget(self.submit_btn)

        self.feedback = QLabel("")
        layout.addWidget(self.feedback)

        self.setLayout(layout)

    def mark_complete(self):
        end_time = time.time()
        answer = self.quiz_input.toPlainText().strip()

        if len(answer) < 3:
            self.feedback.setText("\U0001F6D1 Please write a longer answer.")
            return

        content_type = "video" if getattr(self.lesson, "video_id", None) or getattr(self.lesson, "video_path", None) else "text"
        mode, confidence = detect_mode(answer, self.start_time, end_time, content_type)
        log_mode_event(self.lesson.name, mode, confidence, reason=["length", "time"])

        with open(os.path.join(PROFILE_DIR, "completed_lessons.txt"), "a") as f:
            f.write(self.lesson.name + "\n")

        save_score(self.lesson.name, 100, quiz_answer=answer, mode=mode, confidence=confidence)

        streak = update_streak()
        self.feedback.setText(f"\u2705 Marked complete! \U0001F525 Streak: {streak} days")
        if hasattr(self.parent(), 'streak_label'):
            self.parent().streak_label.setText(f"\U0001F525 {streak}-day streak")

        xp_award = 25 if mode == "creative" else 15 if mode == "analytical" else 10
        xp_total = add_xp(xp_award, get_active_user())

        if hasattr(self.parent(), 'xp_bar'):
            blocks = int((xp_total % 100) / 20)
            bar = "█" * blocks + "░" * (5 - blocks)
            percent = xp_total % 100
            self.parent().xp_bar.setText(f"XP: {bar} {percent}%")
