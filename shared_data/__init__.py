class SharedData:
    def __init__(self) -> None:
        self.dialogs = []

    def set_dialogs(self, dialogs: list):
        self.dialogs = dialogs.copy()
