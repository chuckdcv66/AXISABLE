import os, sys, json, time
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QApplication,
    QHBoxLayout, QListWidget, QListWidgetItem, QStackedWidget, QFrame
)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

# Add 'core' to sys.path
core_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'core'))
if core_path not in sys.path:
    sys.path.insert(0, core_path)

from thinking_mode import detect_mode
from adaptive_logger import log_mode_event
from xp_tracker import add_xp
from score_tracker import save_score
from agent_manager import AgentManager
from lesson_loader import load_lessons

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PROFILE_FILE = os.path.join(BASE_DIR, 'active_user.json')

def get_active_user():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, 'r') as f:
            return json.load(f).get("user", "Riley")
    return "Riley"

PROFILE_DIR = os.path.join(BASE_DIR, 'data', get_active_user())
os.makedirs(PROFILE_DIR, exist_ok=True)

def update_streak():
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
            web.setUrl(QUrl(f"https://www.youtube-nocookie.com/embed/{video_id}?autoplay=1"))
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

        info_frame = QFrame()
        info_layout = QHBoxLayout()
        self.feedback = QLabel("")
        self.streak_label = QLabel("")
        self.xp_bar = QLabel("")

        info_layout.addWidget(self.feedback)
        info_layout.addStretch(1)
        info_layout.addWidget(self.streak_label)
        info_layout.addWidget(self.xp_bar)
        info_frame.setLayout(info_layout)
        layout.addWidget(info_frame)

        self.setLayout(layout)

    def mark_complete(self):
        end_time = time.time()
        answer = self.quiz_input.toPlainText().strip()

        if len(answer) < 3:
            self.feedback.setText("⛑ Please write a longer answer.")
            return

        content_type = "video" if getattr(self.lesson, "video_id", None) or getattr(self.lesson, "video_path", None) else "text"
        mode, confidence = detect_mode(answer, self.start_time, end_time, content_type)
        log_mode_event(self.lesson.name, mode, confidence, reason=["length", "time"])

        with open(os.path.join(PROFILE_DIR, "completed_lessons.txt"), "a") as f:
            f.write(self.lesson.name + "\n")

        save_score(self.lesson.name, 100, quiz_answer=answer, mode=mode, confidence=confidence)

        streak = update_streak()
        self.feedback.setText(f"✅ Marked complete! 🔥 Streak: {streak} days")
        self.streak_label.setText(f"🔥 {streak}-day streak")

        xp_award = 25 if mode == "creative" else 15 if mode == "analytical" else 10
        xp_total = add_xp(xp_award, get_active_user())
        blocks = int((xp_total % 100) / 20)
        bar = "█" * blocks + "░" * (5 - blocks)
        percent = xp_total % 100
        self.xp_bar.setText(f"XP: {bar} {percent}%")

class CelestialApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Celestial Companion Interface")
        self.setStyleSheet("background-color: #111; color: white; font-family: Consolas;")
        self.agent_manager = AgentManager()
        self.lesson_stack = QStackedWidget()
        self.agent_list = QListWidget()
        self.agent_list.setFixedWidth(240)
        self.agent_list.itemClicked.connect(self.load_lessons_for_agent)

        agents = getattr(self.agent_manager, 'agents', [])

        for agent in agents:
            item = QListWidgetItem(agent.name)
            item.setData(Qt.UserRole, agent)
            item.setTextAlignment(Qt.AlignCenter)
            self.agent_list.addItem(item)

        outer = QHBoxLayout()
        outer.addWidget(self.agent_list)
        outer.addWidget(self.lesson_stack, 1)
        self.setLayout(outer)

    def load_lessons_for_agent(self, item):
        agent = item.data(Qt.UserRole)
        lessons = load_lessons()
        self.lesson_stack.clear()
        for lesson in lessons:
            lesson_widget = LessonWindow(lesson, agent_manager=self.agent_manager)
            self.lesson_stack.addWidget(lesson_widget)
        if lessons:
            self.lesson_stack.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CelestialApp()
    window.resize(1280, 800)
    window.show()
    sys.exit(app.exec_())
