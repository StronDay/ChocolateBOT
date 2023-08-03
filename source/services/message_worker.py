class MessageWorker():

    def __init__(self) -> None:
        self.message = None

    def save_message(self, message):
        self.message = message

    def get_message(self):
        return self.message