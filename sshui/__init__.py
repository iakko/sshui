"""PyQt UI package for sshcli."""

from __future__ import annotations

import sys
from pathlib import Path

from PyQt6.QtCore import QTimer, QBuffer, QByteArray
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu

from .constants import APP_NAME, APP_TITLE
from .main_window import MainWindow

__all__ = ["MainWindow", "main"]


def _set_macos_app_name(name: str) -> None:
    """Set the macOS application name for an unbundled console-script app.

    Two distinct identities default to the interpreter name (e.g. ``python3.14``)
    and must be set separately, *before* ``QApplication`` initializes:

    * ``CFBundleName`` drives the bold menu-bar entry.
    * ``NSProcessInfo.processName`` drives the Dock tooltip.
    """
    if sys.platform != "darwin":
        return
    try:
        from Foundation import NSBundle, NSProcessInfo

        bundle = NSBundle.mainBundle()
        if bundle is not None:
            info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
            if info is not None:
                info["CFBundleName"] = name

        NSProcessInfo.processInfo().setProcessName_(name)
    except Exception as exc:  # pragma: no cover - platform/runtime guard
        print(f"[sshui] could not set macOS app name: {exc}", file=sys.stderr)


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


def _set_macos_dock_icon(icon: QIcon) -> None:
    """Set the macOS Dock icon.

    ``QApplication.setWindowIcon`` does not affect the Dock for a console-script
    app, so we hand the icon to AppKit explicitly. The SVG is rendered through
    Qt to PNG bytes because ``NSImage`` does not read SVG reliably.
    """
    if sys.platform != "darwin":
        return
    try:
        from AppKit import NSApplication, NSImage

        pixmap = icon.pixmap(512, 512)
        if pixmap.isNull():
            return
        data = QByteArray()
        buffer = QBuffer(data)
        buffer.open(QBuffer.OpenModeFlag.WriteOnly)
        pixmap.save(buffer, "PNG")
        buffer.close()

        ns_image = NSImage.alloc().initWithData_(bytes(data))
        if ns_image is None:
            return
        NSApplication.sharedApplication().setApplicationIconImage_(ns_image)
    except Exception as exc:  # pragma: no cover - platform/runtime guard
        print(f"[sshui] could not set macOS dock icon: {exc}", file=sys.stderr)


def main() -> int:
    """Entry point used by the `sshui` console script."""
    _set_macos_app_name(APP_NAME)

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationDisplayName(APP_NAME)

    icon_path = Path(__file__).parent / "sshui.svg"
    icon = QIcon(str(icon_path))
    app.setWindowIcon(icon)
    _set_macos_dock_icon(icon)

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
