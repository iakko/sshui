"""PyQt UI package for sshcli."""

from __future__ import annotations

import sys
from pathlib import Path

from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu

from .main_window import MainWindow

__all__ = ["MainWindow", "main"]


def main() -> int:
    """Entry point used by the `sshui` console script."""
    app = QApplication(sys.argv)
    app.setApplicationName("SSH-UI")
    app.setApplicationDisplayName("SSH-UI")

    icon_path = Path(__file__).parent / "sshui.xpm"
    icon = QIcon(str(icon_path))
    app.setWindowIcon(icon)

    window = MainWindow()
    window.setWindowIcon(icon)
    window.setWindowTitle("SSH-UI: The sshcli frontend!")

    tray_icon = QSystemTrayIcon(icon, app)
    tray_icon.setToolTip("SSH-UI: The sshcli frontend!")
    
    menu = QMenu()
    show_action = QAction("Show", app)
    quit_action = QAction("Quit", app)
    show_action.triggered.connect(window.show)
    quit_action.triggered.connect(app.quit)
    menu.addAction(show_action)
    menu.addAction(quit_action)
    
    tray_icon.setContextMenu(menu)
    tray_icon.show()
    tray_icon.activated.connect(window.show)

    window.show()
    
    return app.exec()
