pending_action = {
    "action": "shutdown",
    "confirmed": False
}
class StateManager:
    def __init__(self):
        self.pending_action = None

    def set_pending(self, action_callable):
        self.pending_action = action_callable

    def confirm(self):
        if self.pending_action:
            action = self.pending_action
            self.pending_action = None
            action()
            return True
        return False

    def has_pending(self):
        return self.pending_action is not None
