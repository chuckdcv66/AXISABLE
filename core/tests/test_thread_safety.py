import unittest
import threading
import time
from interface_celestial_unified import CelestialGUI

class MockAgent:
    @property
    def agents(self):
        return [type("Agent", (), {"name": "Delta", "mood": "calm"})()]

    def process_voice_queue(self):
        self.voice_queue_processed = True

    def audit_memory(self):
        self.memory_audited = True

    def get_recent_lessons(self):
        return []

    voice_engine = type("VoiceEngine", (), {"toggle_mute": lambda s: None, "is_muted": False})()

class ThreadSafetyTests(unittest.TestCase):
    def setUp(self):
        self.agent = MockAgent()
        self.gui = CelestialGUI(self.agent)

    def test_voice_thread_executes(self):
        self.gui.voice_service_loop()
        self.assertTrue(hasattr(self.agent, "voice_queue_processed"))

    def test_memory_thread_executes(self):
        self.gui.memory_watcher_loop()
        self.assertTrue(hasattr(self.agent, "memory_audited"))

    def tearDown(self):
        self.gui._shutdown_flag.set()
        if self.gui.voice_thread:
            self.gui.voice_thread.join(timeout=1.0)
        if self.gui.memory_thread:
            self.gui.memory_thread.join(timeout=1.0)

if __name__ == "__main__":
    unittest.main()


