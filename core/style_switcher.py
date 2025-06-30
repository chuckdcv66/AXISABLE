# style_switcher.py
from PyQt5.QtGui import QFont

def apply_style_mode(self, gui, mode):
    """
    Apply a different interface layout based on cognitive mode.
    gui: CelestialGUI instance
    mode: 'creative' | 'analytical' | 'flex'
    """
    if mode == "analytical":
        gui.sidebar.setMaximumWidth(220)
        gui.content_area.setStyleSheet("font-size: 12px; font-family: Segoe UI; background-color: #1e1e1e;")
        gui.xp_bar.setStyleSheet("color: #66ff99; font-size: 12px; font-family: monospace;")
        gui.streak_label.setText("🧠 Analytical Mode")
    elif mode == "creative":
        gui.sidebar.setMaximumWidth(300)
        gui.content_area.setStyleSheet("font-size: 14px; font-family: Comic Sans MS; background-color: #1a1a1a;")
        gui.xp_bar.setStyleSheet("color: #ffcc66; font-size: 14px; font-family: Georgia;")
        gui.streak_label.setText("🎨 Creative Mode")
    else:
        # Fallback or Flex Mode
        gui.sidebar.setMaximumWidth(250)
        gui.content_area.setStyleSheet("font-size: 13px; font-family: Consolas; background-color: #202020;")
        gui.xp_bar.setStyleSheet("color: #aaaaff; font-size: 13px;")
        gui.streak_label.setText("🌀 Flex Mode")

    # Visually force repaint
    gui.sidebar.repaint()
    gui.content_area.repaint()
    gui.xp_bar.repaint()
    gui.streak_label.repaint()
