#!/usr/bin/env python3
"""
Generate sounds for new Claude Code hooks: Stop, SubagentStart, PermissionRequest
Creates sounds for all 5 themes
"""

import wave
import math
import struct
import os

def generate_sine_wave(frequency, duration, sample_rate=44100, amplitude=0.5):
    """Generate a sine wave at the specified frequency"""
    num_samples = int(sample_rate * duration)
    samples = []
    for i in range(num_samples):
        value = amplitude * math.sin(2 * math.pi * frequency * i / sample_rate)
        samples.append(int(value * 32767))
    return samples

def generate_square_wave(frequency, duration, sample_rate=44100, amplitude=0.3):
    """Generate a square wave (retro beep sound)"""
    num_samples = int(sample_rate * duration)
    samples = []
    for i in range(num_samples):
        value = amplitude if math.sin(2 * math.pi * frequency * i / sample_rate) > 0 else -amplitude
        samples.append(int(value * 32767))
    return samples

def apply_fade(samples, fade_in_ms=50, fade_out_ms=200, sample_rate=44100):
    """Apply fade in/out to prevent clicks"""
    fade_in_samples = int(sample_rate * fade_in_ms / 1000)
    fade_out_samples = int(sample_rate * fade_out_ms / 1000)

    # Fade in
    for i in range(min(fade_in_samples, len(samples))):
        samples[i] = int(samples[i] * (i / fade_in_samples))

    # Fade out
    start = len(samples) - fade_out_samples
    for i in range(max(0, start), len(samples)):
        factor = 1.0 - ((i - start) / fade_out_samples)
        samples[i] = int(samples[i] * factor)

    return samples

def save_wav(filename, samples, sample_rate=44100):
    """Save samples to a WAV file"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_data = struct.pack('<' + ('h' * len(samples)), *samples)
        wav_file.writeframes(wav_data)

def combine_samples(*sample_lists):
    """Concatenate multiple sample lists"""
    result = []
    for samples in sample_lists:
        result.extend(samples)
    return result

# Musical notes (frequencies in Hz)
C4 = 261.63
D4 = 293.66
E4 = 329.63
F4 = 349.23
G4 = 392.00
A4 = 440.00
B4 = 493.88
C5 = 523.25
D5 = 587.33
E5 = 659.25
F5 = 698.46
G5 = 783.99
A5 = 880.00
C6 = 1046.50

# ============================================================================
# CLASSIC / TERMINAL NATIVE THEME
# ============================================================================

def generate_classic_stop():
    """Main agent completion - definitive conclusion tone"""
    samples = combine_samples(
        generate_sine_wave(E5, 0.12),
        generate_sine_wave(C5, 0.15),
        generate_sine_wave(A4, 0.18)
    )
    samples = apply_fade(samples, fade_out_ms=250)
    save_wav('Classic/stop.wav', samples)

def generate_classic_subagent_start():
    """Subagent initialization - ascending startup tone"""
    samples = combine_samples(
        generate_sine_wave(C4, 0.08),
        generate_sine_wave(E4, 0.08),
        generate_sine_wave(G4, 0.12)
    )
    samples = apply_fade(samples, fade_in_ms=30, fade_out_ms=100)
    save_wav('Classic/subagent_start.wav', samples)

def generate_classic_permission_request():
    """Permission dialog - questioning alert tone"""
    samples = combine_samples(
        generate_sine_wave(G4, 0.15),
        generate_sine_wave(C5, 0.15),
        generate_sine_wave(G4, 0.15)  # Returns to question
    )
    samples = apply_fade(samples)
    save_wav('Classic/permission_request.wav', samples)

# ============================================================================
# RETRO TERMINAL THEME
# ============================================================================

def generate_retro_stop():
    """Retro shutdown tone - descending sequence"""
    samples = combine_samples(
        generate_square_wave(G5, 0.1, amplitude=0.3),
        generate_square_wave(E5, 0.1, amplitude=0.3),
        generate_square_wave(C5, 0.15, amplitude=0.3)
    )
    samples = apply_fade(samples, fade_out_ms=200)
    save_wav('retro-terminal/stop.wav', samples)

def generate_retro_subagent_start():
    """Retro process start - quick ascending beeps"""
    samples = combine_samples(
        generate_square_wave(C4, 0.07, amplitude=0.25),
        generate_square_wave(E4, 0.07, amplitude=0.25),
        generate_square_wave(G4, 0.09, amplitude=0.25)
    )
    samples = apply_fade(samples, fade_in_ms=10, fade_out_ms=80)
    save_wav('retro-terminal/subagent_start.wav', samples)

def generate_retro_permission_request():
    """Retro alert - alternating tones for attention"""
    samples = combine_samples(
        generate_square_wave(A4, 0.12, amplitude=0.3),
        generate_square_wave(E5, 0.12, amplitude=0.3)
    )
    samples = apply_fade(samples)
    save_wav('retro-terminal/permission_request.wav', samples)

# ============================================================================
# PROMPT3STYLE (CYBERPUNK) THEME
# ============================================================================

def generate_cyberpunk_stop():
    """Cyberpunk conclusion - glitchy descending tones"""
    # Mix sine and square for digital grit
    sample_rate = 44100
    duration = 0.4
    num_samples = int(sample_rate * duration)
    samples = []

    for i in range(num_samples):
        t = i / sample_rate
        # Descending frequency sweep
        freq = 600 - (t * 400)  # 600Hz -> 200Hz
        value = 0.4 * math.sin(2 * math.pi * freq * t)
        # Add bit-crushing effect
        if i % 4 == 0:
            value *= 0.7
        samples.append(int(value * 32767))

    samples = apply_fade(samples, fade_out_ms=150)
    save_wav('prompt3style/stop.wav', samples)

def generate_cyberpunk_subagent_start():
    """Cyberpunk process spawn - digital startup"""
    samples = combine_samples(
        generate_square_wave(220, 0.06, amplitude=0.25),
        generate_sine_wave(440, 0.06, amplitude=0.3),
        generate_square_wave(660, 0.08, amplitude=0.25)
    )
    samples = apply_fade(samples, fade_in_ms=20, fade_out_ms=100)
    save_wav('prompt3style/subagent_start.wav', samples)

def generate_cyberpunk_permission_request():
    """Cyberpunk alert - urgent digital notification"""
    samples = []
    for _ in range(2):
        samples.extend(generate_square_wave(800, 0.08, amplitude=0.3))
        samples.extend(generate_sine_wave(1200, 0.08, amplitude=0.25))
    samples = apply_fade(samples)
    save_wav('prompt3style/permission_request.wav', samples)

# ============================================================================
# DRIFT (AMBIENT WATER) THEME
# ============================================================================

def generate_drift_stop():
    """Drift conclusion - gentle wave receding"""
    sample_rate = 44100
    duration = 0.5
    num_samples = int(sample_rate * duration)
    samples = []

    for i in range(num_samples):
        t = i / sample_rate
        # Slowly descending harmonics
        value = (
            0.25 * math.sin(2 * math.pi * 329.63 * t) +  # E4
            0.20 * math.sin(2 * math.pi * 261.63 * t) +  # C4
            0.15 * math.sin(2 * math.pi * 196.00 * t)    # G3
        )
        # Gentle amplitude modulation
        envelope = 1.0 - (t / duration) * 0.7
        samples.append(int(value * envelope * 32767))

    samples = apply_fade(samples, fade_in_ms=80, fade_out_ms=300)
    save_wav('drift/stop.wav', samples)

def generate_drift_subagent_start():
    """Drift initialization - gentle ripple forming"""
    samples = combine_samples(
        generate_sine_wave(C4, 0.15, amplitude=0.3),
        generate_sine_wave(E4, 0.15, amplitude=0.25),
        generate_sine_wave(A4, 0.15, amplitude=0.2)
    )
    samples = apply_fade(samples, fade_in_ms=100, fade_out_ms=150)
    save_wav('drift/subagent_start.wav', samples)

def generate_drift_permission_request():
    """Drift alert - soft but present notification"""
    samples = combine_samples(
        generate_sine_wave(A4, 0.18, amplitude=0.3),
        generate_sine_wave(E5, 0.18, amplitude=0.25)
    )
    samples = apply_fade(samples, fade_in_ms=80, fade_out_ms=200)
    save_wav('drift/permission_request.wav', samples)

# ============================================================================
# VOID (COSMIC LIMINAL) THEME
# ============================================================================

def generate_void_stop():
    """Void conclusion - cosmic resolution"""
    sample_rate = 44100
    duration = 0.6
    num_samples = int(sample_rate * duration)
    samples = []

    for i in range(num_samples):
        t = i / sample_rate
        # Deep cosmic tones
        value = (
            0.2 * math.sin(2 * math.pi * 130.81 * t) +  # C3
            0.15 * math.sin(2 * math.pi * 98.00 * t) +  # G2
            0.1 * math.sin(2 * math.pi * 65.41 * t)     # C2
        )
        # Slow fade out
        envelope = 1.0 - (t / duration) * 0.5
        samples.append(int(value * envelope * 32767))

    samples = apply_fade(samples, fade_in_ms=100, fade_out_ms=400)
    save_wav('void/stop.wav', samples)

def generate_void_subagent_start():
    """Void initialization - emergence from darkness"""
    sample_rate = 44100
    duration = 0.4
    num_samples = int(sample_rate * duration)
    samples = []

    for i in range(num_samples):
        t = i / sample_rate
        # Ascending from deep space
        value = (
            0.25 * math.sin(2 * math.pi * (110 + t * 100) * t) +  # Rising tone
            0.15 * math.sin(2 * math.pi * (55 + t * 50) * t)      # Deep undertone
        )
        samples.append(int(value * 32767))

    samples = apply_fade(samples, fade_in_ms=120, fade_out_ms=150)
    save_wav('void/subagent_start.wav', samples)

def generate_void_permission_request():
    """Void alert - ethereal notification"""
    samples = combine_samples(
        generate_sine_wave(196.00, 0.2, amplitude=0.25),  # G3
        generate_sine_wave(329.63, 0.2, amplitude=0.2),   # E4
        generate_sine_wave(196.00, 0.2, amplitude=0.25)   # Return
    )
    samples = apply_fade(samples, fade_in_ms=100, fade_out_ms=250)
    save_wav('void/permission_request.wav', samples)

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("Generating new hook sounds for all themes...")
    print()

    print("📁 Classic (Terminal Native)")
    generate_classic_stop()
    print("  ✓ stop.wav")
    generate_classic_subagent_start()
    print("  ✓ subagent_start.wav")
    generate_classic_permission_request()
    print("  ✓ permission_request.wav")
    print()

    print("📁 Retro Terminal")
    generate_retro_stop()
    print("  ✓ stop.wav")
    generate_retro_subagent_start()
    print("  ✓ subagent_start.wav")
    generate_retro_permission_request()
    print("  ✓ permission_request.wav")
    print()

    print("📁 Prompt3Style (Cyberpunk)")
    generate_cyberpunk_stop()
    print("  ✓ stop.wav")
    generate_cyberpunk_subagent_start()
    print("  ✓ subagent_start.wav")
    generate_cyberpunk_permission_request()
    print("  ✓ permission_request.wav")
    print()

    print("📁 Drift (Ambient Water)")
    generate_drift_stop()
    print("  ✓ stop.wav")
    generate_drift_subagent_start()
    print("  ✓ subagent_start.wav")
    generate_drift_permission_request()
    print("  ✓ permission_request.wav")
    print()

    print("📁 Void (Cosmic Liminal)")
    generate_void_stop()
    print("  ✓ stop.wav")
    generate_void_subagent_start()
    print("  ✓ subagent_start.wav")
    generate_void_permission_request()
    print("  ✓ permission_request.wav")
    print()

    print("✨ All new hook sounds generated successfully!")
    print("📊 Generated 15 files total (3 sounds × 5 themes)")
    print()
    print("New hooks:")
    print("  • stop.wav - Main agent completion")
    print("  • subagent_start.wav - Subagent initialization")
    print("  • permission_request.wav - Permission dialog alert")
