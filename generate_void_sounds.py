#!/usr/bin/env python3
"""
Void Sound Generator
Generates cosmic, liminal soundscape for Claude Code hooks
Theme: Deep space, transcendent void, stellar resonance, liminal thresholds
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

def generate_deep_drone(frequency, duration, sample_rate=44100, amplitude=0.25):
    """Generate a deep cosmic drone with detuned oscillators for shimmer"""
    num_samples = int(sample_rate * duration)
    samples = []

    for i in range(num_samples):
        # Three detuned oscillators for richness and beating
        osc1 = amplitude * math.sin(2 * math.pi * frequency * i / sample_rate)
        osc2 = amplitude * 0.8 * math.sin(2 * math.pi * frequency * 1.003 * i / sample_rate)
        osc3 = amplitude * 0.6 * math.sin(2 * math.pi * frequency * 0.997 * i / sample_rate)

        # Slow LFO for breathing effect (0.3 Hz)
        lfo = 0.85 + 0.15 * math.sin(2 * math.pi * 0.3 * i / sample_rate)

        value = (osc1 + osc2 + osc3) * lfo
        samples.append(int(value * 32767 / 3))

    return samples

def generate_particle_burst(duration, sample_rate=44100, amplitude=0.2):
    """Generate particle-like sound - filtered noise burst with sparkle"""
    num_samples = int(sample_rate * duration)
    samples = []

    for i in range(num_samples):
        # High frequency noise
        noise = random.uniform(-1, 1)

        # Envelope - quick attack, exponential decay
        envelope = math.exp(-8 * i / num_samples)

        # High-pass characteristic by mixing with derivative
        value = amplitude * noise * envelope
        samples.append(int(value * 32767))

    return samples

def generate_cosmic_shimmer(frequency, duration, sample_rate=44100, amplitude=0.2):
    """Generate shimmering cosmic texture with harmonics"""
    num_samples = int(sample_rate * duration)
    samples = []

    for i in range(num_samples):
        # Fundamental and harmonics
        fundamental = amplitude * math.sin(2 * math.pi * frequency * i / sample_rate)
        harmonic2 = amplitude * 0.5 * math.sin(2 * math.pi * frequency * 2.01 * i / sample_rate)
        harmonic3 = amplitude * 0.3 * math.sin(2 * math.pi * frequency * 3.02 * i / sample_rate)

        # Random phase modulation for shimmer
        phase_mod = 0.1 * math.sin(2 * math.pi * random.uniform(5, 15) * i / sample_rate)

        value = fundamental + harmonic2 + harmonic3 + phase_mod
        samples.append(int(value * 32767))

    return samples

def apply_reverb_decay(samples, decay=0.995):
    """Apply exponential decay for vast space effect"""
    decayed = []
    for i, sample in enumerate(samples):
        factor = math.pow(decay, i / 200.0)
        decayed.append(int(sample * factor))
    return decayed

def apply_fade(samples, fade_in_ms=150, fade_out_ms=400, sample_rate=44100):
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

# Cosmic frequency palette (Hz)
DEEP_VOID = 45      # Sub-bass void resonance
LOW_DRONE = 80      # Low frequency drone
THRESHOLD = 110     # Liminal threshold tone
RESONANCE = 220     # Cosmic resonance
STELLAR = 440       # Stellar frequency
PARTICLE = 880      # High particle frequency
SHIMMER = 1760      # Cosmic shimmer

def generate_session_start():
    """Portal opening - void swelling, particles emerging from darkness"""
    samples = []

    # Deep void drone swelling
    drone = generate_deep_drone(DEEP_VOID, 1.0, amplitude=0.28)

    # Add harmonic resonance
    resonance = generate_sine_wave(THRESHOLD, 0.8, amplitude=0.15)

    # Particle bursts emerging
    particles = []
    particles.extend([0] * int(44100 * 0.6))
    particles.extend(generate_particle_burst(0.15, amplitude=0.18))
    particles.extend([0] * int(44100 * 0.1))
    particles.extend(generate_particle_burst(0.12, amplitude=0.15))

    # Extend lists to match
    while len(resonance) < len(drone):
        resonance.append(0)
    while len(particles) < len(drone):
        particles.append(0)

    samples = mix_samples(drone, resonance, particles)
    samples = apply_fade(samples, fade_in_ms=200, fade_out_ms=500)
    save_wav('void/session_start.wav', samples)
    print("✓ Generated session_start.wav - entering the void")

def generate_session_end():
    """Portal closing - void receding, return to silence"""
    samples = []

    # Particles fading first
    particles = generate_particle_burst(0.2, amplitude=0.16)
    samples.extend(particles)
    samples.extend([0] * int(44100 * 0.2))

    # Drone fading away
    drone = generate_deep_drone(LOW_DRONE, 0.8, amplitude=0.22)

    # Combine
    while len(samples) < len(drone) + len(particles):
        samples.append(0)

    for i, s in enumerate(drone):
        if i + len(particles) < len(samples):
            samples[i + len(particles)] = (samples[i + len(particles)] + s) // 2

    samples = apply_fade(samples, fade_in_ms=100, fade_out_ms=800)
    save_wav('void/session_end.wav', samples)
    print("✓ Generated session_end.wav - void recedes")

def generate_tool_start():
    """Particle activation - subtle cosmic ignition"""
    # Quick particle burst with low resonance
    particle = generate_particle_burst(0.1, amplitude=0.18)
    resonance = generate_sine_wave(RESONANCE, 0.1, amplitude=0.12)

    samples = mix_samples(particle, resonance)
    samples = apply_fade(samples, fade_in_ms=10, fade_out_ms=120)
    save_wav('void/tool_start.wav', samples)
    print("✓ Generated tool_start.wav - particle ignition")

def generate_tool_complete():
    """Resonance bloom - cosmic task completion"""
    # Shimmering resonance with particle release
    shimmer = generate_cosmic_shimmer(STELLAR, 0.5, amplitude=0.2)
    drone = generate_deep_drone(THRESHOLD, 0.5, amplitude=0.15)

    samples = mix_samples(shimmer, drone)
    samples = apply_reverb_decay(samples, decay=0.992)
    samples = apply_fade(samples, fade_in_ms=20, fade_out_ms=450)
    save_wav('void/tool_complete.wav', samples)
    print("✓ Generated tool_complete.wav - resonance bloom")

def generate_prompt_submit():
    """Thought released into void - brief particle"""
    samples = generate_particle_burst(0.08, amplitude=0.16)
    samples = apply_fade(samples, fade_in_ms=5, fade_out_ms=90)
    save_wav('void/prompt_submit.wav', samples)
    print("✓ Generated prompt_submit.wav - thought released")

def generate_response_start():
    """Cosmic data stream beginning - void speaks"""
    # Low drone with building shimmer
    drone = generate_deep_drone(LOW_DRONE, 0.5, amplitude=0.18)
    shimmer = generate_cosmic_shimmer(PARTICLE, 0.5, amplitude=0.15)

    samples = mix_samples(drone, shimmer)
    samples = apply_fade(samples, fade_in_ms=200, fade_out_ms=250)
    save_wav('void/response_start.wav', samples)
    print("✓ Generated response_start.wav - void whispers")

def generate_response_end():
    """Cosmic stream subsiding - void quiets"""
    shimmer = generate_cosmic_shimmer(RESONANCE, 0.4, amplitude=0.14)
    drone = generate_deep_drone(DEEP_VOID, 0.4, amplitude=0.16)

    samples = mix_samples(shimmer, drone)
    samples = apply_fade(samples, fade_in_ms=100, fade_out_ms=500)
    save_wav('void/response_end.wav', samples)
    print("✓ Generated response_end.wav - void settles")

def generate_subagent_done():
    """Stellar achievement - cosmic celebration"""
    samples = []

    # Ascending particle bursts
    for i in range(3):
        burst = generate_particle_burst(0.12, amplitude=0.17 + i * 0.02)
        samples.extend(burst)
        if i < 2:
            samples.extend([0] * int(44100 * 0.08))

    # Triumphant resonance
    resonance = generate_cosmic_shimmer(STELLAR, 0.6, amplitude=0.2)
    drone = generate_deep_drone(THRESHOLD, 0.6, amplitude=0.18)

    celebration = mix_samples(resonance, drone)
    samples.extend(celebration)

    samples = apply_fade(samples, fade_in_ms=50, fade_out_ms=500)
    save_wav('void/subagent_done.wav', samples)
    print("✓ Generated subagent_done.wav - stellar achievement")

def generate_precompact_warning():
    """Void pressure - pulsing cosmic urgency"""
    samples = []

    # Three pulses of increasing intensity
    for i in range(3):
        # Pulsing drone
        pulse_drone = generate_deep_drone(LOW_DRONE, 0.25, amplitude=0.2 + i * 0.05)
        pulse_shimmer = generate_cosmic_shimmer(RESONANCE * (1 + i * 0.2), 0.25, amplitude=0.15)

        pulse = mix_samples(pulse_drone, pulse_shimmer)
        samples.extend(pulse)

        if i < 2:
            samples.extend([0] * int(44100 * 0.12))

    samples = apply_fade(samples, fade_in_ms=100, fade_out_ms=400)
    save_wav('void/precompact_warning.wav', samples)
    print("✓ Generated precompact_warning.wav - void pressure")

def generate_notification():
    """Cosmic ping - signal from the depths"""
    # Clear particle burst with resonant tail
    particle = generate_particle_burst(0.15, amplitude=0.22)
    resonance = generate_cosmic_shimmer(SHIMMER, 0.4, amplitude=0.18)

    samples = combine_samples(particle, resonance)
    samples = apply_reverb_decay(samples, decay=0.988)
    samples = apply_fade(samples, fade_in_ms=10, fade_out_ms=450)
    save_wav('void/notification.wav', samples)
    print("✓ Generated notification.wav - cosmic ping")

if __name__ == '__main__':
    print("🌌 Generating Void sound suite...")
    print("Theme: Cosmic liminal space, deep void, stellar resonance")
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
    print("📁 Location: void/")
    print("🌠 Enter the cosmic void...")
