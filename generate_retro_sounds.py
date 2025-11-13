#!/usr/bin/env python3
"""
Retro Terminal Sound Generator
Generates classic 80s computing-inspired sounds for Claude Code hooks
"""

import wave
import math
import struct
import array

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
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)

        # Convert to bytes
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
C6 = 1046.50

def generate_session_start():
    """Classic boot-up sequence: C5-E5-G5-C6 ascending"""
    samples = combine_samples(
        generate_sine_wave(C5, 0.15),
        generate_sine_wave(E5, 0.15),
        generate_sine_wave(G5, 0.15),
        generate_sine_wave(C6, 0.3)
    )
    samples = apply_fade(samples)
    save_wav('retro-terminal/session_start.wav', samples)
    print("✓ Generated session_start.wav")

def generate_session_end():
    """Classic shutdown sequence: C6-G5-E5-C5 descending"""
    samples = combine_samples(
        generate_sine_wave(C6, 0.2),
        generate_sine_wave(G5, 0.2),
        generate_sine_wave(E5, 0.2),
        generate_sine_wave(C5, 0.4)
    )
    samples = apply_fade(samples, fade_out_ms=300)
    save_wav('retro-terminal/session_end.wav', samples)
    print("✓ Generated session_end.wav")

def generate_tool_start():
    """Brief rising tone - process starting"""
    samples = combine_samples(
        generate_square_wave(220, 0.08),
        generate_square_wave(330, 0.08)
    )
    samples = apply_fade(samples, fade_in_ms=10, fade_out_ms=50)
    save_wav('retro-terminal/tool_start.wav', samples)
    print("✓ Generated tool_start.wav")

def generate_tool_complete():
    """Two-tone success confirmation"""
    samples = combine_samples(
        generate_sine_wave(587.33, 0.12),  # D5
        generate_sine_wave(783.99, 0.18)   # G5
    )
    samples = apply_fade(samples)
    save_wav('retro-terminal/tool_complete.wav', samples)
    print("✓ Generated tool_complete.wav")

def generate_prompt_submit():
    """Quick keystroke click"""
    samples = generate_square_wave(800, 0.05, amplitude=0.25)
    samples = apply_fade(samples, fade_in_ms=5, fade_out_ms=30)
    save_wav('retro-terminal/prompt_submit.wav', samples)
    print("✓ Generated prompt_submit.wav")

def generate_response_start():
    """Soft data incoming chime"""
    samples = combine_samples(
        generate_sine_wave(523.25, 0.15),  # C5
        generate_sine_wave(659.25, 0.15)   # E5
    )
    samples = apply_fade(samples)
    save_wav('retro-terminal/response_start.wav', samples)
    print("✓ Generated response_start.wav")

def generate_response_end():
    """Gentle completion tone"""
    samples = combine_samples(
        generate_sine_wave(659.25, 0.12),  # E5
        generate_sine_wave(523.25, 0.18)   # C5
    )
    samples = apply_fade(samples, fade_out_ms=250)
    save_wav('retro-terminal/response_end.wav', samples)
    print("✓ Generated response_end.wav")

def generate_subagent_done():
    """Triumphant achievement chime: C5-E5-G5 chord"""
    # Create a chord by mixing frequencies
    duration = 0.25
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    samples = []

    for i in range(num_samples):
        # Mix three frequencies
        value = (
            0.2 * math.sin(2 * math.pi * 523.25 * i / sample_rate) +  # C5
            0.2 * math.sin(2 * math.pi * 659.25 * i / sample_rate) +  # E5
            0.2 * math.sin(2 * math.pi * 783.99 * i / sample_rate)    # G5
        )
        samples.append(int(value * 32767))

    samples = apply_fade(samples)
    save_wav('retro-terminal/subagent_done.wav', samples)
    print("✓ Generated subagent_done.wav")

def generate_precompact_warning():
    """Oscillating warning tone"""
    # Alternate between two frequencies
    samples = []
    for _ in range(3):
        samples.extend(generate_square_wave(440, 0.15, amplitude=0.35))
        samples.extend(generate_square_wave(330, 0.15, amplitude=0.35))

    samples = apply_fade(samples)
    save_wav('retro-terminal/precompact_warning.wav', samples)
    print("✓ Generated precompact_warning.wav")

def generate_notification():
    """Classic terminal bell - simple high tone"""
    samples = generate_sine_wave(1000, 0.25, amplitude=0.4)
    samples = apply_fade(samples, fade_out_ms=180)
    save_wav('retro-terminal/notification.wav', samples)
    print("✓ Generated notification.wav")

if __name__ == '__main__':
    print("Generating Retro Terminal sound suite...")
    print()

    generate_session_start()
    generate_session_end()
    generate_tool_start()
    generate_tool_complete()
    generate_prompt_submit()
    generate_response_start()
    generate_response_end()
    generate_subagent_done()
    generate_precompact_warning()
    generate_notification()

    print()
    print("✨ All sounds generated successfully!")
    print("📁 Location: retro-terminal/")
