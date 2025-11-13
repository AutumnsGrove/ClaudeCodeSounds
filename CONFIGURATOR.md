# 🎵 Claude Sounds Configurator

A beautiful terminal user interface (TUI) for easily configuring Claude Code sound themes. Built with [Charm Bracelet's Bubble Tea](https://github.com/charmbracelet/bubbletea) framework.

## ✨ Features

- **Interactive TUI** - Beautiful terminal interface for selecting sound themes
- **Sound Previews** - Preview themes before applying them
- **Auto-detection** - Automatically detects your system's audio player (afplay/aplay/paplay)
- **Safe Updates** - Only modifies sound hooks, preserves all other settings
- **Automatic Backups** - Creates timestamped backups before modifying settings
- **Cross-platform** - Works on macOS, Linux, and Windows

## 🚀 Quick Start

### One-Liner Installation (Recommended)

The fastest way to get started:

```bash
curl -sSL https://raw.githubusercontent.com/AutumnsGrove/ClaudeCodeSounds/master/web-install.sh | bash
```

This will:
- Clone the repository to `~/.claude-sounds`
- Build the configurator automatically
- Optionally add a `claude-sounds` command to your shell

Then just run:
```bash
claude-sounds
# or
cd ~/.claude-sounds && ./claude-sounds-config
```

### Prerequisites

1. **Go 1.21 or higher**
2. **Audio player** installed:
   - **macOS**: `afplay` (built-in)
   - **Linux**: `aplay` (alsa-utils) or `paplay` (pulseaudio-utils)
   - **Windows**: PowerShell (built-in)

### Manual Installation

#### Option 1: Run from Source (Development)

```bash
# Clone and enter the repository
git clone https://github.com/AutumnsGrove/ClaudeCodeSounds.git
cd ClaudeCodeSounds

# Run directly
go run main.go
```

#### Option 2: Build and Install

```bash
# Use the installer script
./install.sh

# Or manually build
go build -o claude-sounds-config main.go
./claude-sounds-config

# Optional: Install globally
sudo mv claude-sounds-config /usr/local/bin/
claude-sounds-config
```

## 🎮 Usage

### Navigation

**Browsing Mode:**
- **↑/↓ Arrow Keys** - Navigate through sound themes
- **P or Space** - Preview the selected theme (plays session_start.wav)
- **Enter** - Select theme and show confirmation dialog
- **Q or Ctrl+C** - Quit without making changes

**Confirmation Dialog:**
- **Y** - Confirm and save changes
- **N or ESC** - Cancel and return to theme list

### Applying a Theme

1. Launch the configurator
2. Use **↑/↓** arrow keys to browse available themes
3. Press **P** or **Space** to preview a theme's sound
4. Press **Enter** when you find the theme you want
5. A confirmation dialog appears showing what will change
6. Press **Y** to confirm or **N** to cancel
7. On confirmation, the tool will:
   - Create a backup at `~/.claude/settings.json.backup_TIMESTAMP`
   - Update your sound hooks
   - Preserve all other hooks and settings
   - Show a success message

## 🎨 Available Themes

### Terminal Native (Default)
Original cyberpunk terminal aesthetic - warm and welcoming with digital grit.

### Cyberpunk Intense
Enhanced digital intensity with aggressive terminal energy and heavy bit-crushing.

### Retro Terminal
Classic 80s computing aesthetic with clean sine waves and nostalgic charm.

### Drift
Ambient water-inspired soundscape for transcendent flow state and deep focus.

### Void
Cosmic liminal space with deep drones and stellar resonance.

## 🔧 How It Works

### Settings File Location

The configurator updates: `~/.claude/settings.json`

### Hook Preservation

The tool intelligently manages your settings:

- **Updates these hooks**:
  - `session_start`
  - `session_end`
  - `tool_start`
  - `tool_complete`
  - `prompt_submit`
  - `response_start`
  - `response_end`
  - `subagent_done`
  - `precompact_warning`
  - `notification`

- **Preserves everything else**:
  - Custom hooks you've added
  - All other Claude Code settings
  - Comments and formatting (as much as JSON allows)

### Backup System

Every time you apply a theme, a backup is created:

```
~/.claude/settings.json.backup_20231113_142530
```

The timestamp format is: `YYYYMMDD_HHMMSS`

You can restore from a backup if needed:

```bash
cp ~/.claude/settings.json.backup_20231113_142530 ~/.claude/settings.json
```

## 📁 Project Structure

```
ClaudeCodeSounds/
├── main.go                    # Configurator source code
├── go.mod                     # Go module definition
├── go.sum                     # Dependency checksums
├── claude-sounds-config       # Compiled binary (after build)
└── CONFIGURATOR.md           # This file
```

## 🛠️ Development

### Dependencies

- [Bubble Tea](https://github.com/charmbracelet/bubbletea) - TUI framework
- [Bubbles](https://github.com/charmbracelet/bubbles) - TUI components
- [Lip Gloss](https://github.com/charmbracelet/lipgloss) - Style definitions

### Building

```bash
# Install dependencies
go mod tidy

# Build
go build -o claude-sounds-config main.go

# Run
./claude-sounds-config
```

### Code Structure

The configurator consists of:

1. **Audio Player Detection** - Automatically finds `afplay`, `aplay`, or `paplay`
2. **Sound Suite Scanner** - Discovers available themes in the repository
3. **Bubble Tea Model** - Manages application state and UI
4. **JSON Merger** - Carefully updates only sound hooks while preserving other settings
5. **Backup System** - Creates timestamped backups before any changes

## 🐛 Troubleshooting

### "No audio player found"

**Solution**: Install an audio player:
- **Ubuntu/Debian**: `sudo apt install alsa-utils` or `sudo apt install pulseaudio-utils`
- **Fedora/RHEL**: `sudo dnf install alsa-utils` or `sudo dnf install pulseaudio-utils`
- **Arch**: `sudo pacman -S alsa-utils` or `sudo pacman -S pulseaudio`
- **macOS**: `afplay` is built-in

### "No sound suites found"

**Solution**: Make sure you're running the configurator from the `ClaudeCodeSounds` repository directory, or that the sound files exist in subdirectories.

### Sounds not playing in Claude Code

**Possible issues**:
1. Check that paths in `~/.claude/settings.json` are correct
2. Verify audio files exist at the specified paths
3. Test playing a sound manually:
   ```bash
   afplay ~/path/to/ClaudeCodeSounds/session_start.wav
   ```

### JSON parsing errors

If the configurator reports JSON errors:
1. Validate your existing `~/.claude/settings.json`:
   ```bash
   cat ~/.claude/settings.json | jq .
   ```
2. Restore from a backup if needed
3. If no backup exists, manually fix the JSON syntax

## 🤝 Contributing

Improvements welcome! Potential enhancements:

- [ ] Add custom theme creation
- [ ] Support for mixing and matching individual sounds
- [ ] Volume adjustment per sound
- [ ] Export/import theme configurations
- [ ] Theme marketplace/sharing

## 📜 License

MIT License - See main repository LICENSE file

## 🙏 Credits

- Built with [Charm Bracelet](https://charm.sh/) tools
- Sound themes created for Claude Code
- TUI design inspired by modern terminal aesthetics

---

**Version**: 1.0
**Compatibility**: Claude Code 2.0+ with hooks support
**Platform**: Cross-platform (macOS, Linux, Windows)
