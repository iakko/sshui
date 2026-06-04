"""PyQt UI package for sshcli."""

from __future__ import annotations

import sys
from pathlib import Path

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu

from .constants import APP_NAME, APP_TITLE
from .main_window import MainWindow

__all__ = ["MainWindow", "main"]


def _patch_macos_app_menu(name: str) -> None:
    """Rename the macOS application menu (the 'Python' entry in the menu bar)."""
    try:
        from AppKit import NSApplication
        ns_app = NSApplication.sharedApplication()
        if ns_app is None:
            return
        menu = ns_app.mainMenu()
        if menu is None or menu.numberOfItems() == 0:
            return
        item = menu.itemAtIndex_(0)
        item.setTitle_(name)
        if item.submenu() is not None:
            item.submenu().setTitle_(name)
    except Exception as exc:
        import sys
        print(f"[sshui] could not patch macOS app menu: {exc}", file=sys.stderr)


def main() -> int:
    """Entry point used by the `sshui` console script."""
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationDisplayName(APP_NAME)

    icon_path = Path(__file__).parent / "sshui.svg"
    icon = QIcon(str(icon_path))
    app.setWindowIcon(icon)

    window = MainWindow()
    window.setWindowIcon(icon)
    window.setWindowTitle(APP_TITLE)

    tray_icon = QSystemTrayIcon(icon, app)
    tray_icon.setToolTip(APP_TITLE)
    
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
    QTimer.singleShot(0, lambda: _patch_macos_app_menu(APP_NAME))

    return app.exec()
