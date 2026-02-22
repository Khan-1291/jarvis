# skills/base_skill.py
class BaseSkill:
    def handle(self, text, player):
        raise NotImplementedError("Each skill must implement the handle() method")
