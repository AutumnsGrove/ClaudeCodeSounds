#!/usr/bin/env python3
"""
Drift Sound Generator
Generates ambient water/flow-inspired sounds for Claude Code hooks
Theme: Transcendent, meditative, flow state - like drifting through calm water
"""

import wave
import math
import struct
import random

def generate_sine_wave(frequency, duration, sample_rate=44100, amplitude=0.3):
    """Generate a sine wave at the specified frequency"""
    num_samples = int(sample_rate * duration)
    samples = []
    for i in range(num_samples):
        value = amplitude * math.sin(2 * math.pi * frequency * i / sample_rate)
        samples.append(int(value * 32767))
    return samples

def generate_noise(duration, sample_rate=44100, amplitude=0.15):
    """Generate white noise"""
    num_samples = int(sample_rate * duration)
    samples = []
    for _ in range(num_samples):
        value = random.uniform(-amplitude, amplitude)
        samples.append(int(value * 32767))
    return samples

def apply_lowpass_filter(samples, cutoff_ratio=0.1):
    """Simple lowpass filter to create water-like texture from noise"""
    filtered = []
    prev = 0
    for sample in samples:
        filtered_value = prev + cutoff_ratio * (sample - prev)
        filtered.append(int(filtered_value))
        prev = filtered_value
    return filtered

def apply_reverb_decay(samples, decay=0.97):
    """Apply exponential decay for ambient pad effect"""
    decayed = []
    for i, sample in enumerate(samples):
        factor = math.pow(decay, i / 100.0)
        decayed.append(int(sample * factor))
    return decayed

def apply_fade(samples, fade_in_ms=100, fade_out_ms=300, sample_rate=44100):
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

def mix_samples(*sample_lists):
    """Mix multiple sample lists together (same length)"""
    max_len = max(len(s) for s in sample_lists)
    result = [0] * max_len

    for samples in sample_lists:
        for i in range(len(samples)):
            result[i] += samples[i] // len(sample_lists)

    return result

def combine_samples(*sample_lists):
    """Concatenate multiple sample lists"""
    result = []
    for samples in sample_lists:
        result.extend(samples)
    return result

def save_wav(filename, samples, sample_rate=44100):
    """Save samples to a WAV file"""
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)

        # Clamp samples to 16-bit range
        clamped = [max(-32768, min(32767, s)) for s in samples]
        wav_data = struct.pack('<' + ('h' * len(clamped)), *clamped)
        wav_file.writeframes(wav_data)

def generate_water_drop(duration=0.1, sample_rate=44100):
    """Generate a single water drop sound"""
    # Short filtered noise burst with quick decay
    noise = generate_noise(duration, sample_rate, amplitude=0.25)
    filtered = apply_lowpass_filter(noise, cutoff_ratio=0.15)
    decayed = apply_reverb_decay(filtered, decay=0.92)
    return decayed

def generate_ambient_pad(frequency, duration, sample_rate=44100):
    """Generate a soft ambient pad with reverb"""
    # Multiple sine waves slightly detuned for richness
    pad1 = generate_sine_wave(frequency, duration, sample_rate, amplitude=0.15)
    pad2 = generate_sine_wave(frequency * 1.01, duration, sample_rate, amplitude=0.12)
    pad3 = generate_sine_wave(frequency * 0.99, duration, sample_rate, amplitude=0.12)

    mixed = mix_samples(pad1, pad2, pad3)
    decayed = apply_reverb_decay(mixed, decay=0.995)
    return decayed

# Musical notes (frequencies in Hz) - using lower octaves for calm
C3 = 130.81
D3 = 146.83
E3 = 164.81
F3 = 174.61
G3 = 196.00
A3 = 220.00
C4 = 261.63
D4 = 293.66
E4 = 329.63
G4 = 392.00
A4 = 440.00
C5 = 523.25

def generate_session_start():
    """Gentle water drops building into ambient pad - diving into calm water"""
    samples = []

    # Three water drops at increasing intervals
    samples.extend(generate_water_drop(0.15))
    samples.extend([0] * int(44100 * 0.1))  # Silence
    samples.extend(generate_water_drop(0.15))
    samples.extend([0] * int(44100 * 0.08))
    samples.extend(generate_water_drop(0.15))
    samples.extend([0] * int(44100 * 0.05))

    # Soft ambient pad emerges
    samples.extend(generate_ambient_pad(C4, 0.7))

    samples = apply_fade(samples, fade_in_ms=50, fade_out_ms=400)
    save_wav('drift/session_start.wav', samples)
    print("✓ Generated session_start.wav - diving into flow")

def generate_session_end():
    """Descending drops fading into silence - surfacing from depth"""
    samples = []

    # Ambient pad fading
    samples.extend(generate_ambient_pad(A3, 0.4))

    # Spaced water drops descending
    samples.extend(generate_water_drop(0.12))
    samples.extend([0] * int(44100 * 0.15))
    samples.extend(generate_water_drop(0.12))
    samples.extend([0] * int(44100 * 0.2))
    samples.extend(generate_water_drop(0.15))

    # Final silence
    samples.extend([0] * int(44100 * 0.3))

    samples = apply_fade(samples, fade_in_ms=100, fade_out_ms=600)
    save_wav('drift/session_end.wav', samples)
    print("✓ Generated session_end.wav - surfacing gently")

def generate_tool_start():
    """Subtle water ripple with soft chime"""
    noise = generate_noise(0.08, amplitude=0.12)
    filtered = apply_lowpass_filter(noise, cutoff_ratio=0.2)

    chime = generate_sine_wave(E4, 0.08, amplitude=0.15)

    samples = mix_samples(filtered, chime)
    samples = apply_fade(samples, fade_in_ms=20, fade_out_ms=100)
    save_wav('drift/tool_start.wav', samples)
    print("✓ Generated tool_start.wav - gentle ripple")

def generate_tool_complete():
    """Gentle splash with ambient bloom"""
    # Quick filtered noise burst
    noise = generate_noise(0.1, amplitude=0.18)
    filtered = apply_lowpass_filter(noise, cutoff_ratio=0.18)

    # Soft chime blooming
    chime = generate_ambient_pad(G4, 0.4)

    samples = combine_samples(filtered, chime)
    samples = apply_fade(samples, fade_in_ms=10, fade_out_ms=350)
    save_wav('drift/tool_complete.wav', samples)
    print("✓ Generated tool_complete.wav - task dissolves")

def generate_prompt_submit():
    """Single water drop"""
    samples = generate_water_drop(0.08)
    samples = apply_fade(samples, fade_in_ms=5, fade_out_ms=80)
    save_wav('drift/prompt_submit.wav', samples)
    print("✓ Generated prompt_submit.wav - thought released")

def generate_response_start():
    """Soft water flow beginning"""
    # Gentle filtered noise with rising tone
    noise = generate_noise(0.4, amplitude=0.12)
    filtered = apply_lowpass_filter(noise, cutoff_ratio=0.12)

    pad = generate_ambient_pad(C4, 0.4)

    samples = mix_samples(filtered, pad)
    samples = apply_fade(samples, fade_in_ms=150, fade_out_ms=200)
    save_wav('drift/response_start.wav', samples)
    print("✓ Generated response_start.wav - stream begins")

def generate_response_end():
    """Water flow gently fading"""
    noise = generate_noise(0.4, amplitude=0.12)
    filtered = apply_lowpass_filter(noise, cutoff_ratio=0.12)

    pad = generate_ambient_pad(A3, 0.4)

    samples = mix_samples(filtered, pad)
    samples = apply_fade(samples, fade_in_ms=100, fade_out_ms=400)
    save_wav('drift/response_end.wav', samples)
    print("✓ Generated response_end.wav - stream settles")

def generate_subagent_done():
    """Multiple water drops creating ripples, ambient swell"""
    samples = []

    # Cluster of drops
    samples.extend(generate_water_drop(0.1))
    samples.extend([0] * int(44100 * 0.05))
    samples.extend(generate_water_drop(0.1))
    samples.extend([0] * int(44100 * 0.05))
    samples.extend(generate_water_drop(0.1))

    # Ambient swell
    pad = generate_ambient_pad(E4, 0.5)
    samples.extend(pad)

    samples = apply_fade(samples, fade_in_ms=50, fade_out_ms=400)
    save_wav('drift/subagent_done.wav', samples)
    print("✓ Generated subagent_done.wav - ripples of achievement")

def generate_precompact_warning():
    """Rippling wave pattern with gentle alert tone"""
    samples = []

    # Three iterations of wave ripples
    for i in range(3):
        noise = generate_noise(0.2, amplitude=0.18 + i * 0.03)
        filtered = apply_lowpass_filter(noise, cutoff_ratio=0.15)

        # Rising tone to get attention
        tone = generate_sine_wave(A3 + i * 50, 0.2, amplitude=0.15)

        wave_pattern = mix_samples(filtered, tone)
        samples.extend(wave_pattern)

        if i < 2:
            samples.extend([0] * int(44100 * 0.1))

    samples = apply_fade(samples, fade_in_ms=100, fade_out_ms=300)
    save_wav('drift/precompact_warning.wav', samples)
    print("✓ Generated precompact_warning.wav - gentle urgency")

def generate_notification():
    """Crystal-clear water drop with reverb"""
    # Pure tone like a bell
    bell = generate_sine_wave(C5, 0.15, amplitude=0.25)
    decayed = apply_reverb_decay(bell, decay=0.985)

    # Add subtle water texture
    drop = generate_water_drop(0.15)

    samples = mix_samples(decayed, drop)
    samples = apply_fade(samples, fade_in_ms=10, fade_out_ms=350)
    save_wav('drift/notification.wav', samples)
    print("✓ Generated notification.wav - crystal drop")

if __name__ == '__main__':
    print("🌊 Generating Drift sound suite...")
    print("Theme: Ambient water & transcendent flow")
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
    print("📁 Location: drift/")
    print("💧 Enter the flow state...")
