import os, asyncio, json
import edge_tts
from mutagen.mp3 import MP3

output_dir = "/Users/sandesh/Documents/Manga/my-video/public/Knights_of_Sidonia/audio"
os.makedirs(output_dir, exist_ok=True)

VOICE_MAP = {
    "Narrator": "en-US-ChristopherNeural",
    "Nagate": "en-US-GuyNeural",
    "Kunato": "en-GB-RyanNeural",
    "Shizuka": "en-US-JennyNeural",
    "Kobayashi": "en-US-AriaNeural",
    "Instructor": "en-US-RogerNeural",
    "Control": "en-US-SteffanNeural",
    "Lala": "en-US-EricNeural",
    "Ochiai": "en-GB-RyanNeural",
    "Cadets": "en-US-AnaNeural",
    "Honoka": "en-US-AnaNeural",
    "Elder": "en-US-SteffanNeural",
    "Worker": "en-US-BrianNeural",
    "Investigator": "en-US-ChristopherNeural",
}

# All 66 scenes across Chapters 1, 2, and 3
all_lines = [
    # CHAPTER 1 (Acts 1-7)
    {"id": "01", "act": 1, "page": 1, "pagePath": "Knights_of_Sidonia/photos/page_001.jpg", "speaker": "Narrator", "motion": "pan-spread-left", "text": "In deep space, humanity is fighting an endless war against monsters known as the Gauna."},
    {"id": "02", "act": 1, "page": 3, "pagePath": "Knights_of_Sidonia/photos/page_003.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "These creatures can regenerate almost instantly. Normal weapons don't even scratch them."},
    {"id": "03", "act": 1, "page": 5, "pagePath": "Knights_of_Sidonia/photos/page_005.jpg", "speaker": "Narrator", "motion": "zoom-top-to-bottom", "text": "The only way to kill one is to pierce its core with a heavy mecha called a Garde."},
    {"id": "04", "act": 1, "page": 7, "pagePath": "Knights_of_Sidonia/photos/page_007.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "One clean hit. Target down."},
    {"id": "05", "act": 1, "page": 9, "pagePath": "Knights_of_Sidonia/photos/page_009.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "Except this wasn't real space. It was an underground simulation pod, piloted by a starving kid named Nagate who held every high score on the ship."},

    {"id": "06", "act": 2, "page": 10, "pagePath": "Knights_of_Sidonia/photos/page_010.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "Nagate grew up completely isolated in the underground tunnels. When his grandfather died three years ago, he was left all on his own."},
    {"id": "07", "act": 2, "page": 12, "pagePath": "Knights_of_Sidonia/photos/page_012.jpg", "speaker": "Nagate", "motion": "scroll-down", "text": "Nothing. There's not a single grain of rice left."},
    {"id": "08", "act": 2, "page": 14, "pagePath": "Knights_of_Sidonia/photos/page_014.jpg", "speaker": "Narrator", "motion": "scroll-up", "text": "Starving after two days without food, Nagate broke his grandfather's strict rule and climbed up the air ducts."},
    {"id": "09", "act": 2, "page": 17, "pagePath": "Knights_of_Sidonia/photos/page_017.jpg", "speaker": "Nagate", "motion": "scroll-down", "text": "Whoa! Oof!"},
    {"id": "10", "act": 2, "page": 17, "pagePath": "Knights_of_Sidonia/photos/page_017.jpg", "speaker": "Narrator", "motion": "pan-spread-left", "text": "He found a massive rice silo, but immediately fell straight into the sorting machine."},

    {"id": "11", "act": 3, "page": 19, "pagePath": "Knights_of_Sidonia/photos/page_019.jpg", "speaker": "Worker", "motion": "scroll-down", "text": "Intruder in Sector 8! It's a rice thief! Grab him!"},
    {"id": "12", "act": 3, "page": 19, "pagePath": "Knights_of_Sidonia/photos/page_019.jpg", "speaker": "Nagate", "motion": "zoom-top-to-bottom", "text": "Wait, please! I'm just hungry!"},
    {"id": "13", "act": 3, "page": 21, "pagePath": "Knights_of_Sidonia/photos/page_021.jpg", "speaker": "Narrator", "motion": "pan-spread-left", "text": "Cornered in the vents, Nagate kicked through a window and tumbled outside."},
    {"id": "14", "act": 3, "page": 23, "pagePath": "Knights_of_Sidonia/photos/page_023.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "For the first time in his life, he saw the city above. But completely out of energy, he passed out on the pavement."},
    {"id": "15", "act": 3, "page": 24, "pagePath": "Knights_of_Sidonia/photos/page_024.jpg", "speaker": "Investigator", "motion": "scroll-down", "text": "Your grandfather died seventeen years ago, and you aren't in any database. Who are you?"},
    {"id": "16", "act": 3, "page": 24, "pagePath": "Knights_of_Sidonia/photos/page_024.jpg", "speaker": "Nagate", "motion": "zoom-top-to-bottom", "text": "Can I stand up? Everything's spinning..."},

    {"id": "17", "act": 4, "page": 25, "pagePath": "Knights_of_Sidonia/photos/page_025.jpg", "speaker": "Ochiai", "motion": "scroll-down", "text": "Two days without food and you faint. Sucks that you can't photosynthesize like the rest of us."},
    {"id": "18", "act": 4, "page": 25, "pagePath": "Knights_of_Sidonia/photos/page_025.jpg", "speaker": "Nagate", "motion": "zoom-top-to-bottom", "text": "Don't turn me into fertilizer!"},
    {"id": "19", "act": 4, "page": 28, "pagePath": "Knights_of_Sidonia/photos/page_028.jpg", "speaker": "Ochiai", "motion": "scroll-down", "text": "Relax. Someone important wants to sponsor you. Name's Ochiai. You got lucky, kid."},
    {"id": "20", "act": 4, "page": 27, "pagePath": "Knights_of_Sidonia/photos/page_027.jpg", "speaker": "Narrator", "motion": "scroll-up", "text": "People on Sidonia produce energy from sunlight, but Nagate is a regular human who needs real food to survive."},
    {"id": "21", "act": 4, "page": 30, "pagePath": "Knights_of_Sidonia/photos/page_030.jpg", "speaker": "Kobayashi", "motion": "scroll-down", "text": "Nagate Tanikaze. Follow me. I have something to show you."},
    {"id": "22", "act": 4, "page": 31, "pagePath": "Knights_of_Sidonia/photos/page_031.jpg", "speaker": "Lala", "motion": "scroll-down", "text": "Here's your room, Nagate. Those clothes stink, so put this uniform on."},
    {"id": "23", "act": 4, "page": 31, "pagePath": "Knights_of_Sidonia/photos/page_031.jpg", "speaker": "Nagate", "motion": "zoom-top-to-bottom", "text": "Wait... you're a talking bear with a robot arm?"},

    {"id": "24", "act": 5, "page": 33, "pagePath": "Knights_of_Sidonia/photos/page_033.jpg", "speaker": "Shizuka", "motion": "scroll-down", "text": "Hey, you're that boy from earlier. What are you doing here?"},
    {"id": "25", "act": 5, "page": 34, "pagePath": "Knights_of_Sidonia/photos/page_034.jpg", "speaker": "Instructor", "motion": "scroll-down", "text": "Hey! Hook your safety belt to the wall rail! If we hit turbulence, you'll fly into the wall and die. Go check every bolt in this hallway!"},
    {"id": "26", "act": 5, "page": 36, "pagePath": "Knights_of_Sidonia/photos/page_036.jpg", "speaker": "Narrator", "motion": "pan-spread-left", "text": "Attached to the wall rail, Nagate followed the line right into an open room."},
    {"id": "27", "act": 5, "page": 37, "pagePath": "Knights_of_Sidonia/photos/page_037.jpg", "speaker": "Cadets", "motion": "scroll-down", "text": "Kyaaa! Pervert! Get out!"},
    {"id": "28", "act": 5, "page": 37, "pagePath": "Knights_of_Sidonia/photos/page_037.jpg", "speaker": "Nagate", "motion": "zoom-top-to-bottom", "text": "Wait! It's a mistake, the belt pulled me in!"},
    {"id": "29", "act": 5, "page": 39, "pagePath": "Knights_of_Sidonia/photos/page_039.jpg", "speaker": "Nagate", "motion": "scroll-down", "text": "Hi everyone. My name is Nagate Tanikaze."},
    {"id": "30", "act": 5, "page": 40, "pagePath": "Knights_of_Sidonia/photos/page_040.jpg", "speaker": "Honoka", "motion": "scroll-down", "text": "Hi everyone? What a weird guy."},

    {"id": "31", "act": 6, "page": 42, "pagePath": "Knights_of_Sidonia/photos/page_042.jpg", "speaker": "Elder", "motion": "scroll-down", "text": "A Gauna cluster has entered our sector, within three light years."},
    {"id": "32", "act": 6, "page": 45, "pagePath": "Knights_of_Sidonia/photos/page_045.jpg", "speaker": "Kobayashi", "motion": "zoom-top-to-bottom", "text": "We can't negotiate with them. If we want to survive, we have to fight."},
    {"id": "33", "act": 6, "page": 46, "pagePath": "Knights_of_Sidonia/photos/page_046.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "The cadets thought the Gauna were just history, but the captain knew the war was starting again."},

    {"id": "34", "act": 7, "page": 47, "pagePath": "Knights_of_Sidonia/photos/page_047.jpg", "speaker": "Narrator", "motion": "pan-spread-left", "text": "This is the starship Sidonia, traveling through deep space a thousand years after Earth was destroyed."},
    {"id": "35", "act": 7, "page": 49, "pagePath": "Knights_of_Sidonia/photos/page_049.jpg", "speaker": "Nagate", "motion": "scroll-up", "text": "So this is what real space looks like."},
    {"id": "36", "act": 7, "page": 50, "pagePath": "Knights_of_Sidonia/photos/page_050.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "Waiting in the hangar was the Type 17 Tsugumori, the legendary mecha his grandfather once flew."},
    {"id": "37", "act": 7, "page": 50, "pagePath": "Knights_of_Sidonia/photos/page_050.jpg", "speaker": "Kobayashi", "motion": "zoom-top-to-bottom", "text": "Will you pilot this machine and protect Sidonia, Nagate?"},
    {"id": "38", "act": 7, "page": 50, "pagePath": "Knights_of_Sidonia/photos/page_050.jpg", "speaker": "Nagate", "motion": "pan-spread-left", "text": "And of course, I said yes. That was the day I became a pilot."},

    # CHAPTER 2 (Acts 8-11)
    {"id": "39", "act": 8, "page": 1, "pagePath": "Knights_of_Sidonia/chapter_2/page_001.jpg", "speaker": "Narrator", "motion": "pan-spread-left", "text": "News spread through Sidonia like wildfire. The legendary Type 17 Tsugumori had been assigned to an unknown rookie."},
    {"id": "40", "act": 8, "page": 3, "pagePath": "Knights_of_Sidonia/chapter_2/page_003.jpg", "speaker": "Kunato", "motion": "scroll-down", "text": "Who do you think you are? That machine belonged to my family's legacy. You don't deserve to sit in that cockpit."},
    {"id": "41", "act": 8, "page": 5, "pagePath": "Knights_of_Sidonia/chapter_2/page_005.jpg", "speaker": "Nagate", "motion": "zoom-top-to-bottom", "text": "I didn't ask for it. But my grandfather taught me how to fly it, and I won't back down."},
    {"id": "42", "act": 8, "page": 7, "pagePath": "Knights_of_Sidonia/chapter_2/page_007.jpg", "speaker": "Shizuka", "motion": "scroll-down", "text": "Don't let him get to you, Nagate. Out in space, your skills are the only thing that matters."},

    {"id": "43", "act": 9, "page": 9, "pagePath": "Knights_of_Sidonia/chapter_2/page_009.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "Inside the hangar, Nagate stepped into the pressurized cockpit of the Tsugumori and locked the neuro-link harness."},
    {"id": "44", "act": 9, "page": 12, "pagePath": "Knights_of_Sidonia/chapter_2/page_012.jpg", "speaker": "Control", "motion": "zoom-top-to-bottom", "text": "Garde 17 Tsugumori, all systems green. Pressure seals locked. Electromagnetic catapult standing by."},
    {"id": "45", "act": 9, "page": 15, "pagePath": "Knights_of_Sidonia/chapter_2/page_015.jpg", "speaker": "Instructor", "motion": "scroll-up", "text": "Catapult clearance confirmed! Squad 4, launch in three, two, one, clear!"},
    {"id": "46", "act": 9, "page": 18, "pagePath": "Knights_of_Sidonia/chapter_2/page_018.jpg", "speaker": "Nagate", "motion": "pan-spread-left", "text": "Tanikaze, Tsugumori... launching!"},

    {"id": "47", "act": 10, "page": 20, "pagePath": "Knights_of_Sidonia/chapter_2/page_020.jpg", "speaker": "Narrator", "motion": "pan-spread-left", "text": "Shooting out from Sidonia's massive hull, the squad formed up in the vacuum of space, heading toward an ice mining asteroid."},
    {"id": "48", "act": 10, "page": 22, "pagePath": "Knights_of_Sidonia/chapter_2/page_022.jpg", "speaker": "Shizuka", "motion": "scroll-down", "text": "Nagate, your flight line is rock solid. It's like you've been flying in real zero-G your whole life."},
    {"id": "49", "act": 10, "page": 25, "pagePath": "Knights_of_Sidonia/chapter_2/page_025.jpg", "speaker": "Kunato", "motion": "zoom-top-to-bottom", "text": "Stay focused on the mining perimeter. Don't slow us down, rookie."},

    {"id": "50", "act": 11, "page": 28, "pagePath": "Knights_of_Sidonia/chapter_2/page_028.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "Without warning, deep space gravity wave sensors on Sidonia lit up in violent red."},
    {"id": "51", "act": 11, "page": 30, "pagePath": "Knights_of_Sidonia/chapter_2/page_030.jpg", "speaker": "Control", "motion": "zoom-top-to-bottom", "text": "Warning! Massive gravity distortion detected in Sector 4! It's right on top of the mining asteroid!"},
    {"id": "52", "act": 11, "page": 32, "pagePath": "Knights_of_Sidonia/chapter_2/page_032.jpg", "speaker": "Kobayashi", "motion": "scroll-down", "text": "All units, battle stations immediately! A Gauna has appeared!"},

    # CHAPTER 3 (Acts 12-15)
    {"id": "53", "act": 12, "page": 1, "pagePath": "Knights_of_Sidonia/chapter_3/page_001.jpg", "speaker": "Narrator", "motion": "pan-spread-left", "text": "The asteroid cracked open, and a towering Gauna unfurled its massive biological tentacles into the void."},
    {"id": "54", "act": 12, "page": 4, "pagePath": "Knights_of_Sidonia/chapter_3/page_004.jpg", "speaker": "Shizuka", "motion": "scroll-down", "text": "It's huge! Break formation! Evacuate the mining crews!"},
    {"id": "55", "act": 12, "page": 7, "pagePath": "Knights_of_Sidonia/chapter_3/page_007.jpg", "speaker": "Kunato", "motion": "zoom-top-to-bottom", "text": "Open fire with heavy particle cannons! Concentrate fire on the upper mass!"},
    {"id": "56", "act": 12, "page": 10, "pagePath": "Knights_of_Sidonia/chapter_3/page_010.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "Particle beams blasted into the monster, but the placenta flesh regenerated instantly, brushing off the assault."},

    {"id": "57", "act": 13, "page": 13, "pagePath": "Knights_of_Sidonia/chapter_3/page_013.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "A colossal tentacle whipped across space, striking one of the cadet Gardes and sending it hurtling into the abyss."},
    {"id": "58", "act": 13, "page": 16, "pagePath": "Knights_of_Sidonia/chapter_3/page_016.jpg", "speaker": "Shizuka", "motion": "zoom-top-to-bottom", "text": "Cadet unit down! We can't pierce its armor with standard weapons!"},
    {"id": "59", "act": 13, "page": 19, "pagePath": "Knights_of_Sidonia/chapter_3/page_019.jpg", "speaker": "Kobayashi", "motion": "scroll-down", "text": "Only the Kabizashi spear can destroy the true core! Pilot Tanikaze, you are authorized to strike!"},

    {"id": "60", "act": 14, "page": 21, "pagePath": "Knights_of_Sidonia/chapter_3/page_021.jpg", "speaker": "Nagate", "motion": "pan-spread-left", "text": "I see the core pattern! Full thrusters... override!"},
    {"id": "61", "act": 14, "page": 24, "pagePath": "Knights_of_Sidonia/chapter_3/page_024.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "Executing an impossible high-G booster turn, Nagate dodged a barrage of tentacles, diving straight into the monster's blind spot."},
    {"id": "62", "act": 14, "page": 27, "pagePath": "Knights_of_Sidonia/chapter_3/page_027.jpg", "speaker": "Kunato", "motion": "zoom-top-to-bottom", "text": "What kind of insane maneuver is that?! He's moving faster than the simulator limits!"},

    {"id": "63", "act": 15, "page": 29, "pagePath": "Knights_of_Sidonia/chapter_3/page_029.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "Drawing the heavy Kabizashi spear, the Type 17 Tsugumori drove its blade directly into the Gauna's pulsating heart."},
    {"id": "64", "act": 15, "page": 31, "pagePath": "Knights_of_Sidonia/chapter_3/page_031.jpg", "speaker": "Nagate", "motion": "zoom-top-to-bottom", "text": "Core pierced! Break apart!"},
    {"id": "65", "act": 15, "page": 33, "pagePath": "Knights_of_Sidonia/chapter_3/page_033.jpg", "speaker": "Narrator", "motion": "pan-spread-left", "text": "The leviathan dissolved into glittering space particles. Nagate Tanikaze had won his first true battle in the cosmos."},
    {"id": "66", "act": 15, "page": 34, "pagePath": "Knights_of_Sidonia/chapter_3/page_034.jpg", "speaker": "Shizuka", "motion": "scroll-down", "text": "You actually did it, Nagate... you saved us all."}
]

async def process_line(item):
    voice = VOICE_MAP.get(item["speaker"], "en-US-ChristopherNeural")
    out_file = f"line_{item['id']}.mp3"
    out_path = os.path.join(output_dir, out_file)
    
    # Generate energetic fast-paced speech (+18% speech rate)
    for attempt in range(3):
        try:
            communicate = edge_tts.Communicate(item["text"], voice, rate="+18%", pitch="+0Hz")
            await communicate.save(out_path)
            break
        except Exception:
            await asyncio.sleep(0.8)
            
    audio = MP3(out_path)
    dur = round(audio.info.length, 2)
    
    # Super tight padding: only 3 frames (~0.10s) between scenes for rapid pacing
    frames = int(dur * 30) + 3
    
    item["audio_file"] = f"Knights_of_Sidonia/audio/{out_file}"
    item["duration_sec"] = dur
    item["duration_frames"] = frames
    print(f"[{item['id']}/66] {item['speaker']:<12}: {dur:.2f}s ({frames} frames) -> \"{item['text'][:40]}...\"")
    return item

async def main():
    print("Rebuilding all 66 voiceovers with fast pacing (+18% rate, tight 3-frame gaps)...")
    results = []
    for line in all_lines:
        res = await process_line(line)
        results.append(res)
        
    # Save full manifest
    manifest_path = "/Users/sandesh/Documents/Manga/my-video/public/Knights_of_Sidonia/audio_manifest_full.json"
    with open(manifest_path, 'w') as f:
        json.dump(results, f, indent=2)
        
    # Also save as audio_manifest.json for compatibility
    with open("/Users/sandesh/Documents/Manga/my-video/public/Knights_of_Sidonia/audio_manifest.json", 'w') as f:
        json.dump(results[:38], f, indent=2)
        
    # Update storyData.ts
    story_path = "/Users/sandesh/Documents/Manga/my-video/src/storyData.ts"
    items_ts = []
    for item in results:
        items_ts.append(f'''  {{
    id: "{item['id']}",
    act: {item['act']},
    page: {item['page']},
    pagePath: "{item['pagePath']}",
    speaker: "{item['speaker']}",
    motion: "{item['motion']}",
    audioFile: "{item['audio_file']}",
    durationInFrames: {item['duration_frames']},
  }}''')

    content = '''import { SceneItem } from "./types";

export const SCENES: SceneItem[] = [
''' + ',\n'.join(items_ts) + '\n];\n'

    with open(story_path, 'w') as f:
        f.write(content)

    total_frames = sum(s['duration_frames'] for s in results)
    total_sec = total_frames / 30.0
    print(f"\n=======================================================")
    print(f"Fast Pacing Applied Successfully across all 66 scenes!")
    print(f"Total Video Runtime: {total_frames} frames (~{int(total_sec//60)}m {int(total_sec%60):02d}s)")
    print(f"=======================================================")

if __name__ == "__main__":
    asyncio.run(main())
