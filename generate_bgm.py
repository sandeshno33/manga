import os, wave, numpy as np
from scipy.signal import butter, filtfilt

output_dir = "/Users/sandesh/Documents/Manga/my-video/public/Knights_of_Sidonia/audio"
os.makedirs(output_dir, exist_ok=True)
SAMPLE_RATE = 44100

def apply_reverb(audio, decay=0.4, delays=[0.05, 0.08, 0.12, 0.17, 0.23]):
    out = np.copy(audio)
    for d in delays:
        samples = int(d * SAMPLE_RATE)
        if samples < len(audio):
            out[samples:] += audio[:-samples] * decay
            decay *= 0.75
    return out / np.max(np.abs(out) + 1e-6)

def synth_pad(freq, duration, sample_rate=SAMPLE_RATE):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    # 3 detuned oscillators with warm saturation
    osc1 = np.sin(2 * np.pi * freq * t)
    osc2 = 0.5 * np.sin(2 * np.pi * (freq * 1.006) * t)
    osc3 = 0.5 * np.sin(2 * np.pi * (freq * 0.994) * t)
    osc4 = 0.25 * np.sin(2 * np.pi * (freq * 2.0) * t)
    sig = osc1 + osc2 + osc3 + osc4
    
    # Envelope: slow attack and smooth release
    attack = int(0.6 * sample_rate)
    release = int(0.8 * sample_rate)
    env = np.ones_like(t)
    if len(env) > attack + release:
        env[:attack] = np.linspace(0, 1, attack)
        env[-release:] = np.linspace(1, 0, release)
    return sig * env

def lowpass_filter(data, cutoff=1200, fs=SAMPLE_RATE, order=4):
    b, a = butter(order, cutoff / (0.5 * fs), btype='low')
    return filtfilt(b, a, data)

def save_stereo_wav(filepath, left_channel, right_channel):
    # Normalize
    max_val = max(np.max(np.abs(left_channel)), np.max(np.abs(right_channel)), 1e-6)
    left_norm = (left_channel / max_val * 0.85 * 32767).astype(np.int16)
    right_norm = (right_channel / max_val * 0.85 * 32767).astype(np.int16)
    
    stereo = np.empty((left_norm.size + right_norm.size,), dtype=np.int16)
    stereo[0::2] = left_norm
    stereo[1::2] = right_norm
    
    with wave.open(filepath, 'wb') as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(stereo.tobytes())
    print(f"Generated BGM: {filepath}")

# ==============================================================================
# TRACK 1: Deep Space Cosmic Mecha Combat (Act 1)
# ==============================================================================
def generate_act1_space_battle():
    duration = 45.0
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    
    # Sub-bass drone in D (36.7 Hz & 73.4 Hz)
    sub = 0.6 * np.sin(2 * np.pi * 36.7 * t) + 0.4 * np.sin(2 * np.pi * 73.4 * t)
    
    # Tense rhythmic pulse at 115 BPM
    bpm = 115
    pulse_period = 60.0 / bpm
    pulse = np.sin(2 * np.pi * (1.0 / pulse_period) * t) ** 4
    pulsing_sub = sub * (0.5 + 0.5 * pulse)
    
    # Dark string pads (Dm chord: D3, F3, A3, D4)
    pad = np.zeros_like(t)
    chord_times = [(0, 12, 146.8), (12, 24, 130.8), (24, 36, 116.5), (36, 45, 146.8)]
    for start, end, root in chord_times:
        s_idx = int(start * SAMPLE_RATE)
        e_idx = int(end * SAMPLE_RATE)
        dur = end - start
        chord = synth_pad(root, dur) + synth_pad(root * 1.2, dur) + synth_pad(root * 1.5, dur)
        pad[s_idx:e_idx] += chord[:e_idx - s_idx]
        
    left = apply_reverb(lowpass_filter(pulsing_sub * 0.7 + pad * 0.45, cutoff=1500))
    right = apply_reverb(lowpass_filter(pulsing_sub * 0.7 + np.roll(pad, 400) * 0.45, cutoff=1600))
    save_stereo_wav(os.path.join(output_dir, "bgm_act1.wav"), left, right)

# ==============================================================================
# TRACK 2: Melancholic Subterranean Catacombs (Act 2)
# ==============================================================================
def generate_act2_catacombs():
    duration = 45.0
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    
    # Low hollow drone in A (55 Hz and 110 Hz)
    hollow_drone = 0.5 * np.sin(2 * np.pi * 55 * t) + 0.3 * np.sin(2 * np.pi * 110 * t)
    
    # Melancholic minor piano/bell echoes (Am - Em - F - C)
    chords = [(0, 11, 220.0), (11, 22, 164.8), (22, 33, 174.6), (33, 45, 130.8)]
    music = np.zeros_like(t)
    for start, end, freq in chords:
        s_idx = int(start * SAMPLE_RATE)
        e_idx = int(end * SAMPLE_RATE)
        dur = end - start
        note = synth_pad(freq, dur) + synth_pad(freq * 1.2, dur) * 0.6
        music[s_idx:e_idx] += note[:e_idx - s_idx]
        
    # Reverb ambient water/wind noise
    noise = np.random.normal(0, 0.04, len(t))
    ambient = lowpass_filter(noise, cutoff=350)
    
    left = apply_reverb(hollow_drone * 0.5 + music * 0.4 + ambient * 0.3, decay=0.5)
    right = apply_reverb(hollow_drone * 0.5 + np.roll(music, 600) * 0.4 + ambient * 0.3, decay=0.5)
    save_stereo_wav(os.path.join(output_dir, "bgm_act2.wav"), left, right)

# ==============================================================================
# TRACK 3: High-Pace Pursuit to Sky Reveal (Act 3)
# ==============================================================================
def generate_act3_pursuit():
    duration = 45.0
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    
    # Cyberpunk bass arpeggio / running beat
    bass_freq = 65.4  # C2
    bass_pulse = np.sin(2 * np.pi * bass_freq * t) * (np.sin(2 * np.pi * 8 * t) ** 2)
    
    # Sky reveal transition after 25s (Grand major swelling chord C - G - Am - F)
    chords = [(0, 12, 130.8), (12, 24, 146.8), (24, 35, 130.8 * 1.5), (35, 45, 130.8 * 2.0)]
    pad = np.zeros_like(t)
    for start, end, freq in chords:
        s_idx = int(start * SAMPLE_RATE)
        e_idx = int(end * SAMPLE_RATE)
        dur = end - start
        chord = synth_pad(freq, dur) + synth_pad(freq * 1.25, dur) + synth_pad(freq * 1.5, dur)
        pad[s_idx:e_idx] += chord[:e_idx - s_idx]
        
    left = apply_reverb(lowpass_filter(bass_pulse * 0.5 + pad * 0.55, cutoff=2000))
    right = apply_reverb(lowpass_filter(bass_pulse * 0.5 + np.roll(pad, 300) * 0.55, cutoff=2000))
    save_stereo_wav(os.path.join(output_dir, "bgm_act3.wav"), left, right)

# ==============================================================================
# TRACK 4: Ambient Sci-Fi & Photosynthesis (Act 4)
# ==============================================================================
def generate_act4_cyber_city():
    duration = 45.0
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    
    # Warm floating atmospheric pads in F# Major / Ab Major
    chords = [(0, 11, 185.0), (11, 23, 207.6), (23, 34, 233.0), (34, 45, 185.0)]
    pad = np.zeros_like(t)
    for start, end, freq in chords:
        s_idx = int(start * SAMPLE_RATE)
        e_idx = int(end * SAMPLE_RATE)
        dur = end - start
        chord = synth_pad(freq, dur) + synth_pad(freq * 1.26, dur) + synth_pad(freq * 1.5, dur) * 0.7
        pad[s_idx:e_idx] += chord[:e_idx - s_idx]
        
    left = apply_reverb(lowpass_filter(pad * 0.6, cutoff=1800), decay=0.45)
    right = apply_reverb(lowpass_filter(np.roll(pad, 500) * 0.6, cutoff=1800), decay=0.45)
    save_stereo_wav(os.path.join(output_dir, "bgm_act4.wav"), left, right)

# ==============================================================================
# TRACK 5: Academy Comedy & Blunder (Act 5)
# ==============================================================================
def generate_act5_academy():
    duration = 45.0
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    
    # Bouncy synth pluck rhythm at 120 BPM
    bpm = 120
    beat_t = (t * (bpm / 60.0)) % 1.0
    pluck = np.exp(-beat_t * 6.0) * np.sin(2 * np.pi * 261.6 * t)
    
    # Upbeat melody progression
    chords = [(0, 11, 261.6), (11, 23, 293.6), (23, 34, 329.6), (34, 45, 261.6)]
    pad = np.zeros_like(t)
    for start, end, freq in chords:
        s_idx = int(start * SAMPLE_RATE)
        e_idx = int(end * SAMPLE_RATE)
        dur = end - start
        chord = synth_pad(freq, dur) * 0.4
        pad[s_idx:e_idx] += chord[:e_idx - s_idx]
        
    left = apply_reverb(pluck * 0.4 + pad * 0.4, decay=0.3)
    right = apply_reverb(pluck * 0.4 + np.roll(pad, 300) * 0.4, decay=0.3)
    save_stereo_wav(os.path.join(output_dir, "bgm_act5.wav"), left, right)

# ==============================================================================
# TRACK 6: Immortal Council & Looming Cosmic Threat (Act 6)
# ==============================================================================
def generate_act6_council():
    duration = 45.0
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    
    # Dark ominous low drone in C (32.7 Hz and 65.4 Hz with slow beating)
    drone = 0.6 * np.sin(2 * np.pi * 32.7 * t) + 0.4 * np.sin(2 * np.pi * 65.4 * t) + 0.2 * np.sin(2 * np.pi * 67.0 * t)
    
    # Ominous minor chords (Cm - Ab - Fm - G)
    chords = [(0, 12, 130.8), (12, 23, 103.8), (23, 34, 87.3), (34, 45, 98.0)]
    dark_pad = np.zeros_like(t)
    for start, end, freq in chords:
        s_idx = int(start * SAMPLE_RATE)
        e_idx = int(end * SAMPLE_RATE)
        dur = end - start
        chord = synth_pad(freq, dur) + synth_pad(freq * 1.189, dur) + synth_pad(freq * 1.5, dur)
        dark_pad[s_idx:e_idx] += chord[:e_idx - s_idx]
        
    left = apply_reverb(lowpass_filter(drone * 0.6 + dark_pad * 0.45, cutoff=1200), decay=0.55)
    right = apply_reverb(lowpass_filter(drone * 0.6 + np.roll(dark_pad, 600) * 0.45, cutoff=1200), decay=0.55)
    save_stereo_wav(os.path.join(output_dir, "bgm_act6.wav"), left, right)

# ==============================================================================
# TRACK 7: Grand Awakening of Tsugumori & Sidonia Cosmos (Act 7)
# ==============================================================================
def generate_act7_epic_tsugumori():
    duration = 50.0
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    
    # Epic heroic chord progression (D - A - Bm - G - D - A - G - D)
    chords = [
        (0, 7, 146.8),   # D3
        (7, 14, 110.0),  # A2
        (14, 21, 123.5), # Bm2
        (21, 28, 98.0),  # G2
        (28, 35, 146.8), # D3
        (35, 42, 110.0), # A2
        (42, 50, 146.8 * 2) # D4 Grand Climax
    ]
    
    epic_pad = np.zeros_like(t)
    for start, end, freq in chords:
        s_idx = int(start * SAMPLE_RATE)
        e_idx = int(end * SAMPLE_RATE)
        dur = end - start
        chord = (
            synth_pad(freq, dur) +
            synth_pad(freq * 1.26, dur) * 0.9 +
            synth_pad(freq * 1.5, dur) * 0.9 +
            synth_pad(freq * 2.0, dur) * 0.6
        )
        epic_pad[s_idx:e_idx] += chord[:e_idx - s_idx]
        
    sub = 0.4 * np.sin(2 * np.pi * 36.7 * t)
    
    left = apply_reverb(lowpass_filter(sub * 0.4 + epic_pad * 0.65, cutoff=3000), decay=0.5)
    right = apply_reverb(lowpass_filter(sub * 0.4 + np.roll(epic_pad, 450) * 0.65, cutoff=3000), decay=0.5)
    save_stereo_wav(os.path.join(output_dir, "bgm_act7.wav"), left, right)

print("Synthesizing ambient cinematic BGM soundtracks for all 7 Acts...")
generate_act1_space_battle()
generate_act2_catacombs()
generate_act3_pursuit()
generate_act4_cyber_city()
generate_act5_academy()
generate_act6_council()
generate_act7_epic_tsugumori()
print("All 7 ambient BGM audio tracks created successfully!")
