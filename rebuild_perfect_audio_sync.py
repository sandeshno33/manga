import os, re, json
from mutagen.mp3 import MP3

BASE_DIR = "/Users/sandesh/Documents/Manga"
PUBLIC_DIR = os.path.join(BASE_DIR, "my-video/public")
AUDIO_DIR = os.path.join(PUBLIC_DIR, "Solo_Max_Level_Newbie/audio")
STORY_TS = os.path.join(BASE_DIR, "my-video/src/soloNewbieStoryData.ts")

# 1. Get all synthesized saga audio files
audio_files = sorted([f for f in os.listdir(AUDIO_DIR) if f.startswith("saga_line_") and f.endswith(".mp3")])

# Measure each audio duration exactly
audio_durations = {}
for f in audio_files:
    p = os.path.join(AUDIO_DIR, f)
    dur = MP3(p).info.length
    audio_durations[f] = dur

MOTIONS = [
    "scroll-down",
    "slow-drift-center",
    "pan-spread-left",
    "zoom-top-to-bottom",
    "pan-spread-right",
    "scroll-up"
]

SPEAKERS = ["Narrator", "Jinhyuk", "Narrator", "Teresa", "System", "Jinhyuk", "GuildMaster", "SwordMaster"]

def rebuild_perfect_sync():
    print("=================================================================")
    print("🎯 REBUILDING 100% FLAWLESS AUDIO & VIDEO SYNCHRONIZATION")
    print("=================================================================")

    chapters = sorted([d for d in os.listdir(os.path.join(BASE_DIR, "Solo_Max_Level_Newbie")) if d.startswith("chapter_")], key=lambda x: int(x.split('_')[1]))
    
    # We want a total runtime of ~55 to 60 minutes (~100,000 to 108,000 frames)
    # Each scene will hold for the EXACT duration of the voiceover + 8 frames padding
    all_scenes = []
    global_id = 1
    
    audio_idx = 0
    num_audios = len(audio_files)

    for ch in chapters:
        ch_num = int(ch.split('_')[1])
        p_dir = os.path.join(BASE_DIR, "Solo_Max_Level_Newbie", ch, "panels")
        if not os.path.exists(p_dir):
            continue
            
        panel_files = sorted([f for f in os.listdir(p_dir) if f.startswith("panel_") and f.endswith(('.jpg', '.png', '.webp'))])
        if not panel_files:
            continue
            
        # Select rich panels for this chapter (~18-22 panels per chapter)
        step = max(1, len(panel_files) // 20)
        selected_panels = panel_files[::step]
        
        for p_name in selected_panels:
            aud_file = audio_files[audio_idx % num_audios]
            aud_dur = audio_durations[aud_file]
            
            # Exact frame count: audio length + 8 frames safe padding (0.26s)
            dur_frames = int(aud_dur * 30) + 8
            
            sid = f"{global_id:04d}"
            motion = MOTIONS[global_id % len(MOTIONS)]
            speaker = SPEAKERS[global_id % len(SPEAKERS)]
            page_path = f"Solo_Max_Level_Newbie/{ch}/panels/{p_name}"
            
            all_scenes.append({
                "id": sid,
                "act": min(9, (ch_num - 1) // 3 + 1),
                "chapter": ch_num,
                "pagePath": page_path,
                "speaker": speaker,
                "motion": motion,
                "audioFile": f"Solo_Max_Level_Newbie/audio/{aud_file}",
                "durationInFrames": dur_frames,
                "audio_dur": aud_dur
            })
            global_id += 1
            audio_idx += 1

    # Add Triumphant Grand Finale Scene at the very end
    finale_aud = "saga_line_056.mp3"
    finale_dur = audio_durations.get(finale_aud, 7.0)
    all_scenes.append({
        "id": f"{global_id:04d}",
        "act": 9,
        "chapter": 25,
        "pagePath": "Solo_Max_Level_Newbie/chapter_25/panels/panel_050.jpg",
        "speaker": "Jinhyuk",
        "motion": "zoom-top-to-bottom",
        "audioFile": f"Solo_Max_Level_Newbie/audio/{finale_aud}",
        "durationInFrames": int(finale_dur * 30) + 150, # 5 extra seconds of peaceful outro ambiance
        "audio_dur": finale_dur
    })

    # Write out soloNewbieStoryData.ts
    items_ts = []
    for s in all_scenes:
        items_ts.append(f'''  {{
    id: "{s['id']}",
    act: {s['act']},
    chapter: {s['chapter']},
    pagePath: "{s['pagePath']}",
    speaker: "{s['speaker']}",
    motion: "{s['motion']}",
    audioFile: "{s['audioFile']}",
    durationInFrames: {s['durationInFrames']},
  }}''')

    ts_content = '''import { CameraMotion, SlideDirection } from "./types";

export type SoloSpeakerType =
  | "Narrator"
  | "Jinhyuk"
  | "Teresa"
  | "System"
  | "GuildMaster"
  | "Cheon"
  | "Merchant"
  | "Player"
  | "SwordMaster";

export interface SoloSceneItem {
  id: string;
  act: number;
  chapter: number;
  pagePath: string;
  speaker: SoloSpeakerType;
  motion: CameraMotion;
  slideDirection?: SlideDirection;
  audioFile: string;
  durationInFrames: number;
}

export const SOLO_SCENES: SoloSceneItem[] = [
''' + ',\n'.join(items_ts) + '\n];\n'

    with open(STORY_TS, 'w') as f:
        f.write(ts_content)
        
    total_frames = sum(s["durationInFrames"] for s in all_scenes)
    total_sec = total_frames / 30.0
    minutes = int(total_sec // 60)
    seconds = int(total_sec % 60)
    
    print(f"\n=================================================================")
    print(f"🎉 PERFECT SYNC REBUILT SUCCESSFULLY!")
    print(f"Total Scenes: {len(all_scenes)}")
    print(f"Total Video Runtime: {total_frames} frames ({minutes}m {seconds:02d}s)")
    print(f"Truncated Voiceovers: ZERO (Every line finishes completely with clean padding)!")
    print("=================================================================")

if __name__ == "__main__":
    rebuild_perfect_sync()
