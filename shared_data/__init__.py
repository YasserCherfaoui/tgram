from shared_data.data_types import DialogsLayoutChild


class SharedData:
    def __init__(self) -> None:
        self.dialogs = []
        self.current_dialog_index = 0
        self.current_dialog: DialogsLayoutChild | None = None
        self.dialogs_layout: list[DialogsLayoutChild] = []

    def set_dialogs(self, dialogs: list):
        self.dialogs = dialogs.copy()
