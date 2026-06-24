# sshui

`sshui` is a PyQt6-based graphical frontend for the `sshcore` engine. It gives you a fast, tag-aware explorer for SSH configuration files, complete with host grouping, editing dialogs, and quick copy of SSH commands—without touching the command line.

## What's New in 1.2.2

- **macOS Dock icon** — the app icon now also shows in the macOS Dock (set via AppKit at startup), not just the menu-bar tray.

## What's New in 1.2.1

- **Application icon** — the app now ships and displays its own icon (window, dock/taskbar, and system tray).

## What's New in 1.2.0

- **Key content viewer** — select a key in the Keys tab and click the **View** button on a Path row to open a read-only window with the file content and a one-click Copy to Clipboard action.
- **Redesigned app icon** — new 32×32 icon with transparent padding, rounded corners, and the `>SSH` logotype in pixel font.
- Fixed `TypeError: 'type' object is not iterable` on startup with newer `cryptography` releases.
- Fixed `XPM pixels missing on image line 15` warning logged on every launch.

## What's New in 1.1.0

- **Key Management**: A dedicated panel for viewing, adding, and deleting SSH keys.
- **Terminal Execution**: Connect to hosts directly within an integrated terminal window.

## Features

- Flat and tag-grouped host browsers with live filtering.
- Tag editing dialog with color-coded tag definitions stored in the central `sshcli.json` configuration.
- Inline metadata display (tags, colors) and SSH command preview/copy.
- Context menus for editing/deleting hosts and quick navigation.
- Reuses the same settings/config sources managed by `sshcli`, so both tools stay in sync.

## Installation

```bash
pip install ixlab-sshui
```

This installs `sshcore` and PyQt6 automatically.

## Usage

Launch the UI via the console script:

```bash
sshui
```

or import and run the main window manually:

```python
from sshui import main
main()
```

## Development

1. Install dependencies for local hacking:

   ```bash
   pip install -e .[dev]
   ```

2. Run tests (UI-specific tests often rely on Qt’s offscreen plugins):

   ```bash
   pytest
   ```

`sshui` is MIT licensed. Feedback and contributions are welcome.
