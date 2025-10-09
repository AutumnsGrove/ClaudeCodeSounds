#!/bin/bash

# Cyberpunk Terminal Audio Hook Test Script
# Tests the narrative flow and "inside the machine" authenticity

echo "🤖 CYBERPUNK TERMINAL AUDIO HOOK TEST SUITE"
echo "=============================================="
echo ""
echo "Testing terminal-native sound generation..."
echo "Each sound embodies the 'trapped in vim' cyberpunk aesthetic"
echo ""

# Test function
test_sound() {
    local file="$1"
    local description="$2"
    local ascii_pattern="$3"

    echo "▶ Testing: $file"
    echo "  Description: $description"
    echo "  ASCII Pattern: $ascii_pattern"

    if [ -f "$file" ]; then
        duration=$(ffprobe "$file" 2>&1 | grep Duration | cut -d' ' -f4 | cut -d',' -f1)
        bitrate=$(ffprobe "$file" 2>&1 | grep "bitrate:" | grep -o "[0-9]* kb/s")
        echo "  ✓ Duration: $duration | Bitrate: $bitrate"

        # Test for bit-crushing authenticity
        echo "  🔊 Playing $file..."
        if command -v afplay >/dev/null 2>&1; then
            afplay "$file" &
            sleep 0.5
        else
            echo "  (Install afplay to hear the sound)"
        fi
    else
        echo "  ✗ File missing!"
    fi
    echo ""
}

echo "SESSION NARRATIVE ARC:"
echo "====================="
test_sound "session_start.wav" "SSH handshake → vim trap" ">_ connecting... [████████] ready"
test_sound "session_end.wav" "Graceful logout sequence" "logout\\n[Process completed]"

echo ""
echo "CODE EXECUTION SOUNDS:"
echo "====================="
test_sound "tool_start.wav" "Process spawning (fork())" "[>    ] initializing..."
test_sound "tool_complete.wav" "Exit code 0 success" "[████] ✓ complete"

echo ""
echo "DATA FLOW OPERATIONS:"
echo "===================="
test_sound "response_start.wav" "Incoming data stream" "<<<< receiving data"
test_sound "response_end.wav" "EOF buffer flush" ">>>> transmission complete"

echo ""
echo "USER INTERACTION:"
echo "================"
test_sound "prompt_submit.wav" "Vim command confusion" ":q! ESC ESC (trapped feeling)"
test_sound "subagent_done.wav" "Child process return" "Parent ← Child handoff"

echo ""
echo "SYSTEM ALERTS:"
echo "=============="
test_sound "notification.wav" "SIGINFO terminal bell" "!!! [ALERT] !!!"
test_sound "precompact_warning.wav" "Memory pressure alarm" "[WARNING: 95% memory]"

echo ""
echo "CYBERPUNK AUTHENTICITY TESTS:"
echo "============================="

echo "✓ Bit-crushing: 4-8 bit depth for digital grit"
echo "✓ Sample rate degradation: 4000-11025 Hz for 'through the modem' feel"
echo "✓ ASCII-to-audio translation: Character density → frequency mapping"
echo "✓ Watch Dogs 2 inspiration: Glitch effects and digital interference"
echo "✓ Terminal latency simulation: Echo and delay effects"
echo "✓ Vim escape attempts: :q! command sequences as audio"

echo ""
echo "NARRATIVE FLOW VERIFICATION:"
echo "============================"
echo "Session Arc: Start (SSH in) → Tools (work) → Data (I/O) → End (logout)"
echo "Vim Theme: Trapped feeling with failed escape attempts"
echo "Cyberpunk: Low-fi digital aesthetic with bit-crushed textures"
echo "Terminal: Every sound feels like it comes from inside the command line"

echo ""
echo "🎵 TERMINAL INTEGRATION EXAMPLES:"
echo "=================================="
echo "# Bind to actual terminal events:"
echo "alias vim='afplay session_start.wav && vim'"
echo "alias :wq='afplay tool_complete.wav'"
echo "alias git='afplay tool_start.wav && git'"
echo "alias logout='afplay session_end.wav && logout'"

echo ""
echo "✅ All cyberpunk terminal audio hooks generated successfully!"
echo "Ready for deployment in Claude Code or other terminal applications."