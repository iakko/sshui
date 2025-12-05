from __future__ import annotations
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QComboBox,
    QCheckBox,
    QPushButton,
    QHBoxLayout,
    QFileDialog,
)
from sshcore import keys as keys_module

class KeyDialog(QDialog):
    """Dialog for capturing key generation options."""

    def __init__(self, parent=None, title: str = "Generate Key Pair"):
        super().__init__(parent)
        self.setWindowTitle(title)

        self.name_input = QLineEdit()
        self.size_input = QSpinBox()
        self.size_input.setRange(1024, 16384)
        self.size_input.setValue(2048)
        self.public_exponent_input = QLineEdit("65537")
        self.path_input = QLineEdit("~/.ssh/keys")
        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self._browse_path)

        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.browse_button)

        self.key_type_input = QComboBox()
        self.key_type_input.addItems(["rsa"])
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.comment_input = QLineEdit()
        self.private_format_input = QComboBox()
        self.private_format_input.addItems(keys_module.PRIVATE_FORMAT_OPTIONS)
        self.private_encoding_input = QComboBox()
        self.private_encoding_input.addItems(keys_module.ENCODING_OPTIONS)
        self.public_format_input = QComboBox()
        self.public_format_input.addItems(keys_module.PUBLIC_FORMAT_OPTIONS)
        self.public_encoding_input = QComboBox()
        self.public_encoding_input.addItems(keys_module.ENCODING_OPTIONS)
        self.overwrite_input = QCheckBox()

        layout = QFormLayout(self)
        layout.addRow("Name:", self.name_input)
        layout.addRow("Size:", self.size_input)
        layout.addRow("Public Exponent:", self.public_exponent_input)
        layout.addRow("Path:", path_layout)
        layout.addRow("Key Type:", self.key_type_input)
        layout.addRow("Password:", self.password_input)
        layout.addRow("Comment:", self.comment_input)
        layout.addRow("Private Format:", self.private_format_input)
        layout.addRow("Private Encoding:", self.private_encoding_input)
        layout.addRow("Public Format:", self.public_format_input)
        layout.addRow("Public Encoding:", self.public_encoding_input)
        layout.addRow("Overwrite:", self.overwrite_input)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowTitleHint | Qt.WindowType.WindowCloseButtonHint)
        self.setSizeGripEnabled(False)
        self.adjustSize()

    def _browse_path(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.path_input.setText(directory)

    @property
    def key_options(self) -> dict:
        return {
            "name": self.name_input.text(),
            "size": self.size_input.value(),
            "public_exponent": int(self.public_exponent_input.text()),
            "path": self.path_input.text(),
            "key_type": self.key_type_input.currentText(),
            "password": self.password_input.text(),
            "comment": self.comment_input.text(),
            "private_format": self.private_format_input.currentText(),
            "private_encoding": self.private_encoding_input.currentText(),
            "public_format": self.public_format_input.currentText(),
            "public_encoding": self.public_encoding_input.currentText(),
            "overwrite": self.overwrite_input.isChecked(),
        }
