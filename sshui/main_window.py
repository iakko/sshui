from __future__ import annotations

from typing import List
import shlex

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QTabWidget,
    QVBoxLayout
)

from sshcore.models import HostBlock
from .about_dialog import AboutDialog
from .terminal_window import TerminalWindow
from .host_panel import HostPanel
from .key_panel import KeyPanel


class MainWindow(QMainWindow):
    """Simple PyQt window that lists SSH host blocks via the core APIs."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("SSH-UI: The sshcli frontend!")
        self.resize(900, 520)
        self._terminal_windows: List[TerminalWindow] = []

        self._host_panel = HostPanel()
        self._key_panel = KeyPanel()
        self._setup_menus()
        self._setup_ui()

        self._host_panel.connect_to_host_requested.connect(self._connect_to_host)

    def _setup_ui(self) -> None:
        central = QWidget(self)
        layout = QVBoxLayout(central)

        self._tabs = QTabWidget()
        self._tabs.addTab(self._host_panel, "Hosts")
        self._tabs.addTab(self._key_panel, "Keys")

        layout.addWidget(self._tabs)
        self.setCentralWidget(central)

    def _setup_menus(self) -> None:
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        refresh_action = QAction("Refresh Hosts", self)
        refresh_action.setShortcut("Ctrl+R")
        refresh_action.triggered.connect(self._host_panel.load_hosts)
        file_menu.addAction(refresh_action)

        file_menu.addSeparator()
        quit_action = QAction("Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self._quit_application)
        file_menu.addAction(quit_action)

        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About sshcli UI", self)
        about_action.triggered.connect(self._show_about_dialog)
        help_menu.addAction(about_action)

    def _show_about_dialog(self) -> None:
        about_dialog = AboutDialog(self)
        about_dialog.exec()

    def _quit_application(self) -> None:
        app = QApplication.instance()
        if app is not None:
            app.quit()

    def _get_ssh_command_tokens(self, block: HostBlock) -> List[str]:
        return self._host_panel.get_ssh_command_tokens(block)

    def _connect_to_host(self, block: HostBlock) -> None:
        command_tokens = self._get_ssh_command_tokens(block)
        target_host = command_tokens[-1]
        
        terminal_window = TerminalWindow(command=command_tokens, title=f"SSH to {target_host}", parent=self)
        
        # Center the terminal window on the same screen as the main window
        main_window_screen = self.screen()
        if main_window_screen:
            screen_geometry = main_window_screen.geometry()
            terminal_window.move(screen_geometry.center() - terminal_window.rect().center())

        self._terminal_windows.append(terminal_window)
        terminal_window.show()

        def _cleanup(*_args) -> None:
            if terminal_window in self._terminal_windows:
                self._terminal_windows.remove(terminal_window)

        terminal_window.destroyed.connect(_cleanup)