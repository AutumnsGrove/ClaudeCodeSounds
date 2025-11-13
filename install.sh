#!/bin/bash
# Installation script for Claude Sounds Configurator

set -e

echo "🎵 Claude Sounds Configurator - Installation Script"
echo ""

# Check if Go is installed
if ! command -v go &> /dev/null; then
    echo "❌ Go is not installed. Please install Go 1.21 or higher first."
    echo "   Visit: https://golang.org/doc/install"
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
    echo "⚠️  Warning: No audio player found (afplay, paplay, or aplay)"
    echo "   The configurator will still build, but you need one of these to play sounds."
    echo ""
else
    echo "✅ Audio player found: $AUDIO_PLAYER"
    echo ""
fi

# Build the configurator
echo "🔨 Building configurator..."
go build -o claude-sounds-config main.go

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo ""

    # Offer to install globally
    echo "Would you like to install the configurator globally? (requires sudo)"
    echo "This will copy it to /usr/local/bin/claude-sounds-config"
    read -p "Install globally? [y/N]: " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo cp claude-sounds-config /usr/local/bin/claude-sounds-config
        sudo chmod +x /usr/local/bin/claude-sounds-config
        echo "✅ Installed globally! You can now run: claude-sounds-config"
    else
        echo "ℹ️  Binary built locally. Run with: ./claude-sounds-config"
    fi

    echo ""
    echo "🎉 Installation complete!"
    echo ""
    echo "Usage:"
    echo "  ./claude-sounds-config          # Run from this directory"
    echo "  claude-sounds-config            # Run globally (if installed)"
    echo ""
    echo "See CONFIGURATOR.md for more details."
else
    echo "❌ Build failed"
    exit 1
fi
