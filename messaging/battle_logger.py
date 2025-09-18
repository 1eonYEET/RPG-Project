from messaging.notifier import Notifier

class BattleLogger:
    def __init__(self, notifier: Notifier):
        self.notifier = notifier
        self.logs = []

    def log(self, message: str):
        self.logs.append(message)

    def flush(self):
        for message in self.logs:
            self.notifier.notify(message)
        self.logs.clear()
