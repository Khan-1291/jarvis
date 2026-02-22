class AssistantEngine:
    def __init__(self, router, event_bus):
        self.router = router
        self.bus = event_bus

    async def process(self, text):
        await self.bus.emit("user_text", text)

        handled, response = await self.router.route(text)

        if response:
            await self.bus.emit("assistant_text", response)

        return handled