# Claude Code Audio Hook Generation Metaprompt v2.0

## Objective
Generate a complete set of customizable audio files for Claude Code UI events using ffmpeg, with specialized subagents handling different sound categories. This metaprompt incorporates user feedback loops and customization variables for personalized audio experiences.

## Customization Variables

Before starting, gather these user preferences:

### Audio Style Preferences
- **Complexity Level**: `simple` | `moderate` | `complex` | `elaborate`
- **Melody Style**: `directional` | `harmonic` | `sequential` | `rhythmic`
- **Duration Preference**: `brief` (0.5-2s) | `standard` (1-3s) | `extended` (3-6s)
- **Volume Level**: `subtle` (0.4-0.6) | `balanced` (0.6-0.8) | `prominent` (0.8-1.0)

### Sound Character Customization
- **Session Start Character**: `welcoming` | `energetic` | `mysterious` | `professional` | `playful`
- **Session End Character**: `peaceful` | `triumphant` | `nostalgic` | `formal` | `gentle`
- **Notification Style**: `unique` | `standard` | `musical` | `minimal` | `attention-grabbing`
- **Tool Feedback**: `responsive` | `confirmatory` | `celebratory` | `subtle`

### Advanced Options
- **Harmonic Complexity**: `single-tones` | `dual-tones` | `chords` | `complex-harmonies`
- **Fade Style**: `quick` (0.05-0.1s) | `gentle` (0.1-0.3s) | `gradual` (0.3-0.6s)
- **Musical Key**: `C-major` | `D-major` | `pentatonic` | `minor-key` | `custom`

## Project Structure
```
sounds/
├── session_start.wav      # Customizable start sequence
├── session_end.wav        # Customizable end sequence
├── tool_start.wav         # Tool activation sound
├── tool_complete.wav      # Tool completion sound
├── prompt_submit.wav      # User input submission
├── response_start.wav     # Claude response begins
├── response_end.wav       # Claude response ends
├── subagent_done.wav      # Subagent task completion
├── precompact_warning.wav # System warning alert
├── notification.wav       # General notifications
└── METAPROMPT2.md        # This file
```

## Implementation Workflow

### Phase 1: Setup and Planning
1. **Create todo list** using TodoWrite tool to track all tasks
2. **Gather user preferences** using the customization variables above
3. **Create sounds directory structure**
4. **Generate base frequency maps** based on musical key preference

### Phase 2: Subagent Deployment Strategy

Deploy **four specialized subagents in parallel** using the Task tool:

#### Subagent 1: Session Management Sounds
**Specialization**: Complex, narrative-driven session start/end sounds
**Custom Variables to Consider**:
- Session start character preference
- Session end character preference
- Duration preference
- Complexity level
- Melody style (especially for directional patterns)

**Enhanced Responsibilities**:
- Create **session_start.wav** with user-specified character and complexity
- Create **session_end.wav** with matching but contrasting emotional arc
- Implement directional melody patterns if requested:
  - Start patterns: `down-up-up-left-right-up` | `ascending-spiral` | `exploration-theme`
  - End patterns: `up-down-down-flat` | `descending-rest` | `conclusion-theme`
- Support extended durations (3-6 seconds) for complex melodies
- Apply harmonic complexity based on user preference

#### Subagent 2: Tool Execution Sounds
**Specialization**: Responsive tool interaction feedback
**Custom Variables to Consider**:
- Tool feedback style preference
- Volume level
- Complexity level (affects number of tones)

**Enhanced Responsibilities**:
- **tool_start.wav**: Quick, responsive activation (0.3-0.8s)
- **tool_complete.wav**: Satisfying completion confirmation (0.5-1.2s)
- Adapt tone characteristics to tool feedback preference
- Support harmonic vs single-tone based on complexity setting

#### Subagent 3: Communication Sounds
**Specialization**: User-Claude interaction audio cues
**Custom Variables to Consider**:
- Notification style preference
- Volume level (especially for non-intrusive communication)
- Duration preference

**Enhanced Responsibilities**:
- **prompt_submit.wav**: User input acknowledgment (0.1-0.3s)
- **response_start.wav**: Claude response initiation (0.4-0.8s)
- **response_end.wav**: Claude response conclusion (0.5-1.0s)
- Create unique notification patterns if requested (3+ note sequences)
- Balance clarity with non-intrusive volume levels

#### Subagent 4: Special Event Sounds
**Specialization**: System alerts and achievement sounds
**Custom Variables to Consider**:
- Notification style for alerts
- Complexity level for celebration sounds
- Volume and attention-grabbing preferences

**Enhanced Responsibilities**:
- **subagent_done.wav**: Achievement/completion celebration (0.8-1.5s)
- **precompact_warning.wav**: Attention-getting system warning (1.0-1.5s)
- **notification.wav**: General purpose alert with customization
- Implement unique notification patterns (avoid standard 2-tone alerts)
- Support attention-grabbing vs subtle alert styles

### Phase 3: Interactive Feedback Loop

**CRITICAL**: Implement user testing and iteration cycle:

1. **Initial Generation**: All subagents generate their assigned files
2. **Bulk Playback Test**: Create command to play all files sequentially:
   ```bash
   for file in session_start.wav session_end.wav tool_start.wav tool_complete.wav prompt_submit.wav response_start.wav response_end.wav subagent_done.wav precompact_warning.wav notification.wav; do
     echo "🔊 Playing: $file"
     afplay "$file"
     sleep 2
   done
   ```
3. **Gather User Feedback**: Ask specifically about:
   - Session start/end complexity and emotional impact
   - Notification uniqueness and recognition
   - Overall length and character satisfaction
   - Volume balance across all files
4. **Targeted Improvements**: Based on feedback, regenerate specific files
5. **Final Validation**: Re-test modified files

### Phase 4: Quality Assurance

**File Validation Commands**:
```bash
# Check all file properties
for file in *.wav; do
  echo "=== $file ==="
  ffprobe -hide_banner -v quiet -show_entries format=duration,size:stream=sample_rate,channels,bits_per_sample "$file"
done

# Verify file integrity
file *.wav

# Test playback individually
for file in *.wav; do
  echo "Testing: $file"
  afplay "$file"
  sleep 1
done
```

## FFmpeg Command Templates

### Dynamic Session Start (Directional Pattern Example)
```bash
# Variables: COMPLEXITY, DURATION_PREF, CHARACTER, FADE_STYLE
# Example: down-up-up-left-right-up pattern
ffmpeg -y \
  -f lavfi -i "sine=frequency=392.00:duration=0.5" \  # down
  -f lavfi -i "sine=frequency=261.63:duration=0.6" \  # base
  -f lavfi -i "sine=frequency=523.25:duration=0.6" \  # up
  -f lavfi -i "sine=frequency=659.25:duration=0.6" \  # up more
  -f lavfi -i "sine=frequency=440.00:duration=0.5" \  # left step
  -f lavfi -i "sine=frequency=493.88:duration=0.5" \  # right step
  -f lavfi -i "sine=frequency=783.99:duration=0.8" \  # final up
  -filter_complex "[0:a][1:a][2:a][3:a][4:a][5:a][6:a]concat=n=7:v=0:a=1,afade=t=in:d=0.2,afade=t=out:d=0.6,volume=0.75" \
  -ar 44100 -ac 1 session_start.wav
```

### Unique Notification (3+ Notes)
```bash
# Variables: NOTIFICATION_STYLE, UNIQUENESS_LEVEL
# Example: 3-note unique pattern
ffmpeg -y \
  -f lavfi -i "sine=frequency=740:duration=0.25" \     # note 1
  -f lavfi -i "sine=frequency=587.33:duration=0.25" \ # note 2
  -f lavfi -i "sine=frequency=659.25:duration=0.35" \ # note 3 (longer)
  -filter_complex "[0:a][1:a][2:a]concat=n=3:v=0:a=1,afade=t=in:d=0.05,afade=t=out:d=0.15,volume=0.7" \
  -ar 44100 -ac 1 notification.wav
```

### Harmonic Complexity Options
```bash
# Single tone (simple)
ffmpeg -f lavfi -i "sine=frequency=440:duration=1.0"

# Dual tone (moderate)
ffmpeg -f lavfi -i "sine=frequency=440:duration=1.0" -f lavfi -i "sine=frequency=554.37:duration=1.0" -filter_complex "[0:a][1:a]amix=inputs=2"

# Chord (complex)
ffmpeg -f lavfi -i "sine=frequency=261.63:duration=1.0" -f lavfi -i "sine=frequency=329.63:duration=1.0" -f lavfi -i "sine=frequency=392.00:duration=1.0" -filter_complex "[0:a][1:a][2:a]amix=inputs=3"
```

## Musical Note Frequency Reference

### C Major Scale (Standard)
- C4: 261.63 Hz
- D4: 293.66 Hz
- E4: 329.63 Hz
- F4: 349.23 Hz
- G4: 392.00 Hz
- A4: 440.00 Hz
- B4: 493.88 Hz
- C5: 523.25 Hz

### Extended Range
- **Lower octave**: Divide by 2 (C3: 130.81 Hz)
- **Higher octave**: Multiply by 2 (C6: 1046.5 Hz)
- **Other keys**: Multiply by appropriate ratios

## User Interaction Scripts

### Feedback Collection Template
```bash
echo "🎵 Audio Hook Testing Session"
echo "Please listen to all sounds and provide feedback on:"
echo "1. Session start complexity and character"
echo "2. Session end emotional satisfaction"
echo "3. Notification uniqueness and clarity"
echo "4. Overall volume balance"
echo "5. Any specific sounds that need adjustment"
echo ""
echo "Playing all sounds with 2-second gaps..."
# [playback loop here]
```

### Regeneration Workflow
```bash
# Example: User wants more complex session start
echo "Regenerating session_start.wav with increased complexity..."
[enhanced ffmpeg command with more notes/harmony]
echo "Testing new version:"
afplay session_start.wav
```

## Quality Standards

### Technical Requirements
- **Sample Rate**: 44.1kHz (always)
- **Format**: WAV uncompressed PCM
- **Bit Depth**: 16-bit signed little-endian
- **Channels**: Mono (1 channel)
- **File Integrity**: RIFF/WAVE format verified

### Audio Design Standards
- **Fade Effects**: Always include gentle fade-in/out to prevent clicks
- **Volume Consistency**: Balance across all files for cohesive experience
- **Duration Appropriateness**: Match duration to function (brief for clicks, extended for sessions)
- **Harmonic Compatibility**: Ensure all sounds work well together
- **Non-Intrusive Design**: Enhance without disrupting workflow

## Troubleshooting

### Common Issues
1. **FFmpeg errors**: Check for proper syntax and file permissions
2. **Audio clicks**: Ensure fade-in/out are applied
3. **Volume imbalance**: Test with consistent playback system
4. **Duration concerns**: Verify against user preferences
5. **File corruption**: Re-run commands if files appear damaged

### Validation Checklist
- [ ] All 10 files generated successfully
- [ ] Each file plays without errors
- [ ] Duration matches user preferences
- [ ] Volume levels are balanced
- [ ] Audio quality meets technical standards
- [ ] User feedback incorporated
- [ ] Files ready for integration

## Integration Notes

Generated files are ready for Claude Code hook system integration:
- Place in appropriate hook configuration directory
- Test with actual UI events before deployment
- Consider user volume settings and system audio
- Provide easy way for users to disable/modify sounds
- Document the customization variables used for future reference

## Example User Customization Session

```
User Input: "I want complex session sounds that are more musical, unique 3-note notifications, and everything should be a bit longer than normal"

Parsed Variables:
- Complexity Level: complex
- Session Start Character: musical
- Session End Character: musical
- Notification Style: unique
- Duration Preference: extended
- Harmonic Complexity: chords

Result: Generate elaborate musical sequences with chord progressions, extended durations, and unique notification patterns.
```

---

**Version**: 2.0
**Created**: Based on interactive development and user feedback loop
**Usage**: Deploy with Task tool using 4 parallel subagents, implement feedback loop, iterate based on user testing