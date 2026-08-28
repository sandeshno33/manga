import os, wave, asyncio, json, time
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
}

extra_lines = [
    # CHAPTER 2: FIRST SORTIE (Acts 8 - 11)
    {"id": "39", "act": 8, "page": 1, "ch": 2, "pagePath": "Knights_of_Sidonia/chapter_2/page_001.jpg", "speaker": "Narrator", "motion": "pan-spread-left", "text": "News spread through Sidonia like wildfire. The legendary Type 17 Tsugumori had been assigned to an unknown rookie."},
    {"id": "40", "act": 8, "page": 3, "ch": 2, "pagePath": "Knights_of_Sidonia/chapter_2/page_003.jpg", "speaker": "Kunato", "motion": "scroll-down", "text": "Who do you think you are? That machine belonged to my family's legacy. You don't deserve to sit in that cockpit."},
    {"id": "41", "act": 8, "page": 5, "ch": 2, "pagePath": "Knights_of_Sidonia/chapter_2/page_005.jpg", "speaker": "Nagate", "motion": "zoom-top-to-bottom", "text": "I didn't ask for it. But my grandfather taught me how to fly it, and I won't back down."},
    {"id": "42", "act": 8, "page": 7, "ch": 2, "pagePath": "Knights_of_Sidonia/chapter_2/page_007.jpg", "speaker": "Shizuka", "motion": "scroll-down", "text": "Don't let him get to you, Nagate. Out in space, your skills are the only thing that matters."},
    {"id": "43", "act": 9, "page": 9, "ch": 2, "pagePath": "Knights_of_Sidonia/chapter_2/page_009.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "Inside the hangar, Nagate stepped into the pressurized cockpit of the Tsugumori and locked the neuro-link harness."},
    {"id": "44", "act": 9, "page": 12, "ch": 2, "pagePath": "Knights_of_Sidonia/chapter_2/page_012.jpg", "speaker": "Control", "motion": "zoom-top-to-bottom", "text": "Garde 17 Tsugumori, all systems green. Pressure seals locked. Electromagnetic catapult standing by."},
    {"id": "45", "act": 9, "page": 15, "ch": 2, "pagePath": "Knights_of_Sidonia/chapter_2/page_015.jpg", "speaker": "Instructor", "motion": "scroll-up", "text": "Catapult clearance confirmed! Squad 4, launch in three, two, one, clear!"},
    {"id": "46", "act": 9, "page": 18, "ch": 2, "pagePath": "Knights_of_Sidonia/chapter_2/page_018.jpg", "speaker": "Nagate", "motion": "pan-spread-left", "text": "Tanikaze, Tsugumori... launching!"},
    {"id": "47", "act": 10, "page": 20, "ch": 2, "pagePath": "Knights_of_Sidonia/chapter_2/page_020.jpg", "speaker": "Narrator", "motion": "pan-spread-left", "text": "Shooting out from Sidonia's massive hull, the squad formed up in the vacuum of space, heading toward an ice mining asteroid."},
    {"id": "48", "act": 10, "page": 22, "ch": 2, "pagePath": "Knights_of_Sidonia/chapter_2/page_022.jpg", "speaker": "Shizuka", "motion": "scroll-down", "text": "Nagate, your flight line is rock solid. It's like you've been flying in real zero-G your whole life."},
    {"id": "49", "act": 10, "page": 25, "ch": 2, "pagePath": "Knights_of_Sidonia/chapter_2/page_025.jpg", "speaker": "Kunato", "motion": "zoom-top-to-bottom", "text": "Stay focused on the mining perimeter. Don't slow us down, rookie."},
    {"id": "50", "act": 11, "page": 28, "ch": 2, "pagePath": "Knights_of_Sidonia/chapter_2/page_028.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "Without warning, deep space gravity wave sensors on Sidonia lit up in violent red."},
    {"id": "51", "act": 11, "page": 30, "ch": 2, "pagePath": "Knights_of_Sidonia/chapter_2/page_030.jpg", "speaker": "Control", "motion": "zoom-top-to-bottom", "text": "Warning! Massive gravity distortion detected in Sector 4! It's right on top of the mining asteroid!"},
    {"id": "52", "act": 11, "page": 32, "ch": 2, "pagePath": "Knights_of_Sidonia/chapter_2/page_032.jpg", "speaker": "Kobayashi", "motion": "scroll-down", "text": "All units, battle stations immediately! A Gauna has appeared!"},

    # CHAPTER 3: GAUNA CONTACT & FIRST COMBAT (Acts 12 - 15)
    {"id": "53", "act": 12, "page": 1, "ch": 3, "pagePath": "Knights_of_Sidonia/chapter_3/page_001.jpg", "speaker": "Narrator", "motion": "pan-spread-left", "text": "The asteroid cracked open, and a towering Gauna unfurled its massive biological tentacles into the void."},
    {"id": "54", "act": 12, "page": 4, "ch": 3, "pagePath": "Knights_of_Sidonia/chapter_3/page_004.jpg", "speaker": "Shizuka", "motion": "scroll-down", "text": "It's huge! Break formation! Evacuate the mining crews!"},
    {"id": "55", "act": 12, "page": 7, "ch": 3, "pagePath": "Knights_of_Sidonia/chapter_3/page_007.jpg", "speaker": "Kunato", "motion": "zoom-top-to-bottom", "text": "Open fire with heavy particle cannons! Concentrate fire on the upper mass!"},
    {"id": "56", "act": 12, "page": 10, "ch": 3, "pagePath": "Knights_of_Sidonia/chapter_3/page_010.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "Particle beams blasted into the monster, but the placenta flesh regenerated instantly, brushing off the assault."},
    {"id": "57", "act": 13, "page": 13, "ch": 3, "pagePath": "Knights_of_Sidonia/chapter_3/page_013.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "A colossal tentacle whipped across space, striking one of the cadet Gardes and sending it hurtling into the abyss."},
    {"id": "58", "act": 13, "page": 16, "ch": 3, "pagePath": "Knights_of_Sidonia/chapter_3/page_016.jpg", "speaker": "Shizuka", "motion": "zoom-top-to-bottom", "text": "Cadet unit down! We can't pierce its armor with standard weapons!"},
    {"id": "59", "act": 13, "page": 19, "ch": 3, "pagePath": "Knights_of_Sidonia/chapter_3/page_019.jpg", "speaker": "Kobayashi", "motion": "scroll-down", "text": "Only the Kabizashi spear can destroy the true core! Pilot Tanikaze, you are authorized to strike!"},
    {"id": "60", "act": 14, "page": 21, "ch": 3, "pagePath": "Knights_of_Sidonia/chapter_3/page_021.jpg", "speaker": "Nagate", "motion": "pan-spread-left", "text": "I see the core pattern! Full thrusters... override!"},
    {"id": "61", "act": 14, "page": 24, "ch": 3, "pagePath": "Knights_of_Sidonia/chapter_3/page_024.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "Executing an impossible high-G booster turn, Nagate dodged a barrage of tentacles, diving straight into the monster's blind spot."},
    {"id": "62", "act": 14, "page": 27, "ch": 3, "pagePath": "Knights_of_Sidonia/chapter_3/page_027.jpg", "speaker": "Kunato", "motion": "zoom-top-to-bottom", "text": "What kind of insane maneuver is that?! He's moving faster than the simulator limits!"},
    {"id": "63", "act": 15, "page": 29, "ch": 3, "pagePath": "Knights_of_Sidonia/chapter_3/page_029.jpg", "speaker": "Narrator", "motion": "scroll-down", "text": "Drawing the heavy Kabizashi spear, the Type 17 Tsugumori drove its blade directly into the Gauna's pulsating heart."},
    {"id": "64", "act": 15, "page": 31, "ch": 3, "pagePath": "Knights_of_Sidonia/chapter_3/page_031.jpg", "speaker": "Nagate", "motion": "zoom-top-to-bottom", "text": "Core pierced! Break apart!"},
    {"id": "65", "act": 15, "page": 33, "ch": 3, "pagePath": "Knights_of_Sidonia/chapter_3/page_033.jpg", "speaker": "Narrator", "motion": "pan-spread-left", "text": "The leviathan dissolved into glittering space particles. Nagate Tanikaze had won his first true battle in the cosmos."},
    {"id": "66", "act": 15, "page": 34, "ch": 3, "pagePath": "Knights_of_Sidonia/chapter_3/page_034.jpg", "speaker": "Shizuka", "motion": "scroll-down", "text": "You actually did it, Nagate... you saved us all."}
]

async def generate_all():
    results = []
    print(f"Generating {len(extra_lines)} dialogue tracks for Chapters 2 & 3...")
    for item in extra_lines:
        voice = VOICE_MAP.get(item["speaker"], "en-US-ChristopherNeural")
        out_file = f"line_{item['id']}.mp3"
        out_path = os.path.join(output_dir, out_file)
        
        if not (os.path.exists(out_path) and os.path.getsize(out_path) > 3000):
            for attempt in range(3):
                try:
                    communicate = edge_tts.Communicate(item["text"], voice, rate="+2%", pitch="+0Hz")
                    await communicate.save(out_path)
                    break
                except Exception as e:
                    if attempt == 2:
                        print(f"Error on line {item['id']}: {e}")
                    await asyncio.sleep(1.0)
        
        audio = MP3(out_path)
        dur = round(audio.info.length, 2)
        frames = max(45, int(dur * 30))
        
        item["audio_file"] = f"Knights_of_Sidonia/audio/{out_file}"
        item["duration_sec"] = dur
        item["duration_frames"] = frames + 16
        print(f"✔ Line {item['id']} ({item['speaker']}) - {dur:.2f}s: \"{item['text']}\"")
        results.append(item)
        
    ch1_manifest_path = "/Users/sandesh/Documents/Manga/my-video/public/Knights_of_Sidonia/audio_manifest.json"
    with open(ch1_manifest_path, 'r') as f:
        ch1_results = json.load(f)
        
    full_results = ch1_results + results
    full_manifest_path = "/Users/sandesh/Documents/Manga/my-video/public/Knights_of_Sidonia/audio_manifest_full.json"
    with open(full_manifest_path, 'w') as f:
        json.dump(full_results, f, indent=2)
        
    print(f"\nAll {len(full_results)} scenes across Chapters 1, 2, and 3 compiled successfully!")

if __name__ == "__main__":
    asyncio.run(generate_all())
