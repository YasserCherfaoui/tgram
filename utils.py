from shared_data.data_types import DialogsLayoutChild


def get_dialog_index(
    dialogs: list[DialogsLayoutChild], dialog: DialogsLayoutChild
) -> int:
    for i, j in enumerate(dialogs):
        if j.dialog.id == dialog.dialog.id:
            return i
    return -1
