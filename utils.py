class MessageStack:
    """Стэк для ID Сообщений."""
    def __init__(self) -> None:
        self.messages = []

    def length(self):
        return len(self.messages)

    def push(self, message_id: int):
        self.messages.append(message_id)

    def pop(self):
        if len(self.messages) == 0:
            return None
        removed = self.messages.pop()
        return removed
