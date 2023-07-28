class MessageWorker():
    def __init__(self) -> None:
        pass

    def save_message(self, message):
        self.message = message

    def get_message(self):
        return self.message