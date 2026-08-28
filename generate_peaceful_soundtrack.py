import os, math, struct, wave

AUDIO_DIR = "/Users/sandesh/Documents/Manga/my-video/public/Solo_Max_Level_Newbie/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

def make_peaceful_wav(filename, duration, sample_rate, gen_fn):
    out_path = os.path.join(AUDIO_DIR, filename)
    num_samples = int(duration * sample_rate)
    with wave.open(out_path, 'wb') as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        frames = bytearray()
        for i in range(num_samples):
            t = i / sample_rate
            left, right = gen_fn(t, duration)
            l_val = max(-32767, min(32767, int(left * 32767)))
            r_val = max(-32767, min(32767, int(right * 32767)))
            frames.extend(struct.pack('<hh', l_val, r_val))
        wav.writeframes(frames)
    print(f"✔ Created Soothing Ambient Track: {filename}")
    return out_path

def synth_soothing_soundscapes():
    print("Generating ultra-peaceful, soothing ambient music (Sleep / Lo-Fi Meditation soundscapes)...")

    # 1. Warm Serene Ambient Pad (Soft C Major / A Minor celestial waves)
    def bgm_serene(t, d):
        # Soft layered sine chords: C3 (130.8Hz), G3 (196.0Hz), E4 (329.6Hz), B4 (493.9Hz)
        pad1 = 0.18 * math.sin(2 * math.pi * 130.81 * t + 0.1 * math.sin(2 * math.pi * 0.2 * t))
        pad2 = 0.14 * math.sin(2 * math.pi * 196.00 * t + 0.1 * math.cos(2 * math.pi * 0.15 * t))
        pad3 = 0.12 * math.sin(2 * math.pi * 329.63 * t) * (0.6 + 0.4 * math.sin(2 * math.pi * 0.1 * t))
        pad4 = 0.08 * math.sin(2 * math.pi * 493.88 * t) * (0.5 + 0.5 * math.cos(2 * math.pi * 0.08 * t))
        ambient = (pad1 + pad2 + pad3 + pad4) * 0.6
        return ambient * 0.95, ambient * 1.05

    make_peaceful_wav("bgm_tower_manifest.wav", 75.0, 44100, bgm_serene)

    # 2. Peaceful Lo-Fi Dream Drift (Gentle F Major 7th harp & celestial harmonics)
    def bgm_dream(t, d):
        chord1 = 0.16 * math.sin(2 * math.pi * 174.61 * t) + 0.12 * math.sin(2 * math.pi * 261.63 * t)
        chord2 = 0.10 * math.sin(2 * math.pi * 349.23 * t) + 0.08 * math.sin(2 * math.pi * 440.00 * t)
        pulse = (0.5 + 0.5 * math.sin(2 * math.pi * 0.12 * t))
        shimmer = 0.05 * math.sin(2 * math.pi * 659.25 * t) * math.sin(2 * math.pi * 0.25 * t)
        out = (chord1 + chord2) * pulse * 0.6 + shimmer
        return out * 1.02, out * 0.98

    make_peaceful_wav("bgm_level_grind.wav", 75.0, 44100, bgm_dream)

    # 3. Soft Midnight Ambient Reflection (Deep calm resonant harmonics)
    def bgm_midnight(t, d):
        bass = 0.18 * math.sin(2 * math.pi * 110.00 * t) * (0.7 + 0.3 * math.sin(2 * math.pi * 0.09 * t))
        mid = 0.12 * math.sin(2 * math.pi * 220.00 * t) + 0.10 * math.sin(2 * math.pi * 277.18 * t)
        high = 0.06 * math.sin(2 * math.pi * 440.00 * t) * (0.5 + 0.5 * math.cos(2 * math.pi * 0.14 * t))
        out = (bass + mid + high) * 0.55
        return out * 0.97, out * 1.03

    make_peaceful_wav("bgm_boss_battle.wav", 75.0, 44100, bgm_midnight)

    # 4. Mystic Calming Sanctuary (Gothic peaceful flute & glass harmonics)
    def bgm_sanctuary(t, d):
        drone = 0.16 * math.sin(2 * math.pi * 146.83 * t) + 0.12 * math.sin(2 * math.pi * 220.00 * t)
        flute = 0.09 * math.sin(2 * math.pi * 329.63 * t) * (0.6 + 0.4 * math.sin(2 * math.pi * 0.18 * t))
        glass = 0.06 * math.sin(2 * math.pi * 587.33 * t) * (0.4 + 0.6 * math.cos(2 * math.pi * 0.11 * t))
        out = (drone + flute + glass) * 0.55
        return out * 1.04, out * 0.96

    make_peaceful_wav("bgm_vampire_crypt.wav", 75.0, 44100, bgm_sanctuary)

    # 5. Starlight Healing Melody (Serene 432Hz ambient sleep frequencies)
    def bgm_starlight(t, d):
        fund = 0.18 * math.sin(2 * math.pi * 108.00 * t) # 432Hz harmonic
        warmth = 0.14 * math.sin(2 * math.pi * 216.00 * t) + 0.10 * math.sin(2 * math.pi * 324.00 * t)
        glow = 0.07 * math.sin(2 * math.pi * 432.00 * t) * (0.5 + 0.5 * math.sin(2 * math.pi * 0.08 * t))
        out = (fund + warmth + glow) * 0.58
        return out, out

    make_peaceful_wav("bgm_frost_peaks.wav", 75.0, 44100, bgm_starlight)

    # Empty out or soften SFX files to be silent / gentle
    def make_silent_sfx(filename):
        out_path = os.path.join(AUDIO_DIR, filename)
        with wave.open(out_path, 'wb') as wav:
            wav.setnchannels(2)
            wav.setsampwidth(2)
            wav.setframerate(44100)
            wav.writeframes(bytearray(44100 * 2)) # soft silent buffer
    
    for sfx in ["sfx_boss_roar.wav", "sfx_magic_blast.wav", "sfx_sword_slash.wav", "sfx_level_up.wav"]:
        make_silent_sfx(sfx)
    print("✔ Deactivated harsh SFX triggers for peaceful, sleep-friendly listening.")

if __name__ == "__main__":
    synth_soothing_soundscapes()
