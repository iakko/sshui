import sys
import platform
from typing import List
from PyQt6.QtWidgets import QMainWindow
from termqt import Terminal, TerminalPOSIXExecIO

class TerminalWindow(QMainWindow):
    def __init__(self, command: List[str], title: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 800, 600)

        self.terminal = Terminal(800, 600)
        self.setCentralWidget(self.terminal)

        # Start the SSH process
        self._start_process(command)

    def _start_process(self, command: List[str]):
        if platform.system() in ["Linux", "Darwin"]:
            cmd_string = " ".join(command)
            self.terminal_io = TerminalPOSIXExecIO(
                self.terminal.row_len,
                self.terminal.col_len,
                cmd_string
            )
            
            self.terminal_io.stdout_callback = self.terminal.stdout
            self.terminal.stdin_callback = self.terminal_io.write
            self.terminal.resize_callback = self.terminal_io.resize
            self.terminal_io.spawn()
        else:
            self.terminal.stdout(f"Platform {platform.system()} not supported yet.\n")

if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    # Example usage:
    window = TerminalWindow(["ssh", "user@example.com"], "SSH to user@example.com")
    window.show()
    sys.exit(app.exec())
