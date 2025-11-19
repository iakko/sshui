from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QFrame,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About SSHUI")
        self.setFixedSize(420, 420)

        sshui_version = self._current_version("ixlab-sshui") or "unknown"
        sshcli_version = self._current_version("ixlab-sshcli")
        sshcore_version = self._current_version("ixlab-sshcore") or "unknown"

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        app_name = QLabel("SSH-UI")
        app_name.setFont(QFont("Arial", 20, QFont.Weight.Black))
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        app_name.setStyleSheet("color: #2c3e50; letter-spacing: 1px;")

        tagline = QLabel("Graphical companion for SSH power users")
        tagline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tagline.setStyleSheet("color: #7f8c8d; font-style: italic;")

        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)

        description = QLabel(
            "SSH-UI is a graphical companion for sshcli, providing a tag-aware host browser "
            "with quick access to connection details and editing actions.\n\n"
            "SSH-CLI is a CLI tool for exploring and managing SSH config files with tagging, backup, "
            "and search utilities to keep complex setups tidy."
        )

        description.setWordWrap(True)
        description.setAlignment(Qt.AlignmentFlag.AlignLeft)
        description.setStyleSheet("color: #34495e; padding: 2px")

        versions_lines = [
            f"<b>SSH-UI:</b> {sshui_version}",
            f"<b>SSH-CLI:</b> {'not installed' if not sshcli_version else sshcli_version}",
            f"<b>SSH-CORE:</b> {sshcore_version}",
        ]
        versions_info = QLabel(
            "<span style='color:#2c3e50; padding: 2px'>Versions</span><br>" + "<br>".join(versions_lines)
        )
        versions_info.setAlignment(Qt.AlignmentFlag.AlignLeft)
        versions_info.setTextFormat(Qt.TextFormat.RichText)

        info_card = QFrame()
        info_card.setStyleSheet(
            "QFrame {background-color: #f6f8fa; border: 1px solid #dce0e6; border-radius: 10px;}"
        )
        card_layout = QVBoxLayout(info_card)
        card_layout.setContentsMargins(14, 12, 14, 12)
        card_layout.setSpacing(5)
        card_layout.addWidget(description)
        card_layout.addWidget(versions_info)

        project_links = QLabel(
            '<a href="https://github.com/iakko/sshui">SSH-UI project page</a><br>'
            '<a href="https://github.com/iakko/sshcli">SSH-CLI project page</a><br>'
            '<a href="https://github.com/iakko/sshcore">SSH-CORE project page</a>'
        )
        project_links.setTextFormat(Qt.TextFormat.RichText)
        project_links.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        project_links.setOpenExternalLinks(True)
        project_links.setAlignment(Qt.AlignmentFlag.AlignLeft)

        author = QLabel(
            'Developed by <a href="mailto:iacopo.palazzi@gmail.com">Iacopo Palazzi</a>'
        )
        author.setTextFormat(Qt.TextFormat.RichText)
        author.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        author.setOpenExternalLinks(True)
        author.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(app_name)
        layout.addWidget(tagline)
        layout.addWidget(divider)
        layout.addWidget(info_card)
        layout.addWidget(project_links)
        layout.addWidget(author)

        self.setLayout(layout)
        
    
        
    def _current_version(self, package) -> str:
        try:
            from importlib.metadata import PackageNotFoundError, version as pkg_version
            return pkg_version(package)
        except Exception:
            return None
