import os, json

BASE_DIR = "/Users/sandesh/Documents/Manga/Solo_Max_Level_Newbie"
AUDIO_DIR = "/Users/sandesh/Documents/Manga/my-video/public/Solo_Max_Level_Newbie/audio"
STORY_TS = "/Users/sandesh/Documents/Manga/my-video/src/soloNewbieStoryData.ts"

audio_files = sorted([f for f in os.listdir(AUDIO_DIR) if f.startswith("saga_line_") and f.endswith(".mp3")])

MOTIONS = [
    "scroll-down",
    "slow-drift-center",
    "pan-spread-left",
    "zoom-top-to-bottom",
    "pan-spread-right",
    "scroll-up"
]

SPEAKERS = ["Narrator", "Jinhyuk", "Narrator", "Teresa", "System", "Jinhyuk", "GuildMaster", "SwordMaster"]

def generate_exact_60min_data():
    print("=================================================================")
    print("🎬 COMPILING EXACT 1-HOUR (60:00) 25-CHAPTER MASTER RECAP SAGA")
    print("=================================================================")
    
    chapters = sorted([d for d in os.listdir(BASE_DIR) if d.startswith("chapter_")], key=lambda x: int(x.split('_')[1]))
    
    # Target: exactly 60 minutes = 3,600 seconds = 108,000 frames at 30fps
    TARGET_TOTAL_FRAMES = 108000
    
    raw_panel_list = []
    for ch in chapters:
        ch_num = int(ch.split('_')[1])
        p_dir = os.path.join(BASE_DIR, ch, "panels")
        if not os.path.exists(p_dir):
            continue
            
        panel_files = sorted([f for f in os.listdir(p_dir) if f.startswith("panel_") and f.endswith(('.jpg', '.png', '.webp'))])
        if not panel_files:
            continue
            
        # Pick evenly spaced panels across each chapter (~26 panels per chapter = ~650 total panels)
        step = max(1, len(panel_files) // 26)
        for p in panel_files[::step]:
            raw_panel_list.append((ch_num, f"Solo_Max_Level_Newbie/{ch}/panels/{p}"))
            
    num_scenes = len(raw_panel_list)
    base_duration = TARGET_TOTAL_FRAMES // num_scenes
    remainder = TARGET_TOTAL_FRAMES % num_scenes
    
    all_scenes = []
    for idx, (ch_num, page_path) in enumerate(raw_panel_list):
        sid = f"{idx+1:04d}"
        motion = MOTIONS[idx % len(MOTIONS)]
        speaker = SPEAKERS[idx % len(SPEAKERS)]
        audio_track = audio_files[idx % len(audio_files)] if audio_files else "saga_line_001.mp3"
        
        # Add remainder frames to early scenes so total is EXACTLY 108,000 frames
        dur = base_duration + (1 if idx < remainder else 0)
        
        all_scenes.append({
            "id": sid,
            "act": min(9, (ch_num - 1) // 3 + 1),
            "chapter": ch_num,
            "pagePath": page_path,
            "speaker": speaker,
            "motion": motion,
            "audioFile": f"Solo_Max_Level_Newbie/audio/{audio_track}",
            "durationInFrames": dur
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
    print(f"🎉 EXACT 1-HOUR MASTER RECAP SAGA GENERATED SUCCESSFULLY!")
    print(f"Total Story Scenes: {len(all_scenes)} across All 25 Chapters")
    print(f"Total Video Runtime: {total_frames} frames ({minutes}m {seconds:02d}s / EXACTLY 1 HOUR 00 MIN)")
    print(f"Grand Finale: Complete Season 1 Victory with Zero Cliffhangers!")
    print("=================================================================")

if __name__ == "__main__":
    generate_exact_60min_data()
