class BaseSkill:
    async def handle(self, text):
        raise NotImplementedError