# Claude Code Audio Hooks Sound Library

A complete set of professional audio files designed specifically for Claude Code UI event hooks, featuring terminal-native, cyberpunk-inspired sounds that make your coding experience feel like you're living inside the command line.

## 🎵 Overview

This repository contains 10 high-quality `.wav` audio files optimized for Claude Code's hook system. Each sound provides subtle, non-intrusive feedback for different UI events, creating an immersive coding experience inspired by Watch Dogs 2's cyberpunk aesthetic and the feeling of being "trapped in vim."

## 📦 Audio Files

### Session Management
- **`session_start.wav`** (1.5s) - Terminal awakening sound, like SSH-ing into your own consciousness
  - Warm C major chord with welcoming tone
  - Modem handshake pattern transitioning to prompt ready
  - ASCII pattern: `>_ connecting... [████████] ready`

- **`session_end.wav`** (1.6s) - Graceful logout, connection closed
  - 5-tone descending melodic sequence (C5 → G4 → E4 → D4 → C4)
  - Nostalgic Tron-esque terminal shutdown feel
  - ASCII pattern: `logout\n[Process completed successfully]`

### Tool Execution
- **`tool_start.wav`** (0.4s) - Process spawning, threads initializing
  - Brief rising activation tone
  - Bit-crushed CPU cycle hum
  - ASCII pattern: `[>    ] initializing...`

- **`tool_complete.wav`** (0.8s) - Exit code 0
  - Two-tone success confirmation
  - Memory deallocation sweep
  - ASCII pattern: `[████] ✓ complete`

### Communication Events
- **`prompt_submit.wav`** (0.1s) - Keystroke echoes in the void
  - Quick click/submit sound (`:w` in vim)
  - Failed command → despair → confusion sequence
  - ASCII pattern: `:wq` but you're in insert mode

- **`response_start.wav`** (0.6s) - Data streams beginning to flow
  - Soft notification chime with packet arrival simulation
  - Brown noise through bandpass filter
  - ASCII pattern: `<<<< receiving data`

- **`response_end.wav`** (0.7s) - Buffer flush, output complete
  - Gentle completion fade with EOF indication
  - Descending bit pattern
  - ASCII pattern: `>>>> transmission complete`

### Special Events
- **`subagent_done.wav`** (1.0s) - Child process returns to parent
  - Triumphant achievement chord
  - Successful compilation celebration
  - Process completion confirmation

- **`precompact_warning.wav`** (1.2s) - Memory pressure, swap approaching
  - Attention-getting warning tone
  - Oscillating low frequency alarm
  - ASCII pattern: `[WARNING: 95% memory]`

- **`notification.wav`** (0.8s) - System interrupt, SIGINFO
  - Balanced general alert
  - Modern take on terminal bell (^G)
  - ASCII pattern: `!!! [ALERT] !!!`

## 🔧 Integration with Claude Code

### 🚀 Quick Start (One-Liner)

**The fastest way to get started:**

```bash
curl -sSL https://raw.githubusercontent.com/AutumnsGrove/ClaudeCodeSounds/main/web-install.sh | bash
```

This will:
- Clone the repository to `~/.claude-sounds`
- Build the interactive configurator
- Optionally add a `claude-sounds` command to your shell

Then just run `claude-sounds` (or `cd ~/.claude-sounds && ./claude-sounds-config`) to configure your themes!

### Manual Setup

If you prefer to set up manually:

1. **Clone or download this repository**
   ```bash
   git clone https://github.com/AutumnsGrove/ClaudeCodeSounds.git
   cd ClaudeCodeSounds
   ```

2. **Use the interactive configurator (recommended)**
   ```bash
   go run main.go
   # Or: ./install.sh for a full installation
   ```

3. **Or manually configure hooks**

   Copy the example configuration from `claude-code-config-example.json` and add it to your Claude Code settings:

   ```json
   {
     "hooks": {
       "session_start": "afplay ~/ClaudeCodeSounds/session_start.wav &",
       "session_end": "afplay ~/ClaudeCodeSounds/session_end.wav &",
       "tool_start": "afplay ~/ClaudeCodeSounds/tool_start.wav &",
       "tool_complete": "afplay ~/ClaudeCodeSounds/tool_complete.wav &",
       "prompt_submit": "afplay ~/ClaudeCodeSounds/prompt_submit.wav &",
       "response_start": "afplay ~/ClaudeCodeSounds/response_start.wav &",
       "response_end": "afplay ~/ClaudeCodeSounds/response_end.wav &",
       "subagent_done": "afplay ~/ClaudeCodeSounds/subagent_done.wav &",
       "precompact_warning": "afplay ~/ClaudeCodeSounds/precompact_warning.wav &",
       "notification": "afplay ~/ClaudeCodeSounds/notification.wav &"
     }
   }
   ```

   **Note**: Replace `afplay` with your system's audio player:
   - macOS: `afplay`
   - Linux: `aplay` or `paplay`
   - Windows: `powershell -c (New-Object Media.SoundPlayer 'path\to\sound.wav').PlaySync();`

### 🎨 Interactive Configurator (Recommended!)

**NEW**: We now provide a beautiful TUI (Terminal User Interface) configurator that makes setup a breeze!

The configurator will:
- ✨ Let you browse and preview all sound themes interactively
- 🎵 Play preview sounds so you can hear before you apply
- 🔍 Auto-detect your system's audio player
- 💾 Automatically backup your existing settings
- 🛡️ Safely update only sound hooks (preserves your other hooks!)

**Quick Start:**

```bash
# From the ClaudeCodeSounds directory
go run main.go

# Or build and run:
go build -o claude-sounds-config main.go
./claude-sounds-config
```

**Controls:**
- ↑/↓ - Navigate themes
- P or Space - Preview the theme (plays session_start.wav)
- Enter - Select theme (shows confirmation dialog)
- Y - Confirm and save changes
- N/ESC - Cancel and return to list
- Q - Quit without saving

See [CONFIGURATOR.md](CONFIGURATOR.md) for detailed documentation.

### Customization

The `extras/` directory contains alternative sounds you can use:
- `CrashMacII.wav` - Retro Mac system crash sound
- `Flute.wav` - Gentle flute melody
- `Item Get.wav` - Achievement/success sound
- `Item Throw.wav` - Quick action sound
- `Secret Unlocked.wav` - Special event notification

#### Alternative Sound Suites

- **`prompt3style/`** - More intense cyberpunk styling with enhanced digital grit
- **`retro-terminal/`** - Classic 80s computing aesthetic with clean sine waves and nostalgic charm
- **`drift/`** - Ambient water-inspired soundscape for transcendent flow state and deep focus
- **`void/`** - Cosmic liminal soundscape with deep space drones and stellar resonance (NEW!)

## 📊 Technical Specifications

All audio files meet professional standards:

- **Format**: WAV (RIFF/WAVE, uncompressed PCM)
- **Sample Rate**: 44.1 kHz (CD quality)
- **Bit Depth**: 16-bit signed little-endian
- **Channels**: Mono (1 channel)
- **Fade Effects**: Gentle fade-in/out to prevent audio clicks
- **Volume**: Balanced at 0.3-0.7 for non-intrusive use
- **Total Size**: ~766 KB for all 10 files

### File Sizes
- Largest: `session_end.wav` (190 KB)
- Smallest: `prompt_submit.wav` (17 KB)
- Average: ~77 KB per file

## 🎨 Sound Design Philosophy

### Terminal-Native Aesthetic
These sounds are designed to feel like you're experiencing audio from within the terminal itself - as if the code is singing, data packets are dancing, and you're living inside the digital realm.

### Cyberpunk Characteristics
- **Sample Rate Degradation**: 4000-11025 Hz for that "through the modem" feel
- **Bit Crushing**: 4-8 bit depth for digital grit
- **Pink/Brown Noise**: Data stream ambience
- **Echo/Delay**: Terminal latency simulation
- **Frequency Modulation**: Carrier wave aesthetics

### ASCII-to-Audio Translation
Each sound was conceptualized by mapping ASCII art patterns to audio frequencies:
- Dense characters (█▓▒░) = lower frequencies (100-400 Hz)
- Sparse characters (. · ˙) = higher frequencies (800-1200 Hz)
- Special chars (!@#$%) = glitch effects
- Whitespace = silence or reverb

## 📖 Generation Documentation

This repository includes comprehensive documentation on how these sounds were created:

- **`METAPROMPT3.md`** - Terminal Native Edition metaprompt
  - Complete ASCII-to-audio translation system
  - FFmpeg command templates and examples
  - Cyberpunk audio texture specifications
  - Watch Dogs 2 inspired elements

- **`SESSION_END_GENERATION_PROMPT.md`** - Detailed session_end.wav generation guide
  - Musical pattern specifications
  - Multiple generation approaches
  - Validation and quality criteria

- **`METAPROMPT2.md`** - Earlier iteration documenting the evolution of the sound design

### Generation Tools
All sounds were generated using **FFmpeg 7.1.1** with specialized synthesis commands involving:
- `sine` wave generation
- `anoisesrc` for digital noise textures
- `acrusher` for bit-crushing effects
- `asetrate` for sample rate manipulation
- Complex filter chains for layered effects

See the `archive/` directory for the original ffmpeg-generated versions before final processing.

## 🚀 Usage Examples

### Basic Terminal Integration
```bash
# Bind sounds to common commands
alias vim='afplay ~/ClaudeCodeSounds/session_start.wav && vim'
alias git='afplay ~/ClaudeCodeSounds/tool_start.wav && git'
```

### Claude Code Hook Configuration
Place hooks in your Claude Code settings file (typically `~/.claude/config.json` or similar):

```json
{
  "audioHooks": {
    "enabled": true,
    "soundDirectory": "~/ClaudeCodeSounds",
    "hooks": {
      "session_start": "session_start.wav",
      "session_end": "session_end.wav",
      "tool_start": "tool_start.wav",
      "tool_complete": "tool_complete.wav",
      "prompt_submit": "prompt_submit.wav",
      "response_start": "response_start.wav",
      "response_end": "response_end.wav",
      "subagent_done": "subagent_done.wav",
      "precompact_warning": "precompact_warning.wav",
      "notification": "notification.wav"
    }
  }
}
```

## 🎯 Quality Assurance

Each sound has been verified for:
- ✅ Correct duration and timing
- ✅ Proper sample rate (44.1 kHz)
- ✅ Appropriate volume levels (non-intrusive)
- ✅ Clean fade-in/fade-out (no clicks or pops)
- ✅ Mono channel format
- ✅ Low latency playback optimization

## 📂 Repository Structure

```
ClaudeCodeSounds/
├── *.wav                          # Main audio files (10 hooks)
├── README.md                      # This file
├── LICENSE                        # MIT License
├── CONFIGURATOR.md                # Configurator documentation
├── main.go                        # TUI configurator source code
├── go.mod                         # Go module definition
├── go.sum                         # Go dependencies
├── claude-sounds-config           # Compiled configurator binary (after build)
├── claude-code-config-example.json # Example hook configuration
├── generate_retro_sounds.py       # Python script for retro suite generation
├── generate_drift_sounds.py       # Python script for drift suite generation
├── generate_void_sounds.py        # Python script for void suite generation
├── extras/                        # Alternative sound files
├── prompt3style/                  # Alternative cyberpunk-intense set
├── retro-terminal/                # Classic 80s computing sound suite
├── drift/                         # Ambient water/flow sound suite
├── void/                          # Cosmic liminal space sound suite
├── archive/                       # Original ffmpeg-generated versions
└── docs/                          # Generation documentation
    ├── METAPROMPT3.md
    ├── METAPROMPT2.md
    └── SESSION_END_GENERATION_PROMPT.md
```

## 🤝 Contributing

Feel free to:
- Create your own sound variations using the generation metaprompts
- Submit alternative sounds for different aesthetic preferences
- Improve the FFmpeg generation commands
- Add support for other audio players/platforms

## 📜 License

MIT License - See [LICENSE](LICENSE) file for details

## 🙏 Credits

- Generated using Claude Code and FFmpeg 7.1.1
- Sound design inspired by Watch Dogs 2 and terminal aesthetics
- ASCII-to-audio translation concept
- Created with love for developers who live in the command line

---

**Version**: 1.0
**Generated**: September 2025
**Compatibility**: Claude Code 2.0+ hook system
**Platform**: Cross-platform (macOS, Linux, Windows)

For detailed generation methodology and customization guidance, see the documentation in the `docs/` directory.
