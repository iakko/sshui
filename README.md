# sshui

`sshui` is a PyQt6-based graphical frontend for the `sshcore` engine. It gives you a fast, tag-aware explorer for SSH configuration files, complete with host grouping, editing dialogs, and quick copy of SSH commands—without touching the command line.

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
