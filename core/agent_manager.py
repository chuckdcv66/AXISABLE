class Agent:
    def __init__(self, name, mood):
        self.name = name
        self.mood = mood
        self.lessons = []

class VoiceEngine:
    def __init__(self):
        self.is_muted = False

    def toggle_mute(self):
        self.is_muted = not self.is_muted

class AgentManager:
    def __init__(self):
        self.agents = [
            Agent("Delta", "socratic"),
            Agent("Lyra", "montessori"),
            Agent("Kairos", "direct"),
            Agent("Noor", "mindful")
        ]
        self.active_agent = self.agents[0]
        self.voice_engine = VoiceEngine()

    def set_active_agent(self, agent):
        self.active_agent = agent

    def get_recent_lessons(self):
        return self.active_agent.lessons[:3]

    def process_voice_queue(self):
        pass

    def audit_memory(self):
        pass
