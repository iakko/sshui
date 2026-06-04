from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)


class KeyContentDialog(QDialog):
    """Read-only viewer for a single key file with a copy-to-clipboard action."""

    def __init__(self, parent=None, *, path: Path) -> None:
        super().__init__(parent)
        self.setWindowTitle(f"Key Content — {path.name}")
        self.resize(660, 420)
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.WindowTitleHint
            | Qt.WindowType.CustomizeWindowHint
            | Qt.WindowType.WindowCloseButtonHint
        )
        self._path = path
        self._setup_ui()
        self._load_content()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        self._path_label = QLabel()
        self._path_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        layout.addWidget(self._path_label)

        self._text_edit = QTextEdit()
        self._text_edit.setReadOnly(True)
        mono = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
        mono.setPointSize(10)
        self._text_edit.setFont(mono)
        layout.addWidget(self._text_edit)

        button_bar = QHBoxLayout()
        button_bar.addStretch()

        self._copy_btn = QPushButton("Copy to Clipboard")
        self._copy_btn.clicked.connect(self._copy_to_clipboard)
        button_bar.addWidget(self._copy_btn)

        close_btn = QPushButton("Close")
        close_btn.setDefault(True)
        close_btn.clicked.connect(self.accept)
        button_bar.addWidget(close_btn)

        layout.addLayout(button_bar)

    # ------------------------------------------------------------------
    # Logic
    # ------------------------------------------------------------------

    def _load_content(self) -> None:
        self._path_label.setText(str(self._path))
        try:
            content = self._path.read_text(encoding="utf-8")
        except Exception as exc:
            self._text_edit.setPlainText(f"[Error reading file: {exc}]")
            self._text_edit.setEnabled(False)
            self._copy_btn.setEnabled(False)
            return
        self._text_edit.setPlainText(content)

    def _copy_to_clipboard(self) -> None:
        QApplication.clipboard().setText(self._text_edit.toPlainText())
        self._copy_btn.setText("Copied!")
        self._copy_btn.setEnabled(False)
