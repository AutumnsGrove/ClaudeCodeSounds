# Session End Sound Generation Prompt

## Objective
Generate a single audio file `session_end.wav` - a nostalgic, Tron-esque terminal shutdown sound with a descending 5-tone melodic sequence.

## Target Specifications

### Audio Characteristics
- **Character**: Nostalgic, Tron-esque terminal logging off
- **Melody**: Descending 5-tone sequence
- **Duration**: ~2.2 seconds total
- **Volume**: 0.3 (3/10 volume level - subtle but present)
- **Complexity**: Complex multi-tone sequence, NOT a single tone

### Technical Requirements
- **Format**: WAV (RIFF/WAVE format)
- **Sample Rate**: 44100 Hz
- **Bit Depth**: 16-bit PCM signed little-endian
- **Channels**: Mono (1 channel)
- **Fade In**: 0.1 seconds (gentle)
- **Fade Out**: 0.1 seconds (gentle)

## Musical Pattern

The sound should consist of **5 distinct sequential tones** descending from high to low:

1. **Tone 1**: C5 (523.25 Hz) - Duration: 0.4 seconds
2. **Tone 2**: G4 (392.00 Hz) - Duration: 0.4 seconds
3. **Tone 3**: E4 (329.63 Hz) - Duration: 0.4 seconds
4. **Tone 4**: D4 (293.66 Hz) - Duration: 0.4 seconds
5. **Tone 5**: C4 (261.63 Hz) - Duration: 0.6 seconds (extended for finality)

**Total Duration**: 2.2 seconds

## FFmpeg Command Template

```bash
ffmpeg -y \
  -f lavfi -i "sine=frequency=523.25:duration=0.4" \
  -f lavfi -i "sine=frequency=392.00:duration=0.4" \
  -f lavfi -i "sine=frequency=329.63:duration=0.4" \
  -f lavfi -i "sine=frequency=293.66:duration=0.4" \
  -f lavfi -i "sine=frequency=261.63:duration=0.6" \
  -filter_complex "[0:a][1:a][2:a][3:a][4:a]concat=n=5:v=0:a=1,afade=t=in:d=0.1,afade=t=out:d=0.1,volume=0.3" \
  -ar 44100 -ac 1 session_end.wav
```

## Critical Implementation Notes

### MUST HAVE: 5 Distinct Tones
The final audio file **MUST** contain 5 clearly audible descending tones, NOT a single continuous tone. Each tone should be individually distinguishable when played back.

### Validation Steps
After generation, verify:
1. File size is approximately 190KB
2. Duration is 2.2 seconds: `ffprobe session_end.wav`
3. **Play the file and confirm you hear 5 distinct descending tones**
4. If you only hear a single tone, the generation has FAILED

### Alternative Approach (If concat fails)
If the concat method produces a single tone, try generating with explicit silence gaps between tones:

```bash
# Generate individual tone files first
ffmpeg -y -f lavfi -i "sine=frequency=523.25:duration=0.4" -af "afade=t=in:d=0.05,afade=t=out:d=0.05,volume=0.3" -ar 44100 -ac 1 tone1.wav
ffmpeg -y -f lavfi -i "sine=frequency=392.00:duration=0.4" -af "afade=t=in:d=0.05,afade=t=out:d=0.05,volume=0.3" -ar 44100 -ac 1 tone2.wav
ffmpeg -y -f lavfi -i "sine=frequency=329.63:duration=0.4" -af "afade=t=in:d=0.05,afade=t=out:d=0.05,volume=0.3" -ar 44100 -ac 1 tone3.wav
ffmpeg -y -f lavfi -i "sine=frequency=293.66:duration=0.4" -af "afade=t=in:d=0.05,afade=t=out:d=0.05,volume=0.3" -ar 44100 -ac 1 tone4.wav
ffmpeg -y -f lavfi -i "sine=frequency=261.63:duration=0.6" -af "afade=t=in:d=0.05,afade=t=out:d=0.1,volume=0.3" -ar 44100 -ac 1 tone5.wav

# Create file list
echo "file 'tone1.wav'" > filelist.txt
echo "file 'tone2.wav'" >> filelist.txt
echo "file 'tone3.wav'" >> filelist.txt
echo "file 'tone4.wav'" >> filelist.txt
echo "file 'tone5.wav'" >> filelist.txt

# Concatenate using file demuxer
ffmpeg -y -f concat -safe 0 -i filelist.txt -c copy session_end.wav

# Cleanup
rm tone1.wav tone2.wav tone3.wav tone4.wav tone5.wav filelist.txt
```

### Alternative Approach 2: Using amerge with delays
```bash
ffmpeg -y \
  -f lavfi -i "sine=frequency=523.25:duration=0.4,adelay=0|0" \
  -f lavfi -i "sine=frequency=392.00:duration=0.4,adelay=400|400" \
  -f lavfi -i "sine=frequency=329.63:duration=0.4,adelay=800|800" \
  -f lavfi -i "sine=frequency=293.66:duration=0.4,adelay=1200|1200" \
  -f lavfi -i "sine=frequency=261.63:duration=0.6,adelay=1600|1600" \
  -filter_complex "[0:a][1:a][2:a][3:a][4:a]amix=inputs=5:duration=longest,afade=t=in:d=0.1,afade=t=out:d=0.1,volume=0.3" \
  -ar 44100 -ac 1 session_end.wav
```

## Expected Output

When you play `session_end.wav`, you should hear:
- A high C5 tone (descending start)
- Followed by G4 (stepping down)
- Then E4 (continuing descent)
- Then D4 (approaching home)
- Finally C4 held longer (terminal shutdown complete)

This creates a nostalgic, retro-computer shutdown effect reminiscent of classic Tron or 80s terminal interfaces.

## Success Criteria

✅ File exists and is ~190KB
✅ Duration is 2.2 seconds
✅ File plays without errors
✅ **You can hear 5 distinct descending tones when played**
✅ Volume is subtle (3/10 level)
✅ Tron-esque nostalgic feel achieved

## Failure Mode

❌ If file plays as a single continuous tone
❌ If duration is very short (<1 second)
❌ If file is corrupted or won't play

→ Try one of the alternative approaches above

## Context

This file is part of the Claude Code 2.0 audio hook system. The session_end.wav sound plays when a Claude Code session terminates, providing auditory feedback with a nostalgic, retro-computing aesthetic. The 5-tone descending pattern evokes the feeling of a system gracefully powering down.

## Working Directory
`/Users/mini/Documents/scripts/sounds/`

---

**Version**: 1.0
**Created**: 2025-09-29
**Purpose**: Standalone prompt for generating session_end.wav in a fresh Claude Code session