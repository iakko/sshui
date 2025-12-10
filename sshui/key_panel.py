from __future__ import annotations
from typing import Callable, List, Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QSplitter,
    QTableWidget,
    QMessageBox,
    QTableWidgetItem,
    QHeaderView,
    QSizePolicy,
    QToolButton,
    QStyle,
)

from sshcore import keys as keys_module
from .key_dialog import KeyDialog

class KeyPanel(QWidget):
    """
    A widget that displays the list of SSH keys and their details.
    """
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._keys_list: QListWidget
        self._key_details_table: QTableWidget
        self._key_pairs: List[keys_module.KeyPairInfo] = []
        self._setup_ui()
        self.load_keys()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        button_bar = QHBoxLayout()
        button_bar.setContentsMargins(0, 0, 0, 0)
        button_bar.setSpacing(6)
        button_bar.addWidget(self._make_tool_button("New Key", QStyle.StandardPixmap.SP_FileIcon, self._add_key))
        button_bar.addWidget(self._make_tool_button("Delete Key", QStyle.StandardPixmap.SP_TrashIcon, self._delete_key))
        button_bar.addStretch()
        layout.addLayout(button_bar)

        splitter = QSplitter()
        splitter.setChildrenCollapsible(False)
        splitter.addWidget(self._build_keys_list_panel())
        splitter.addWidget(self._build_key_details_panel())
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        layout.addWidget(splitter)

    def _build_keys_list_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self._keys_list = QListWidget()
        self._keys_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._keys_list.currentRowChanged.connect(self._show_key_details)
        layout.addWidget(self._keys_list)

        return panel

    def _build_key_details_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self._key_details_table = QTableWidget()
        self._key_details_table.setColumnCount(2)
        self._key_details_table.setHorizontalHeaderLabels(["Property", "Value"])
        self._key_details_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._key_details_table.verticalHeader().setVisible(False)
        self._key_details_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._key_details_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._key_details_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        layout.addWidget(self._key_details_table)

        return panel

    def _add_key(self) -> None:
        dialog = KeyDialog(self)
        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        try:
            keys_module.generate_key_pair(**dialog.key_options)
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"Failed to generate key pair:\n{exc}")
            return

        self.load_keys()

    def _delete_key(self) -> None:
        index = self._keys_list.currentRow()
        if index < 0 or index >= len(self._key_pairs):
            QMessageBox.warning(self, "No Key Selected", "Select a key to delete.")
            return

        key_pair = self._key_pairs[index]

        response = QMessageBox.question(
            self,
            "Delete Key",
            f"Are you sure you want to delete key pair '{key_pair.base_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if response != QMessageBox.StandardButton.Yes:
            return

        try:
            if key_pair.private_info and key_pair.private_info.exists:
                key_pair.private_info.path.unlink()
            if key_pair.public_info and key_pair.public_info.exists:
                key_pair.public_info.path.unlink()
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"Failed to delete key pair:\n{exc}")
            return

        self.load_keys()

    def load_keys(self) -> None:
        """Fetch key pairs from the shared config logic and display them."""
        try:
            # Assuming default ssh path, can be changed later
            self._key_pairs = keys_module.list_key_pairs("~/.ssh/keys")
        except Exception as exc:  # pragma: no cover - UI feedback
            QMessageBox.critical(self, "Error", f"Failed to load keys:\n{exc}")
            return

        self._keys_list.clear()
        for key_pair in self._key_pairs:
            self._keys_list.addItem(key_pair.base_name)

    def _show_key_details(self, index: int) -> None:
        if index < 0 or index >= len(self._key_pairs):
            self._key_details_table.setRowCount(0)
            return

        key_pair = self._key_pairs[index]
        self._key_details_table.setRowCount(0)

        self._add_key_info("Private Key", key_pair.private_info)
        self._add_key_info("Public Key", key_pair.public_info)

    def _add_key_info(self, title: str, key_info: Optional[keys_module.KeyFileInfo]):
        row = self._key_details_table.rowCount()
        self._key_details_table.insertRow(row)
        title_item = QTableWidgetItem(title)
        title_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        self._key_details_table.setItem(row, 0, title_item)
        self._key_details_table.setSpan(row, 0, 1, 2)

        if key_info is None:
            row = self._key_details_table.rowCount()
            self._key_details_table.insertRow(row)
            self._key_details_table.setItem(row, 0, QTableWidgetItem("Info"))
            self._key_details_table.setItem(row, 1, QTableWidgetItem("Not found"))
            return

        def add_row(prop, value):
            row = self._key_details_table.rowCount()
            self._key_details_table.insertRow(row)
            self._key_details_table.setItem(row, 0, QTableWidgetItem(prop))
            self._key_details_table.setItem(row, 1, QTableWidgetItem(value))

        add_row("Path", str(key_info.path))
        add_row("Exists", str(key_info.exists))
        if key_info.exists:
            add_row("Size", str(key_info.size))
            add_row("Mode", oct(key_info.mode))
            add_row("Modified At", str(key_info.modified_at))
            add_row("Description", key_info.description)
        if key_info.error:
            add_row("Error", key_info.error)

    def _make_tool_button(self, text: str, icon: QStyle.StandardPixmap, slot: Callable[[], None]) -> QToolButton:
        button = QToolButton()
        button.setIcon(self.style().standardIcon(icon))
        button.setText(text)
        button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        button.setAutoRaise(True)
        button.clicked.connect(slot)
        return button
