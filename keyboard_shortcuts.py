import threading
from app import App


class KeyboardShortcut:
    def __init__(self, application: App) -> None:
        self.app = application
        self.running = True
        self.keypress_thread = threading.Thread(target=self.handle_keypresses)
        self.keypress_thread.start()

    def handle_keypresses(self):
        if self.app.ui.stdscr is not None:
            while self.running:
                key = self.app.ui.stdscr.getch()
                if key == ord("j"):
                    self.app.ui.dialog_forward()
                if key == ord("k"):
                    self.app.ui.dialog_backward()
                if key == ord("q"):
                    self.app.destroy()

    def stop(self):
        self.running = False
