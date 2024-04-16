from telethon.tl.custom.dialog import Dialog
from dataclasses import dataclass


@dataclass
class DialogsLayoutChild:
    dialog: Dialog
    position: tuple[int, int]
    hidden: bool = False
