#!/bin/bash
# Compress all WAV files to 22.05kHz, 16-bit mono
# This will reduce file sizes to ~50% while keeping great quality

set -e

echo "🎵 WAV Compression Script"
echo "Converting to: 22.05kHz, 16-bit, mono"
echo ""

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ ffmpeg is not installed"
    echo "Install with:"
    echo "  macOS: brew install ffmpeg"
    echo "  Ubuntu/Debian: sudo apt install ffmpeg"
    exit 1
fi

echo "✅ ffmpeg found: $(ffmpeg -version | head -n1)"
echo ""

# Directories to process
DIRS=(
    "."
    "prompt3style"
    "retro-terminal"
    "drift"
    "void"
)

# Sound files to process
SOUNDS=(
    "session_start"
    "session_end"
    "tool_start"
    "tool_complete"
    "prompt_submit"
    "response_start"
    "response_end"
    "subagent_done"
    "precompact_warning"
    "notification"
)

# Create backup directory with timestamp
BACKUP_DIR="archive/pre-compression-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "📦 Backing up original files to: $BACKUP_DIR"
echo ""

# Function to get file size in human readable format
get_size() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        stat -f%z "$1" 2>/dev/null || echo "0"
    else
        # Linux
        stat -c%s "$1" 2>/dev/null || echo "0"
    fi
}

# Function to format bytes
format_bytes() {
    local bytes=$1
    if [ $bytes -lt 1024 ]; then
        echo "${bytes}B"
    elif [ $bytes -lt 1048576 ]; then
        echo "$((bytes / 1024))KB"
    else
        echo "$((bytes / 1048576))MB"
    fi
}

total_before=0
total_after=0
files_processed=0

# Process each directory
for dir in "${DIRS[@]}"; do
    echo "Processing: $dir/"

    for sound in "${SOUNDS[@]}"; do
        wav_file="$dir/$sound.wav"

        if [ ! -f "$wav_file" ]; then
            echo "  ⚠️  Skipping $wav_file (not found)"
            continue
        fi

        # Get original size
        size_before=$(get_size "$wav_file")
        total_before=$((total_before + size_before))

        # Backup original
        backup_path="$BACKUP_DIR/$dir"
        mkdir -p "$backup_path"
        cp "$wav_file" "$backup_path/$sound.wav"

        # Create temp file
        temp_file="${wav_file}.tmp.wav"

        # Convert: 22.05kHz, 16-bit, mono
        ffmpeg -i "$wav_file" \
            -ar 22050 \
            -ac 1 \
            -sample_fmt s16 \
            -y "$temp_file" \
            -loglevel error 2>&1

        if [ $? -eq 0 ] && [ -f "$temp_file" ]; then
            # Get new size
            size_after=$(get_size "$temp_file")
            total_after=$((total_after + size_after))

            # Replace original
            mv "$temp_file" "$wav_file"

            # Calculate savings
            savings=$((100 - (size_after * 100 / size_before)))

            echo "  ✓ $sound.wav: $(format_bytes $size_before) → $(format_bytes $size_after) (-${savings}%)"
            files_processed=$((files_processed + 1))
        else
            echo "  ❌ Failed to convert $wav_file"
            rm -f "$temp_file"
        fi
    done

    echo ""
done

# Calculate total savings
if [ $total_before -gt 0 ]; then
    total_savings=$((100 - (total_after * 100 / total_before)))

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🎉 Compression Complete!"
    echo ""
    echo "Files processed: $files_processed"
    echo "Total before:    $(format_bytes $total_before)"
    echo "Total after:     $(format_bytes $total_after)"
    echo "Total savings:   $(format_bytes $((total_before - total_after))) (-${total_savings}%)"
    echo ""
    echo "Backups saved to: $BACKUP_DIR"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
    echo "❌ No files were processed"
fi
