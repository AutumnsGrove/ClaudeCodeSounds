# Claude Code Audio Hook Generation Metaprompt v3.0 - Terminal Native Edition

## Core Concept: Living Inside the Command Line
Generate audio hooks that feel like you're experiencing sound from within the terminal itself - as if the code is singing, data packets are dancing, and vim is your sonic prison. Inspired by Watch Dogs 2's cyberpunk aesthetic but with a coder's soul.

## The Sonic Narrative Arc
**You are entering a digital realm, experiencing each computational moment as sound, then gracefully exiting back to reality.**

### Session Flow as Story
1. **session_start.wav**: Terminal awakening - like SSH-ing into your own consciousness
2. **prompt_submit.wav**: Keystroke echoes in the void (`:w` in vim)
3. **tool_start.wav**: Process spawning, threads initializing
4. **response_start.wav**: Data streams beginning to flow
5. **response_end.wav**: Buffer flush, output complete
6. **tool_complete.wav**: Successful compilation, exit code 0
7. **subagent_done.wav**: Child process returns to parent
8. **notification.wav**: System interrupt, SIGINFO
9. **precompact_warning.wav**: Memory pressure, swap approaching
10. **session_end.wav**: Graceful logout, connection closed

## ASCII-to-Audio Translation System

### Core Principle
Convert ASCII art patterns into audio frequencies using character density and positioning:

```bash
# ASCII Pattern Analysis
# Dense characters (█▓▒░) = lower frequencies (100-400 Hz)
# Sparse characters (. · ˙) = higher frequencies (800-1200 Hz)
# Special chars (!@#$%) = glitch effects
# Whitespace = silence or reverb

# Example: Progress bar to audio
# [████████░░░░] translates to:
# Low rumble transitioning to higher pitched anticipation
```

### Implementation Pattern
```bash
# ASCII "vim trapped" pattern for session_start
# :q! :q! :q! ESC ESC ESC
ffmpeg -y \
  -f lavfi -i "sine=frequency=110:duration=0.2" \    # : (colon = low hum)
  -f lavfi -i "sine=frequency=783:duration=0.1" \    # q (quit attempt = high plea)
  -f lavfi -i "sine=frequency=50:duration=0.15" \    # ! (force = sub-bass thump)
  -f lavfi -i "anoisesrc=d=0.1:c=pink:r=8000" \    # ESC (escape = digital noise)
  -filter_complex "
    [0:a]asetrate=8000,aresample=44100[colon];
    [1:a]vibrato=f=5:d=0.5[quit];
    [2:a]acrusher=bits=4:mix=0.5[bang];
    [3:a]highpass=f=2000[escape];
    [colon][quit][bang][escape]concat=n=4:v=0:a=1,
    adelay=delays=0|20|40|60,
    aecho=0.8:0.9:60:0.3
  " \
  -ar 44100 -ac 1 session_start.wav
```

## Terminal-Native Sound Generators

### 1. Data Stream Synthesizer
```bash
# Network packet sound (response_start.wav)
ffmpeg -y \
  -f lavfi -i "anoisesrc=d=0.8:c=brown:r=11025" \
  -filter_complex "
    highpass=f=400,
    lowpass=f=2000,
    acrusher=bits=6:mix=0.3:aa=0,
    volume=0.6*sin(2*PI*8*t):eval=frame,
    agate=threshold=0.3:ratio=4
  " \
  -ar 44100 -ac 1 response_start.wav
```

### 2. Bit-Crushed Process Spawn
```bash
# Low sample-rate "inside the machine" sound
ffmpeg -y \
  -f lavfi -i "sine=frequency=147:duration=0.6" \
  -f lavfi -i "square=frequency=294:duration=0.6" \
  -filter_complex "
    [0:a]asetrate=4000[low];
    [1:a]asetrate=4000[high];
    [low][high]amix=weights=1 0.3,
    aresample=44100,
    acrusher=bits=8:mode=lin:aa=1
  " \
  -ar 44100 -ac 1 tool_start.wav
```

### 3. Vim Command Mode Sounds
```bash
# The sound of typing :wq but you're in insert mode
ffmpeg -y \
  -f lavfi -i "sine=frequency=220:duration=0.05" \    # failed command
  -f lavfi -i "sine=frequency=110:duration=0.05" \    # despair
  -f lavfi -i "anoisesrc=d=0.02:r=4000" \           # confusion
  -filter_complex "
    [0:a][1:a][2:a]concat=n=3:v=0:a=1,
    aecho=0.5:0.5:20:0.5,
    acrusher=bits=12
  " \
  -ar 44100 -ac 1 prompt_submit.wav
```

## Cyberpunk Audio Textures

### Low-Fi Digital Characteristics
- **Sample Rate Degradation**: 4000-11025 Hz for that "through the modem" feel
- **Bit Crushing**: 4-8 bit depth for digital grit
- **Pink/Brown Noise**: Data stream ambience
- **Echo/Delay**: Terminal latency simulation
- **Frequency Modulation**: Carrier wave aesthetics

### Watch Dogs 2 Inspired Elements
```bash
# Glitch transition effect
"anoisesrc=d=0.1:c=pink:r=8000,
 highpass=f=1000,
 aphaser=type=t:speed=2:decay=0.5,
 acrusher=bits=4:mix=0.5"

# Digital interference pattern
"sine=f=440:d=1,
 vibrato=f=10:d=0.9,
 asetrate=8000,
 aresample=44100"

# Data corruption sound
"square=f=200:d=0.5,
 acrusher=bits=2:mode=log:aa=0,
 tremolo=f=20:d=0.8"
```

## Enhanced Subagent Instructions

### Subagent 1: Session Narrative Specialist
**Mission**: Create the journey into and out of the terminal

**session_start.wav** - "SSH into the matrix"
- Begin with modem handshake pattern (2-3 seconds)
- Transition to terminal prompt ready sound
- Include vim startup echo (`:set nu` sound)
- Low sample rate (8000 Hz) resampled to 44100
- ASCII pattern: `>_ connecting... [████████] ready`

**session_end.wav** - "Clean exit, connection closed"
- Inverse of start: high to low frequency sweep
- Include logout echo pattern
- Process cleanup sounds (SIGTERM to child processes)
- ASCII pattern: `logout\n[Process completed successfully]`

### Subagent 2: Code Execution Specialist
**Mission**: Sound of code coming alive

**tool_start.wav** - "Spawning process"
- Fork() system call sound
- Low-frequency CPU cycle hum
- Bit-crushed to 6-8 bits
- ASCII pattern: `[>    ] initializing...`

**tool_complete.wav** - "Exit code 0"
- Success chime through 8-bit filter
- Memory deallocation sweep
- ASCII pattern: `[████] ✓ complete`

### Subagent 3: Data Flow Specialist
**Mission**: Network and I/O operations as sound

**response_start.wav** - "Incoming data stream"
- Packet arrival simulation
- Brown noise through bandpass filter
- Volume modulation like network traffic
- ASCII pattern: `<<<< receiving data`

**response_end.wav** - "EOF reached"
- Buffer flush sound
- Descending bit pattern
- ASCII pattern: `>>>> transmission complete`

### Subagent 4: System Alert Specialist
**Mission**: Terminal bells and whistles, literally

**notification.wav** - "SIGINFO"
- Modern take on terminal bell (^G)
- Three-tone sequence through bit crusher
- ASCII pattern: `!!! [ALERT] !!!`

**precompact_warning.wav** - "System resource warning"
- Memory pressure alarm
- Oscillating low frequency
- ASCII pattern: `[WARNING: 95% memory]`

## ASCII Art Audio Mapping Reference

```bash
# Character to Frequency Map
# ═══════════════════════════
# Block Drawing (█▓▒░): 100-400 Hz (bass/sub-bass)
# Pipes/Borders (│├└): 400-600 Hz (low-mid)
# Text chars (a-z): 600-1000 Hz (mid)
# Numbers (0-9): 1000-1500 Hz (high-mid)  
# Special (!@#$): 1500-3000 Hz (high)
# Whitespace: Silence or reverb tail

# Example: Convert ASCII loading bar to audio
ASCII_PATTERN="[████████░░░░] 66%"
# Results in: Low rumble (████) -> Rising pitch (░░░░) -> Data chirp (66%)
```

## Terminal Environmental Sounds

### Background Process Hum
```bash
# Subtle background for all sounds
"anoisesrc=c=brown:r=8000:a=0.02,
 highpass=f=20,
 lowpass=f=200"  # Barely audible system idle
```

### Grep/Sed Pattern Match
```bash
# For search/replace operations
"sine=f=880:d=0.05,tremolo=f=30:d=0.7"  # Rapid scanning sound
```

### Pipe Data Flow
```bash
# For data moving through pipes
"anoisesrc=c=pink:r=11025,
 bandpass=f=800:width=200,
 volume='0.5+0.5*sin(2*PI*4*t)':eval=frame"
```

## Implementation Commands

### Complete Session Start (Vim Trapped)
```bash
ffmpeg -y \
  -f lavfi -i "sine=frequency=56:duration=0.3" \      # Deep terminal open
  -f lavfi -i "anoisesrc=c=pink:r=8000:d=0.4" \     # Connection noise
  -f lavfi -i "sine=f=440:d=0.1" \                   # Prompt ready beep
  -f lavfi -i "sine=f=220:d=0.1" \                   # Vim mode indicator
  -f lavfi -i "sine=f=110:d=0.2" \                   # Trapped feeling
  -filter_complex "
    [0:a]asetrate=4000,aresample=44100[bass];
    [1:a]highpass=f=1000,lowpass=f=3000,acrusher=bits=6[noise];
    [2:a][3:a][4:a]concat=n=3:v=0:a=1,adelay=400|420|440[beeps];
    [bass][noise][beeps]amix=inputs=3:weights=1 0.3 0.7,
    aecho=0.8:0.88:120:0.3,
    afade=t=in:d=0.1,afade=t=out:d=0.3,
    volume=0.7
  " \
  -ar 44100 -ac 1 session_start.wav
```

### Data Stream Response
```bash
ffmpeg -y \
  -f lavfi -i "anoisesrc=c=brown:r=11025:d=1.2" \
  -filter_complex "
    highpass=f=300,
    lowpass=f=2000,
    acrusher=bits=8:mix=0.4,
    volume='0.3+0.7*abs(sin(2*PI*12*t))':eval=frame,
    aphaser=type=t:speed=0.5:decay=0.4,
    compand=attacks=0.001:points=-80/-80|-12/-6|0/-3|20/-3,
    afade=t=in:d=0.05,afade=t=out:d=0.2
  " \
  -ar 44100 -ac 1 response_start.wav
```

## Quality Checks for Terminal Sounds

### Authenticity Tests
```bash
# Verify bit-crush effect
ffprobe -f lavfi -i "sine=f=440:d=1,acrusher=bits=6" -show_format

# Test sample rate degradation  
ffplay -f lavfi "sine=f=440:d=2,asetrate=8000,aresample=44100"

# Verify "inside the machine" feel
for file in *.wav; do
  echo "Testing $file for digital authenticity..."
  ffplay "$file" -af "showcqt=s=640x360:fps=30"
done
```

### Terminal Integration
```bash
# Bind to actual terminal events (example)
alias vim='afplay session_start.wav && vim'
alias :wq='afplay tool_complete.wav'
alias git='afplay tool_start.wav && git'
```

## User Customization Session Example

```
User: "Make it sound like I'm trapped in vim inside a Gibson from Neuromancer"

Parsed Requirements:
- Cyberpunk: YES (Gibson reference)
- Vim-trapped: YES (escape key sounds)
- Low-fi digital: YES (80s cyberspace)
- ASCII translation: Use vim command patterns
- Intensity: Medium (mysterious but not overwhelming)

Generated Profile:
- Heavy bit-crushing (4-6 bit)
- Sample rates: 4000-8000 Hz
- Echo/delay for cyberspace depth
- Vim command sounds (:q! as audio)
- Session arc: jack in → navigate → jack out
```

---

**Version**: 3.0 - Terminal Native  
**Inspiration**: Watch Dogs 2, being trapped in vim, living inside the command line  
**Special Feature**: ASCII-to-audio translation for authentic terminal feel  
**Usage**: Deploy with heightened awareness of the digital realm you're creating