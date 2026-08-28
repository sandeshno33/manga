import os, sys, math, struct, wave, asyncio, json
import edge_tts
from mutagen.mp3 import MP3

AUDIO_DIR = "/Users/sandesh/Documents/Manga/my-video/public/Solo_Max_Level_Newbie/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# 1. Synthesize Custom BGM Soundtracks and SFX
def make_wav(filename, duration, sample_rate, gen_fn):
    out_path = os.path.join(AUDIO_DIR, filename)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 100000:
        return out_path
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
    print(f"✔ Synthesized Audio Track: {filename}")
    return out_path

def synth_all_bgm_and_sfx():
    print("Synthesizing BGM & SFX audio tracks for Solo Max-Level Newbie...")
    
    # 1. BGM: Tower Manifest (Reality distortion & digital mystery)
    def bgm_tower(t, d):
        base = 0.25 * math.sin(2 * math.pi * 55 * t) + 0.15 * math.sin(2 * math.pi * 110 * t + 0.3 * math.sin(2 * math.pi * 2 * t))
        arp = 0.12 * math.sin(2 * math.pi * (220 + 55 * math.sin(2 * math.pi * 4 * t)) * t)
        pulse = 0.08 * math.sin(2 * math.pi * 440 * t) * (0.5 + 0.5 * math.sin(2 * math.pi * 6 * t))
        return base + arp + pulse, base + arp - pulse
    make_wav("bgm_tower_manifest.wav", 60.0, 44100, bgm_tower)

    # 2. BGM: Level Grind & Secret Farming (Upbeat electronic dungeon pulse)
    def bgm_grind(t, d):
        bass = 0.22 * math.sin(2 * math.pi * 65.4 * t) * (1.0 if (t % 0.25) < 0.18 else 0.2)
        synth = 0.14 * math.sin(2 * math.pi * 261.6 * t + math.sin(2 * math.pi * 8 * t))
        rhythm = 0.1 * math.sin(2 * math.pi * 523.2 * t) * (0.5 + 0.5 * math.sin(2 * math.pi * 12 * t))
        return bass + synth + rhythm, bass + synth - rhythm
    make_wav("bgm_level_grind.wav", 60.0, 44100, bgm_grind)

    # 3. BGM: Boss Battle Theme (Heavy action battle drums & danger brass)
    def bgm_boss(t, d):
        drum = 0.32 * math.sin(2 * math.pi * 48 * t) * math.exp(-3 * (t % 0.35))
        brass = 0.2 * math.sin(2 * math.pi * 130.8 * t) + 0.15 * math.sin(2 * math.pi * 155.5 * t)
        tension = 0.12 * math.sin(2 * math.pi * 311.1 * t + math.sin(2 * math.pi * 16 * t))
        return drum + brass + tension, drum + brass - tension
    make_wav("bgm_boss_battle.wav", 60.0, 44100, bgm_boss)

    # 4. BGM: Vampire Lord Crypt (Dark gothic choral ambiance)
    def bgm_vampire(t, d):
        drone = 0.28 * math.sin(2 * math.pi * 43.6 * t) + 0.12 * math.sin(2 * math.pi * 87.3 * t)
        organ = 0.16 * math.sin(2 * math.pi * 174.6 * t) * (0.5 + 0.5 * math.sin(2 * math.pi * 1.5 * t))
        whisper = 0.08 * math.sin(2 * math.pi * 349.2 * t)
        return drone + organ + whisper, drone + organ - whisper
    make_wav("bgm_vampire_crypt.wav", 60.0, 44100, bgm_vampire)

    # 5. BGM: Frost Peaks & Solo Dominance (Epic triumphant climax strings)
    def bgm_frost(t, d):
        strings = 0.22 * math.sin(2 * math.pi * 196 * t) + 0.18 * math.sin(2 * math.pi * 293.6 * t)
        lead = 0.18 * math.sin(2 * math.pi * 392 * t + 0.2 * math.sin(2 * math.pi * 5 * t))
        sub = 0.2 * math.sin(2 * math.pi * 49 * t)
        return strings + lead + sub, strings + lead - sub
    make_wav("bgm_frost_peaks.wav", 60.0, 44100, bgm_frost)

    # SFX Tracks
    def sfx_levelup(t, d):
        f = 440 + 600 * (t / d)
        return 0.4 * math.sin(2 * math.pi * f * t) * math.exp(-2.5 * t), 0.4 * math.sin(2 * math.pi * f * t) * math.exp(-2.5 * t)
    make_wav("sfx_level_up.wav", 1.8, 44100, sfx_levelup)

    def sfx_slash(t, d):
        f = 1200 * math.exp(-6 * t) + 80
        return 0.45 * math.sin(2 * math.pi * f * t) * math.exp(-4 * t), 0.45 * math.sin(2 * math.pi * f * t) * math.exp(-4 * t)
    make_wav("sfx_sword_slash.wav", 1.2, 44100, sfx_slash)

    def sfx_blast(t, d):
        f = 80 + 300 * math.sin(2 * math.pi * 15 * t)
        return 0.5 * math.sin(2 * math.pi * f * t) * math.exp(-2 * t), 0.5 * math.sin(2 * math.pi * f * t) * math.exp(-2 * t)
    make_wav("sfx_magic_blast.wav", 2.2, 44100, sfx_blast)

    def sfx_roar(t, d):
        f = 60 + 40 * math.sin(2 * math.pi * 8 * t)
        return 0.55 * math.sin(2 * math.pi * f * t) * math.exp(-1.8 * t), 0.55 * math.sin(2 * math.pi * f * t) * math.exp(-1.8 * t)
    make_wav("sfx_boss_roar.wav", 2.5, 44100, sfx_roar)

VOICE_MAP = {
    "Narrator": "en-US-ChristopherNeural",
    "Jinhyuk": "en-US-GuyNeural",
    "Teresa": "en-US-JennyNeural",
    "System": "en-US-AriaNeural",
    "GuildMaster": "en-GB-RyanNeural",
    "Cheon": "en-US-RogerNeural",
    "Merchant": "en-US-BrianNeural",
    "Player": "en-US-SteffanNeural"
}

# 2. Comprehensive Humanized Story Script for Solo Max-Level Newbie (Chapters 1 - 15)
STORY_LINES = [
    # CHAPTER 1: THE IMPOSSIBLE CLEAR (Act 1 - BGM: bgm_tower_manifest)
    {"id": "01", "act": 1, "ch": 1, "panel": "panel_001.jpg", "speaker": "Narrator", "motion": "pan-spread-left", "sfx": None, "text": "For eleven solid years, the hyper-realistic VR game 'Tower of Trials' drove millions of players to complete despair."},
    {"id": "02", "act": 1, "ch": 1, "panel": "panel_005.jpg", "speaker": "Narrator", "motion": "scroll-down", "sfx": None, "text": "Its absurd difficulty made everyone quit. Everyone, except for a single gaming Nutuber named Jinhyuk Kang."},
    {"id": "03", "act": 1, "ch": 1, "panel": "panel_012.jpg", "speaker": "Jinhyuk", "motion": "zoom-top-to-bottom", "sfx": "sfx_sword_slash.wav", "text": "Eleven years of grinding. Finally... the final floor is cleared. Game over."},
    {"id": "04", "act": 1, "ch": 1, "panel": "panel_020.jpg", "speaker": "Narrator", "motion": "scroll-down", "sfx": None, "text": "Jinhyuk uploaded his ending video to celebrate, planning to retire and find a real job."},
    {"id": "05", "act": 1, "ch": 1, "panel": "panel_032.jpg", "speaker": "System", "motion": "zoom-top-to-bottom", "sfx": "sfx_magic_blast.wav", "text": "Notice. The Tower of Trials service has concluded. Rebooting reality to match game parameters in three, two, one."},
    {"id": "06", "act": 1, "ch": 1, "panel": "panel_042.jpg", "speaker": "Narrator", "motion": "pan-spread-left", "sfx": None, "text": "A colossal black spire thousands of meters high pierced the sky over the city. The game was now real life."},

    # CHAPTER 2: SECRET CLASS ACQUISITION (Act 2 - BGM: bgm_level_grind)
    {"id": "07", "act": 2, "ch": 2, "panel": "panel_002.jpg", "speaker": "System", "motion": "scroll-down", "sfx": "sfx_level_up.wav", "text": "Player Kang Jinhyuk identified. You are the sole survivor who witnessed the ending. Hidden class 'Unknown' granted."},
    {"id": "08", "act": 2, "ch": 2, "panel": "panel_015.jpg", "speaker": "Jinhyuk", "motion": "zoom-top-to-bottom", "sfx": None, "text": "Class Unknown? And my innate ability is the 'Eyes of Gluttony'?! I can copy and steal any target's skills!"},
    {"id": "09", "act": 2, "ch": 2, "panel": "panel_030.jpg", "speaker": "Narrator", "motion": "scroll-down", "sfx": None, "text": "While regular players panicked in the streets, Jinhyuk packed his survival gear and headed straight toward the Tower entrance."},

    # CHAPTER 3-4: FLOOR 1 CATACOMBS & RELIC DAGGER (Act 3 - BGM: bgm_level_grind)
    {"id": "10", "act": 3, "ch": 3, "panel": "panel_008.jpg", "speaker": "Narrator", "motion": "pan-spread-left", "sfx": None, "text": "Stepping onto the first floor, Jinhyuk skipped the crowded starter plains and dived into the subterranean catacombs."},
    {"id": "11", "act": 3, "ch": 3, "panel": "panel_024.jpg", "speaker": "Jinhyuk", "motion": "scroll-down", "sfx": "sfx_sword_slash.wav", "text": "These skeletons only spawn on a three-minute timer. Hit the joint, steal their bone armor buff, and keep moving."},
    {"id": "12", "act": 3, "ch": 4, "panel": "panel_018.jpg", "speaker": "Narrator", "motion": "zoom-top-to-bottom", "sfx": "sfx_level_up.wav", "text": "Behind a hidden illusory wall, he retrieved the ancient relic: the Fang of the Black Dragon."},
    {"id": "13", "act": 3, "ch": 4, "panel": "panel_042.jpg", "speaker": "Player", "motion": "scroll-down", "sfx": None, "text": "Hey kid! Hand over whatever you found in that chest if you want to leave here in one piece!"},
    {"id": "14", "act": 3, "ch": 4, "panel": "panel_055.jpg", "speaker": "Jinhyuk", "motion": "zoom-top-to-bottom", "sfx": "sfx_magic_blast.wav", "text": "You picked the wrong rookie to rob. Eyes of Gluttony... extract skill!"},

    # CHAPTER 5-6: HALL OF TRIALS & FLOOR 1 BOSS (Act 4 - BGM: bgm_boss_battle)
    {"id": "15", "act": 4, "ch": 5, "panel": "panel_012.jpg", "speaker": "Narrator", "motion": "scroll-down", "sfx": None, "text": "Reaching the Hall of Trials, the floor was lined with lethal flame traps and moving spike pendulums."},
    {"id": "16", "act": 4, "ch": 5, "panel": "panel_035.jpg", "speaker": "Jinhyuk", "motion": "pan-spread-left", "sfx": None, "text": "Two steps forward, dodge right on the third pulse. I ran this dungeon a thousand times in the beta."},
    {"id": "17", "act": 4, "ch": 6, "panel": "panel_005.jpg", "speaker": "Narrator", "motion": "scroll-down", "sfx": "sfx_boss_roar.wav", "text": "At the summit of Floor 1, the gate guardian Aelgoth emerged, roaring with blazing infernal energy."},
    {"id": "18", "act": 4, "ch": 6, "panel": "panel_028.jpg", "speaker": "Jinhyuk", "motion": "zoom-top-to-bottom", "sfx": "sfx_sword_slash.wav", "text": "Your attack pattern has a two-second recovery opening. Strike the left knee crystal!"},
    {"id": "19", "act": 4, "ch": 6, "panel": "panel_050.jpg", "speaker": "Narrator", "motion": "pan-spread-left", "sfx": "sfx_magic_blast.wav", "text": "With a single surgical strike, the boss collapsed, shattering into thousands of glowing soul shards."},

    # CHAPTER 7: WORLD FIRST ANNOUNCEMENT (Act 5 - BGM: bgm_tower_manifest)
    {"id": "20", "act": 5, "ch": 7, "panel": "panel_008.jpg", "speaker": "System", "motion": "zoom-top-to-bottom", "sfx": "sfx_level_up.wav", "text": "World Announcement! Player Kang Jinhyuk has achieved the solo first clear of Floor 1! Title 'Pioneer of the Tower' bestowed!"},
    {"id": "21", "act": 5, "ch": 7, "panel": "panel_035.jpg", "speaker": "GuildMaster", "motion": "scroll-down", "sfx": None, "text": "Who the hell is Kang Jinhyuk?! Find him immediately and recruit him to the guild at any cost!"},

    # CHAPTER 8-9: VAMPIRE LABYRINTH & TERESA (Act 6 - BGM: bgm_vampire_crypt)
    {"id": "22", "act": 6, "ch": 8, "panel": "panel_005.jpg", "speaker": "Narrator", "motion": "scroll-down", "sfx": None, "text": "Ascending to the second floor, Jinhyuk stepped into the fog-shrouded Labyrinth of the Vampire Lord."},
    {"id": "23", "act": 6, "ch": 8, "panel": "panel_028.jpg", "speaker": "Teresa", "motion": "zoom-top-to-bottom", "sfx": None, "text": "Halt! You cannot enter the inner sanctuary. The sealed blood lord is awakening!"},
    {"id": "24", "act": 6, "ch": 8, "panel": "panel_050.jpg", "speaker": "Jinhyuk", "motion": "scroll-down", "sfx": None, "text": "Saintess Teresa de Laurent. I know why your holy magic is suppressed here. Follow my lead if you want to survive."},
    {"id": "25", "act": 6, "ch": 9, "panel": "panel_018.jpg", "speaker": "Cheon", "motion": "scroll-down", "sfx": "sfx_boss_roar.wav", "text": "Insolent mortals! You dare disturb the slumber of ancient noble blood?!"},
    {"id": "26", "act": 6, "ch": 9, "panel": "panel_045.jpg", "speaker": "Jinhyuk", "motion": "zoom-top-to-bottom", "sfx": "sfx_magic_blast.wav", "text": "Eyes of Gluttony: Blood Oath Override! You're not my enemy anymore... you're my familiar!"},

    # CHAPTER 10-11: MEGA-GUILD CONFRONTATION & IRON FORTRESS (Act 7 - BGM: bgm_level_grind)
    {"id": "27", "act": 7, "ch": 10, "panel": "panel_012.jpg", "speaker": "GuildMaster", "motion": "scroll-down", "sfx": None, "text": "This gate belongs to the Triad Alliance! Every solo player must pay an eighty percent tribute tax to pass!"},
    {"id": "28", "act": 7, "ch": 10, "panel": "panel_040.jpg", "speaker": "Jinhyuk", "motion": "zoom-top-to-bottom", "sfx": "sfx_sword_slash.wav", "text": "A tribute tax? In a game I cleared eleven years ago? Get out of my way before I clear your entire squad."},
    {"id": "29", "act": 7, "ch": 11, "panel": "panel_022.jpg", "speaker": "Narrator", "motion": "pan-spread-left", "sfx": "sfx_magic_blast.wav", "text": "Entering Floor 3's Iron Fortress, Jinhyuk dismantled twenty elite armored golems in under two minutes."},

    # CHAPTER 12-13: BLACK MARKET & FROST PEAKS (Act 8 - BGM: bgm_boss_battle)
    {"id": "30", "act": 8, "ch": 12, "panel": "panel_015.jpg", "speaker": "Merchant", "motion": "scroll-down", "sfx": None, "text": "Welcome to the secret exchange, customer. How did a beginner find the underground password?"},
    {"id": "31", "act": 8, "ch": 12, "panel": "panel_045.jpg", "speaker": "Jinhyuk", "motion": "zoom-top-to-bottom", "sfx": "sfx_level_up.wav", "text": "Give me the Ice Queen's antidote vial and three high-grade mana cores. Keep the change."},
    {"id": "32", "act": 8, "ch": 13, "panel": "panel_005.jpg", "speaker": "Narrator", "motion": "scroll-down", "sfx": None, "text": "At Floor 4's Frost Peaks, howling blizzards froze the wings of advancing vanguard beasts."},
    {"id": "33", "act": 8, "ch": 13, "panel": "panel_035.jpg", "speaker": "Jinhyuk", "motion": "pan-spread-left", "sfx": "sfx_boss_roar.wav", "text": "The Minotaur guardian has entered Berserk mode! Almost there... the moment he reveals his core...!"},

    # CHAPTER 14-15: GLUTTONY SKILL THEFT & EPIC CLIMAX (Act 9 - BGM: bgm_frost_peaks)
    {"id": "34", "act": 9, "ch": 14, "panel": "panel_010.jpg", "speaker": "Narrator", "motion": "scroll-down", "sfx": None, "text": "Dodging the crushing horns by millimeters, Jinhyuk activated his legendary innate ability."},
    {"id": "35", "act": 9, "ch": 14, "panel": "panel_045.jpg", "speaker": "Jinhyuk", "motion": "zoom-top-to-bottom", "sfx": "sfx_magic_blast.wav", "text": "Eyes of Gluttony: Target Locked! Extracting innate skill: Absolute Glacial Armor!"},
    {"id": "36", "act": 9, "ch": 14, "panel": "panel_075.jpg", "speaker": "System", "motion": "pan-spread-left", "sfx": "sfx_level_up.wav", "text": "Skill successfully copied! Ice resistance increased by five hundred percent!"},
    {"id": "37", "act": 9, "ch": 15, "panel": "panel_025.jpg", "speaker": "Narrator", "motion": "scroll-down", "sfx": "sfx_sword_slash.wav", "text": "Coated in unstoppable frost armor, the Black Dragon Fang sliced through the monster's heart in a single clean sweep."},
    {"id": "38", "act": 9, "ch": 15, "panel": "panel_060.jpg", "speaker": "System", "motion": "zoom-top-to-bottom", "sfx": "sfx_level_up.wav", "text": "Floor 4 Cleared! Total rank across all active players: Number One!"},
    {"id": "39", "act": 9, "ch": 15, "panel": "panel_085.jpg", "speaker": "Jinhyuk", "motion": "pan-spread-left", "sfx": None, "text": "The higher the tower goes, the more skills I get to steal. This is only the beginning."}
]

async def generate_voiceovers():
    print(f"\nGenerating {len(STORY_LINES)} humanized multi-voice dialogue tracks (+18% tempo)...")
    results = []
    
    for item in STORY_LINES:
        voice = VOICE_MAP.get(item["speaker"], "en-US-ChristopherNeural")
        out_file = f"line_{item['id']}.mp3"
        out_path = os.path.join(AUDIO_DIR, out_file)
        
        for attempt in range(3):
            try:
                communicate = edge_tts.Communicate(item["text"], voice, rate="+18%", pitch="+0Hz")
                await communicate.save(out_path)
                break
            except Exception:
                await asyncio.sleep(0.8)
                
        audio = MP3(out_path)
        dur = round(audio.info.length, 2)
        frames = int(dur * 30) + 4 # Fast 4-frame seamless handoff
        
        item["audio_file"] = f"Solo_Max_Level_Newbie/audio/{out_file}"
        item["duration_sec"] = dur
        item["duration_frames"] = frames
        item["pagePath"] = f"Solo_Max_Level_Newbie/chapter_{item['ch']}/panels/{item['panel']}"
        print(f"✔ Line {item['id']} ({item['speaker']:<11}) - {dur:.2f}s -> {item['pagePath']}")
        results.append(item)
        
    manifest_path = os.path.join(AUDIO_DIR, "audio_manifest.json")
    with open(manifest_path, 'w') as f:
        json.dump(results, f, indent=2)
        
    # Generate soloNewbieStoryData.ts
    story_ts_path = "/Users/sandesh/Documents/Manga/my-video/src/soloNewbieStoryData.ts"
    items_ts = []
    for s in results:
        sfx_str = f'"{s["sfx"]}"' if s["sfx"] else 'null'
        items_ts.append(f'''  {{
    id: "{s['id']}",
    act: {s['act']},
    chapter: {s['ch']},
    pagePath: "{s['pagePath']}",
    speaker: "{s['speaker']}",
    motion: "{s['motion']}",
    audioFile: "{s['audio_file']}",
    sfxFile: {sfx_str},
    durationInFrames: {s['duration_frames']},
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
  | "Player";

export interface SoloSceneItem {
  id: string;
  act: number;
  chapter: number;
  pagePath: string;
  speaker: SoloSpeakerType;
  motion: CameraMotion;
  slideDirection?: SlideDirection;
  audioFile: string;
  sfxFile: string | null;
  durationInFrames: number;
}

export const SOLO_SCENES: SoloSceneItem[] = [
''' + ',\n'.join(items_ts) + '\n];\n'

    with open(story_ts_path, 'w') as f:
        f.write(ts_content)

    total_f = sum(s["duration_frames"] for s in results)
    print(f"\n=================================================================")
    print(f"🎉 SOLO MAX-LEVEL NEWBIE STORY ASSETS COMPILED!")
    print(f"Total Scenes: {len(results)} scenes across 15 Chapters")
    print(f"Total Video Runtime: {total_f} frames (~{int(total_f/30//60)}m {int(total_f/30%60):02d}s)")
    print(f"TS Data: {story_ts_path}")
    print("=================================================================")

async def main():
    synth_all_bgm_and_sfx()
    await generate_voiceovers()

if __name__ == "__main__":
    asyncio.run(main())
