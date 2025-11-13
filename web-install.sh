#!/bin/bash
# Quick installer for Claude Sounds Configurator
# Usage: curl -sSL https://raw.githubusercontent.com/AutumnsGrove/ClaudeCodeSounds/master/web-install.sh | bash

set -e

REPO_URL="https://github.com/AutumnsGrove/ClaudeCodeSounds.git"
INSTALL_DIR="$HOME/.claude-sounds"
BINARY_NAME="claude-sounds-config"

echo "🎵 Claude Sounds Configurator - Quick Installer"
echo ""

# Check if Go is installed
if ! command -v go &> /dev/null; then
    echo "❌ Go is not installed."
    echo ""
    echo "Please install Go 1.21 or higher first:"
    echo "  • Visit: https://golang.org/doc/install"
    echo "  • macOS: brew install go"
    echo "  • Ubuntu/Debian: sudo apt install golang-go"
    echo ""
    exit 1
fi

echo "✅ Go found: $(go version)"
echo ""

# Check for audio player
AUDIO_PLAYER=""
if command -v afplay &> /dev/null; then
    AUDIO_PLAYER="afplay"
elif command -v paplay &> /dev/null; then
    AUDIO_PLAYER="paplay"
elif command -v aplay &> /dev/null; then
    AUDIO_PLAYER="aplay"
fi

if [ -z "$AUDIO_PLAYER" ]; then
    echo "⚠️  Warning: No audio player found"
    echo "   Install one of: aplay (alsa-utils) or paplay (pulseaudio-utils)"
    echo ""
else
    echo "✅ Audio player found: $AUDIO_PLAYER"
    echo ""
fi

# Clone or update repository
if [ -d "$INSTALL_DIR" ]; then
    echo "📦 Updating existing installation..."
    cd "$INSTALL_DIR"
    git pull -q
else
    echo "📦 Cloning repository..."
    git clone -q "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

echo "🔨 Building configurator..."
go build -o "$BINARY_NAME" main.go

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo ""

    # Offer to add to PATH
    SHELL_RC=""
    if [ -n "$BASH_VERSION" ]; then
        SHELL_RC="$HOME/.bashrc"
    elif [ -n "$ZSH_VERSION" ]; then
        SHELL_RC="$HOME/.zshrc"
    fi

    if [ -n "$SHELL_RC" ]; then
        if ! grep -q "claude-sounds-config" "$SHELL_RC" 2>/dev/null; then
            echo "📝 Adding 'claude-sounds' command to $SHELL_RC..."
            echo "" >> "$SHELL_RC"
            echo "# Claude Sounds Configurator" >> "$SHELL_RC"
            echo "alias claude-sounds='cd $INSTALL_DIR && ./claude-sounds-config'" >> "$SHELL_RC"
            echo "✅ Added 'claude-sounds' command!"
            echo ""
            echo "Run 'source $SHELL_RC' or restart your terminal to use it"
        fi
    fi

    echo "🎉 Installation complete!"
    echo ""
    echo "🚀 Quick Start:"
    echo "  cd $INSTALL_DIR"
    echo "  ./claude-sounds-config"
    echo ""
    echo "Or if you added the alias:"
    echo "  claude-sounds"
    echo ""
    echo "See README.md for more information."
else
    echo "❌ Build failed"
    exit 1
fi
