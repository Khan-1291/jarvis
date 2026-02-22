class CommandRouter:
    def __init__(self, skills):
        self.skills = skills

    async def route(self, text):
        for skill in self.skills:
            handled, response = await skill.handle(text)
            if handled:
                return True, response
        return False, "I didn't understand"