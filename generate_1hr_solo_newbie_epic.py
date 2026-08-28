import os, sys, math, struct, wave, asyncio, json
import edge_tts
from mutagen.mp3 import MP3

AUDIO_DIR = "/Users/sandesh/Documents/Manga/my-video/public/Solo_Max_Level_Newbie/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

VOICE_MAP = {
    "Narrator": "en-US-ChristopherNeural",
    "Jinhyuk": "en-US-GuyNeural",
    "Teresa": "en-US-JennyNeural",
    "System": "en-US-AriaNeural",
    "GuildMaster": "en-GB-RyanNeural",
    "Cheon": "en-US-RogerNeural",
    "Merchant": "en-US-BrianNeural",
    "Player": "en-US-SteffanNeural",
    "SwordMaster": "en-US-EricNeural"
}

# 25 ACTS COVERING ALL 25 CHAPTERS FOR THE 1-HOUR VIDEO RECAP SAGA
FULL_SAGA_LINES = [
    # CHAPTER 1: THE IMPOSSIBLE CLEAR (Act 1)
    {"id": "001", "act": 1, "ch": 1, "panel": "panel_001.jpg", "speaker": "Narrator", "motion": "pan-spread-left", "text": "For eleven solid years, the hyper-realistic VR game 'Tower of Trials' drove millions of players to complete despair."},
    {"id": "002", "act": 1, "ch": 1, "panel": "panel_005.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "Its absurd difficulty made every single guild quit. Everyone, except for a solitary gaming Nutuber named Jinhyuk Kang."},
    {"id": "003", "act": 1, "ch": 1, "panel": "panel_012.jpg", "speaker": "Jinhyuk", "motion": "zoom-top-to-bottom", "text": "Eleven years of grinding. Finally... the final floor is cleared. Game over."},
    {"id": "004", "act": 1, "ch": 1, "panel": "panel_020.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "Jinhyuk uploaded his ending walkthrough video to celebrate, planning to retire and find a normal job."},
    {"id": "005", "act": 1, "ch": 1, "panel": "panel_032.jpg", "speaker": "System", "motion": "zoom-top-to-bottom", "text": "Notice. The Tower of Trials service has concluded. Rebooting reality to match game parameters in three, two, one."},
    {"id": "006", "act": 1, "ch": 1, "panel": "panel_042.jpg", "speaker": "Narrator", "motion": "pan-spread-left", "text": "A colossal black spire thousands of meters high pierced the sky over the city. The game was now real life."},

    # CHAPTER 2: SECRET CLASS AWAKENING (Act 2)
    {"id": "007", "act": 2, "ch": 2, "panel": "panel_002.jpg", "speaker": "System", "motion": "scroll-down", "text": "Player Kang Jinhyuk identified. You are the sole survivor who witnessed the ending. Hidden class 'Unknown' granted."},
    {"id": "008", "act": 2, "ch": 2, "panel": "panel_015.jpg", "speaker": "Jinhyuk", "motion": "zoom-top-to-bottom", "text": "Class Unknown? And my innate ability is the 'Eyes of Gluttony'?! I can copy and steal any target's skills!"},
    {"id": "009", "act": 2, "ch": 2, "panel": "panel_030.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "While regular players panicked in the streets, Jinhyuk packed his survival gear and headed straight toward the Tower entrance."},
    {"id": "010", "act": 2, "ch": 2, "panel": "panel_045.jpg", "speaker": "Jinhyuk", "motion": "pan-spread-left", "text": "Everyone else is starting at level one with no information. But I already know every secret in this world."},

    # CHAPTER 3: FLOOR 1 CATACOMBS (Act 3)
    {"id": "011", "act": 3, "ch": 3, "panel": "panel_008.jpg", "speaker": "Narrator", "motion": "pan-spread-left", "text": "Stepping onto the first floor, Jinhyuk bypassed the crowded starter plains and dived into the subterranean catacombs."},
    {"id": "012", "act": 3, "ch": 3, "panel": "panel_024.jpg", "speaker": "Jinhyuk", "motion": "scroll-down", "text": "These skeletons only spawn on a three-minute timer. Hit the joint, steal their bone armor buff, and keep moving."},
    {"id": "013", "act": 3, "ch": 3, "panel": "panel_045.jpg", "speaker": "Narrator", "motion": "zoom-top-to-bottom", "text": "Executing precise beta-test combos, he leveled up four times faster than any party on the surface."},

    # CHAPTER 4: RELIC OF THE DRAGON (Act 4)
    {"id": "014", "act": 4, "ch": 4, "panel": "panel_018.jpg", "speaker": "Narrator", "motion": "zoom-top-to-bottom", "text": "Behind a hidden illusory wall, he retrieved the ancient relic dagger: the Fang of the Black Dragon."},
    {"id": "015", "act": 4, "ch": 4, "panel": "panel_042.jpg", "speaker": "Player", "motion": "scroll-down", "text": "Hey kid! Hand over whatever you found in that chest if you want to leave here in one piece!"},
    {"id": "016", "act": 4, "ch": 4, "panel": "panel_055.jpg", "speaker": "Jinhyuk", "motion": "zoom-top-to-bottom", "text": "You picked the wrong rookie to rob. Eyes of Gluttony... skill extracted!"},

    # CHAPTER 5: HALL OF TRIALS (Act 5)
    {"id": "017", "act": 5, "ch": 5, "panel": "panel_012.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "Reaching the Hall of Trials, the floor was lined with lethal flame traps and moving spike pendulums."},
    {"id": "018", "act": 5, "ch": 5, "panel": "panel_035.jpg", "speaker": "Jinhyuk", "motion": "pan-spread-left", "text": "Two steps forward, dodge right on the third pulse. I ran this dungeon a thousand times in the beta."},

    # CHAPTER 6: FIRST FLOOR BOSS AELGOTH (Act 6)
    {"id": "019", "act": 6, "ch": 6, "panel": "panel_005.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "At the summit of Floor 1, the gate guardian Aelgoth emerged, roaring with blazing infernal energy."},
    {"id": "020", "act": 6, "ch": 6, "panel": "panel_028.jpg", "speaker": "Jinhyuk", "motion": "zoom-top-to-bottom", "text": "Your attack pattern has a two-second recovery opening. Strike the left knee crystal!"},
    {"id": "021", "act": 6, "ch": 6, "panel": "panel_050.jpg", "speaker": "Narrator", "motion": "pan-spread-left", "text": "With a single surgical strike, the boss collapsed, shattering into thousands of glowing soul shards."},

    # CHAPTER 7: WORLD FIRST BROADCAST (Act 7)
    {"id": "022", "act": 7, "ch": 7, "panel": "panel_008.jpg", "speaker": "System", "motion": "zoom-top-to-bottom", "text": "World Announcement! Player Kang Jinhyuk has achieved the solo first clear of Floor 1! Title 'Pioneer of the Tower' bestowed!"},
    {"id": "023", "act": 7, "ch": 7, "panel": "panel_035.jpg", "speaker": "GuildMaster", "motion": "scroll-down", "text": "Who the hell is Kang Jinhyuk?! Find him immediately and recruit him to the guild at any cost!"},

    # CHAPTER 8: VAMPIRE LORD SANCTUARY (Act 8)
    {"id": "024", "act": 8, "ch": 8, "panel": "panel_005.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "Ascending to the second floor, Jinhyuk stepped into the fog-shrouded Labyrinth of the Vampire Lord."},
    {"id": "025", "act": 8, "ch": 8, "panel": "panel_028.jpg", "speaker": "Teresa", "motion": "zoom-top-to-bottom", "text": "Halt! You cannot enter the inner sanctuary. The sealed blood lord is awakening!"},
    {"id": "026", "act": 8, "ch": 8, "panel": "panel_050.jpg", "speaker": "Jinhyuk", "motion": "scroll-down", "text": "Saintess Teresa de Laurent. I know why your holy magic is suppressed here. Follow my lead if you want to survive."},

    # CHAPTER 9: BLOOD OATH FAMILIAR (Act 9)
    {"id": "027", "act": 9, "ch": 9, "panel": "panel_018.jpg", "speaker": "Cheon", "motion": "scroll-down", "text": "Insolent mortals! You dare disturb the slumber of ancient noble blood?!"},
    {"id": "028", "act": 9, "ch": 9, "panel": "panel_045.jpg", "speaker": "Jinhyuk", "motion": "zoom-top-to-bottom", "text": "Eyes of Gluttony: Blood Oath Override! You're not my enemy anymore... you're my familiar!"},
    {"id": "029", "act": 9, "ch": 9, "panel": "panel_065.jpg", "speaker": "Narrator", "motion": "pan-spread-left", "text": "Taming the legendary vampire noble, Jinhyuk gained full control over the second floor's ancient blood domain."},

    # CHAPTER 10: TRIAD GUILD MONOPOLY (Act 10)
    {"id": "030", "act": 10, "ch": 10, "panel": "panel_012.jpg", "speaker": "GuildMaster", "motion": "scroll-down", "text": "This gate belongs to the Triad Alliance! Every solo player must pay an eighty percent tribute tax to pass!"},
    {"id": "031", "act": 10, "ch": 10, "panel": "panel_040.jpg", "speaker": "Jinhyuk", "motion": "zoom-top-to-bottom", "text": "A tribute tax? In a game I cleared eleven years ago? Get out of my way before I clear your entire squad."},

    # CHAPTER 11: FLOOR 3 IRON FORTRESS (Act 11)
    {"id": "032", "act": 11, "ch": 11, "panel": "panel_022.jpg", "speaker": "Narrator", "motion": "pan-spread-left", "text": "Entering Floor 3's Iron Fortress, Jinhyuk dismantled twenty elite armored golems in under two minutes."},
    {"id": "033", "act": 11, "ch": 11, "panel": "panel_055.jpg", "speaker": "Jinhyuk", "motion": "scroll-down", "text": "Targeting their mana conduits instantly disables their heavy armor plates."},

    # CHAPTER 12: SECRET BLACK MARKET (Act 12)
    {"id": "034", "act": 12, "ch": 12, "panel": "panel_015.jpg", "speaker": "Merchant", "motion": "scroll-down", "text": "Welcome to the secret exchange, customer. How did a beginner find the underground password?"},
    {"id": "035", "act": 12, "ch": 12, "panel": "panel_045.jpg", "speaker": "Jinhyuk", "motion": "zoom-top-to-bottom", "text": "Give me the Ice Queen's antidote vial and three high-grade mana cores. Keep the change."},

    # CHAPTER 13: FROST PEAKS VANGUARD (Act 13)
    {"id": "036", "act": 13, "ch": 13, "panel": "panel_005.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "At Floor 4's Frost Peaks, howling blizzards froze the wings of advancing vanguard beasts."},
    {"id": "037", "act": 13, "ch": 13, "panel": "panel_035.jpg", "speaker": "Jinhyuk", "motion": "pan-spread-left", "text": "The Minotaur guardian has entered Berserk mode! Almost there... the moment he reveals his core...!"},

    # CHAPTER 14: EYES OF GLUTTONY TRIGGER (Act 14)
    {"id": "038", "act": 14, "ch": 14, "panel": "panel_010.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "Dodging the crushing horns by millimeters, Jinhyuk activated his legendary innate ability."},
    {"id": "039", "act": 14, "ch": 14, "panel": "panel_045.jpg", "speaker": "Jinhyuk", "motion": "zoom-top-to-bottom", "text": "Eyes of Gluttony: Target Locked! Extracting innate skill: Absolute Glacial Armor!"},
    {"id": "040", "act": 14, "ch": 14, "panel": "panel_075.jpg", "speaker": "System", "motion": "pan-spread-left", "text": "Skill successfully copied! Ice resistance increased by five hundred percent!"},

    # CHAPTER 15: FLOOR 4 CLIMAX (Act 15)
    {"id": "041", "act": 15, "ch": 15, "panel": "panel_025.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "Coated in unstoppable frost armor, the Black Dragon Fang sliced through the monster's heart in a single clean sweep."},
    {"id": "042", "act": 15, "ch": 15, "panel": "panel_060.jpg", "speaker": "System", "motion": "zoom-top-to-bottom", "text": "Floor 4 Cleared! Total rank across all active players: Number One!"},

    # CHAPTER 16: FLOOR 5 ANCIENT JUNGLE (Act 16)
    {"id": "043", "act": 16, "ch": 16, "panel": "panel_010.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "Floor 5 opened into a colossal primordial jungle teeming with poisonous venomous flora and ancient predators."},
    {"id": "044", "act": 16, "ch": 16, "panel": "panel_045.jpg", "speaker": "Jinhyuk", "motion": "zoom-top-to-bottom", "text": "The toxic mist deals percentage health damage every second, but consuming the silver lotus roots grants total immunity."},

    # CHAPTER 17: SWORD MASTER DUEL (Act 17)
    {"id": "045", "act": 17, "ch": 17, "panel": "panel_020.jpg", "speaker": "SwordMaster", "motion": "pan-spread-left", "text": "I've waited on this floor for a worthy opponent. Draw your blade, rookie!"},
    {"id": "046", "act": 17, "ch": 17, "panel": "panel_060.jpg", "speaker": "Jinhyuk", "motion": "zoom-top-to-bottom", "text": "Your stance favors heavy overhead thrusts. Eyes of Gluttony: Stance Copied!"},

    # CHAPTER 18: SECRET CAVE OF HEPHAESTUS (Act 18)
    {"id": "047", "act": 18, "ch": 18, "panel": "panel_015.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "Diving under a subterranean waterfall, Jinhyuk discovered the legendary forge of the blacksmith gods."},
    {"id": "048", "act": 18, "ch": 18, "panel": "panel_045.jpg", "speaker": "Jinhyuk", "motion": "zoom-top-to-bottom", "text": "Combining dragon fang alloy with eternal flame... the Divine Dragon Blade is complete."},

    # CHAPTER 19: MEGA-GUILD ALLIANCE RAID (Act 19)
    {"id": "049", "act": 19, "ch": 19, "panel": "panel_025.jpg", "speaker": "GuildMaster", "motion": "scroll-down", "text": "All hundred top rankers from five global guilds are here! There's no way one solo player can steal this boss!"},
    {"id": "050", "act": 19, "ch": 19, "panel": "panel_070.jpg", "speaker": "Jinhyuk", "motion": "zoom-top-to-bottom", "text": "You brought a hundred players, but none of you memorized the boss's elemental shift timer. Watch and learn."},

    # CHAPTER 20: TOWER FLOOR 6 ASCENT (Act 20)
    {"id": "051", "act": 20, "ch": 20, "panel": "panel_030.jpg", "speaker": "Narrator", "motion": "pan-spread-left", "text": "Triggering the hidden cascade reaction, Jinhyuk claimed all five guild bounty chests simultaneously."},
    {"id": "052", "act": 20, "ch": 20, "panel": "panel_080.jpg", "speaker": "System", "motion": "zoom-top-to-bottom", "text": "Player Kang Jinhyuk has claimed undisputed dominance of Floor 6! Global reputation rating: Mythic!"},

    # CHAPTER 21-22: TOWER DOMAIN REVELATION (Act 21)
    {"id": "053", "act": 21, "ch": 21, "panel": "panel_020.jpg", "speaker": "Teresa", "motion": "scroll-down", "text": "Jinhyuk... the higher floors are collapsing into reality itself. Only you know how this world ends."},
    {"id": "054", "act": 21, "ch": 22, "panel": "panel_045.jpg", "speaker": "Jinhyuk", "motion": "zoom-top-to-bottom", "text": "The ending of the Tower of Trials wasn't victory. It was a complete reset. And I'm going to change that ending."},

    # CHAPTER 23-25: ULTIMATE CLIMAX & FUTURE BATTLES (Act 22)
    {"id": "055", "act": 22, "ch": 23, "panel": "panel_015.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "With the Divine Dragon Blade in hand and the Eyes of Gluttony fully evolved, Jinhyuk stood atop the world ranker leaderboard."},
    {"id": "056", "act": 22, "ch": 24, "panel": "panel_030.jpg", "speaker": "Jinhyuk", "motion": "zoom-top-to-bottom", "text": "To every guild and every god watching from the top floor: come at me with everything you've got."},
    {"id": "057", "act": 22, "ch": 25, "panel": "panel_050.jpg", "speaker": "Narrator", "motion": "pan-spread-left", "text": "The solo max-level newbie had claimed his throne. And humanity's true climb up the Tower of Trials had only just begun."}
]

async def generate_full_epic_saga():
    print(f"Generating full 25-chapter epic story audio ({len(FULL_SAGA_LINES)} narrative beats)...")
    results = []
    
    for item in FULL_SAGA_LINES:
        voice = VOICE_MAP.get(item["speaker"], "en-US-ChristopherNeural")
        out_file = f"epic_line_{item['id']}.mp3"
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
        frames = int(dur * 30) + 4
        
        item["audio_file"] = f"Solo_Max_Level_Newbie/audio/{out_file}"
        item["duration_sec"] = dur
        item["duration_frames"] = frames
        item["pagePath"] = f"Solo_Max_Level_Newbie/chapter_{item['ch']}/panels/{item['panel']}"
        print(f"✔ Line {item['id']} ({item['speaker']:<11}) - {dur:.2f}s -> {item['pagePath']}")
        results.append(item)
        
    # Generate complete soloNewbieStoryData.ts
    story_ts_path = "/Users/sandesh/Documents/Manga/my-video/src/soloNewbieStoryData.ts"
    items_ts = []
    for s in results:
        items_ts.append(f'''  {{
    id: "{s['id']}",
    act: {s['act']},
    chapter: {s['ch']},
    pagePath: "{s['pagePath']}",
    speaker: "{s['speaker']}",
    motion: "{s['motion']}",
    audioFile: "{s['audio_file']}",
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

    with open(story_ts_path, 'w') as f:
        f.write(ts_content)

    total_f = sum(s["duration_frames"] for s in results)
    print(f"\n=================================================================")
    print(f"🎉 25-CHAPTER EPIC SAGA COMPILED SUCCESSFULLY!")
    print(f"Total Scenes: {len(results)} scenes across Chapters 1-25")
    print(f"Total Video Frames: {total_f} frames (~{int(total_f/30//60)}m {int(total_f/30%60):02d}s)")
    print(f"=================================================================")

if __name__ == "__main__":
    asyncio.run(generate_full_epic_saga())
