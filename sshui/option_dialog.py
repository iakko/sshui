from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QFileDialog,
)

_SSH_OPTION_NAMES = [
    "HostName",
    "User",
    "Port",
    "IdentityFile",
    "IdentitiesOnly",
    "ProxyCommand",
    "ProxyJump",
    "LocalForward",
    "RemoteForward",
    "PermitLocalCommand",
    "ForwardAgent",
    "ForwardX11",
    "ServerAliveInterval",
    "ServerAliveCountMax",
    "PreferredAuthentications",
    "ControlMaster",
    "ControlPath",
    "ControlPersist",
    "StrictHostKeyChecking",
    "UserKnownHostsFile",
    "SendEnv",
    "SetEnv",
    "Compression",
    "LogLevel",
]


class OptionDialog(QDialog):
    """Dialog for capturing option name/value pairs."""

    def __init__(self, parent=None, title: str = "Option", initial_option: str = "", initial_value: str = "") -> None:
        super().__init__(parent)
        self.setWindowTitle(title)

        self.option_input = QComboBox()
        self.option_input.setEditable(True)
        self.option_input.addItems(_SSH_OPTION_NAMES)
        if initial_option:
            self.option_input.setEditText(initial_option)
        self.value_input = QLineEdit(initial_value)
        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self._browse_file)

        value_layout = QHBoxLayout()
        value_layout.addWidget(self.value_input)
        value_layout.addWidget(self.browse_button)

        layout = QFormLayout(self)
        layout.addRow("Option:", self.option_input)
        layout.addRow("Value:", value_layout)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

        self.option_input.currentTextChanged.connect(self._on_option_changed)
        self._on_option_changed(self.option_input.currentText())

        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowTitleHint | Qt.WindowType.WindowCloseButtonHint)
        self.setSizeGripEnabled(False)
        self.adjustSize()

    def _on_option_changed(self, option: str):
        self.browse_button.setVisible(option == "IdentityFile")

    def _browse_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Identity File")
        if file:
            self.value_input.setText(file)

    @property
    def option_name(self) -> str:
        return self.option_input.currentText()

    @property
    def option_value(self) -> str:
        return self.value_input.text()
