import os, sys, json
from mutagen.mp3 import MP3

BASE_DIR = "/Users/sandesh/Documents/Manga"
PUBLIC_DIR = os.path.join(BASE_DIR, "my-video/public")
STORY_TS = os.path.join(BASE_DIR, "my-video/src/soloNewbieStoryData.ts")

def verify_flow():
    print("=================================================================")
    print("🔍 AUDITING & VERIFYING FULL-LENGTH VOICEOVER & VIDEO FLOW")
    print("=================================================================")

    # Parse scenes from soloNewbieStoryData.ts
    with open(STORY_TS, 'r') as f:
        content = f.read()

    # Extract all scene entries
    import re
    scene_matches = re.findall(r'id:\s*"([^"]+)",\s*act:\s*(\d+),\s*chapter:\s*(\d+),\s*pagePath:\s*"([^"]+)",\s*speaker:\s*"([^"]+)",\s*motion:\s*"([^"]+)",\s*audioFile:\s*"([^"]+)",\s*durationInFrames:\s*(\d+)', content)

    print(f"Total Parsed Scenes: {len(scene_matches)}")
    
    missing_images = []
    missing_audios = []
    truncated_audios = []
    
    total_video_frames = 0
    
    for idx, (sid, act, ch, page_path, speaker, motion, audio_file, dur_frames) in enumerate(scene_matches):
        dur_f = int(dur_frames)
        total_video_frames += dur_f
        
        # 1. Verify Image
        img_abs = os.path.join(PUBLIC_DIR, page_path)
        if not os.path.exists(img_abs) or os.path.getsize(img_abs) < 1000:
            missing_images.append((sid, page_path))
            
        # 2. Verify Audio
        aud_abs = os.path.join(PUBLIC_DIR, audio_file)
        if not os.path.exists(aud_abs) or os.path.getsize(aud_abs) < 500:
            missing_audios.append((sid, audio_file))
        else:
            try:
                audio = MP3(aud_abs)
                audio_sec = audio.info.length
                audio_frames = int(audio_sec * 30)
                # Check if scene cuts off audio early
                if audio_frames > dur_f:
                    truncated_audios.append((sid, audio_file, audio_frames, dur_f))
            except Exception as e:
                missing_audios.append((sid, f"{audio_file} (Error: {e})"))

    print(f"\n--- ASSET INTEGRITY REPORT ---")
    print(f"✔ Missing Images: {len(missing_images)}")
    if missing_images:
        for m in missing_images[:5]: print(f"   ❌ Missing Image: {m}")
        
    print(f"✔ Missing / Corrupt Audios: {len(missing_audios)}")
    if missing_audios:
        for m in missing_audios[:5]: print(f"   ❌ Missing Audio: {m}")
        
    print(f"✔ Truncated Voiceovers: {len(truncated_audios)}")
    if truncated_audios:
        for t in truncated_audios[:5]: print(f"   ⚠️ Truncated Audio: Scene {t[0]} need {t[2]}f, got {t[3]}f")

    # Inspect the final 10 scenes (The Grand Climax / Ending)
    print("\n--- FINAL CLIMAX & ENDING VERIFICATION (Last 10 Scenes) ---")
    last_10 = scene_matches[-10:]
    for s in last_10:
        sid, act, ch, page_path, speaker, motion, audio_file, dur_frames = s
        aud_abs = os.path.join(PUBLIC_DIR, audio_file)
        dur_s = int(dur_frames) / 30.0
        aud_len = round(MP3(aud_abs).info.length, 2) if os.path.exists(aud_abs) else 0
        print(f"Scene {sid:>4} | Ch {ch:>2} | {speaker:<11} | Audio: {aud_len:>4.1f}s / Scene: {dur_s:>4.1f}s | Flow: {'✔ PERFECT' if dur_s >= aud_len else '⚠️ CUT'}")

    total_mins = total_video_frames / 30 / 60
    print(f"\n=================================================================")
    print(f"🏁 TOTAL COMPOSITION RUNTIME: {total_video_frames} Frames ({total_mins:.2f} Minutes)")
    print(f"Flow Integrity: {'100% CLEAN & SYNCHRONIZED' if not missing_images and not missing_audios and not truncated_audios else 'NEEDS FIX'}")
    print("=================================================================")

if __name__ == "__main__":
    verify_flow()
