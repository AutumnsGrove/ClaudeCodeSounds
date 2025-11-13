# Retro Terminal Sound Suite

A fresh take on Claude Code audio hooks with a classic 80s computing aesthetic.

## Theme

Inspired by the golden age of personal computing - Apple II, Commodore 64, and early Unix terminals. These sounds feature clean sine and square waves that evoke the simplicity and charm of vintage computer systems.

## Sound Design Philosophy

Unlike the cyberpunk-heavy "Terminal Native" suite, this collection embraces:
- **Clean waveforms**: Pure sine and square waves
- **Musical progression**: Melodic sequences based on musical notes
- **Nostalgic charm**: Classic computer beeps and boops
- **Gentle feedback**: Non-intrusive, pleasant tones

## Included Sounds

### Session Management
- **session_start.wav** - Ascending C major arpeggio (C5-E5-G5-C6) - like a classic boot sequence
- **session_end.wav** - Descending shutdown sequence (C6-G5-E5-C5) - graceful power-down

### Tool Execution
- **tool_start.wav** - Brief rising square wave beep - process initialization
- **tool_complete.wav** - Two-tone confirmation (D5-G5) - task success

### Communication Events
- **prompt_submit.wav** - Quick keystroke click - command entered
- **response_start.wav** - Soft ascending chime (C5-E5) - data incoming
- **response_end.wav** - Gentle descending tone (E5-C5) - output complete

### Special Events
- **subagent_done.wav** - C major chord (C5+E5+G5) - achievement unlocked
- **precompact_warning.wav** - Oscillating alert tones - attention needed
- **notification.wav** - Classic 1000Hz terminal bell - general notification

## Technical Specifications

- **Format**: WAV (PCM)
- **Sample Rate**: 44.1 kHz
- **Bit Depth**: 16-bit
- **Channels**: Mono
- **Fade**: Smooth in/out to prevent clicks
- **Total Size**: ~370 KB

## Installation

Use these sounds just like the main suite. In your Claude Code configuration:

```json
{
  "hooks": {
    "session_start": "afplay ~/ClaudeCodeSounds/retro-terminal/session_start.wav &",
    "session_end": "afplay ~/ClaudeCodeSounds/retro-terminal/session_end.wav &",
    "tool_start": "afplay ~/ClaudeCodeSounds/retro-terminal/tool_start.wav &",
    "tool_complete": "afplay ~/ClaudeCodeSounds/retro-terminal/tool_complete.wav &",
    "prompt_submit": "afplay ~/ClaudeCodeSounds/retro-terminal/prompt_submit.wav &",
    "response_start": "afplay ~/ClaudeCodeSounds/retro-terminal/response_start.wav &",
    "response_end": "afplay ~/ClaudeCodeSounds/retro-terminal/response_end.wav &",
    "subagent_done": "afplay ~/ClaudeCodeSounds/retro-terminal/subagent_done.wav &",
    "precompact_warning": "afplay ~/ClaudeCodeSounds/retro-terminal/precompact_warning.wav &",
    "notification": "afplay ~/ClaudeCodeSounds/retro-terminal/notification.wav &"
  }
}
```

**Platform-specific players:**
- macOS: `afplay`
- Linux: `aplay` or `paplay`
- Windows: Use PowerShell Media.SoundPlayer

## Generation

These sounds were generated using Python's built-in `wave` module with pure sine and square wave synthesis. See `generate_retro_sounds.py` in the repository root for the complete generation script.

## Comparison to Other Suites

| Suite | Aesthetic | Complexity | Vibe |
|-------|-----------|------------|------|
| **Main Suite** | Cyberpunk/Modem | High | Watch Dogs 2 hacker |
| **Prompt3Style** | Intense Cyberpunk | Very High | Digital dystopia |
| **Retro Terminal** | Classic Computing | Low | 80s nostalgia |

Mix and match sounds from different suites to create your perfect audio experience!

---

*Part of the ClaudeCodeSounds collection*
