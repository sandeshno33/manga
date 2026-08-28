import asyncio, edge_tts, os, json
from mutagen.mp3 import MP3

output_dir = "/Users/sandesh/Documents/Manga/my-video/public/Knights_of_Sidonia/audio"
os.makedirs(output_dir, exist_ok=True)

# Multi-Voice Mapping for natural human character performances
VOICE_MAP = {
    "Narrator": "en-US-ChristopherNeural",     # Deep, natural conversational narrator
    "Nagate": "en-US-GuyNeural",               # Natural anime protagonist
    "Ochiai": "en-GB-RyanNeural",              # Smooth, relaxed agent
    "Kobayashi": "en-US-AriaNeural",           # Clear, authoritative leader
    "Lala": "en-US-EricNeural",                # Warm, casual bear voice
    "Shizuka": "en-US-JennyNeural",            # Natural, gentle female
    "Instructor": "en-US-RogerNeural",         # Snappy drill officer
    "Cadets": "en-US-AnaNeural",               # Expressive female reaction
    "Honoka": "en-US-AnaNeural",               # Calm clone reaction
    "Elder": "en-US-SteffanNeural",            # Serious council voice
    "Worker": "en-US-BrianNeural",             # Natural worker shout
    "Investigator": "en-US-ChristopherNeural", # Direct police officer
}

# 38 Humanized lines (Clean, direct, conversational, zero fluff)
lines = [
    # ACT 1: THE SIMULATED BATTLE
    {"id": "01", "act": 1, "page": 1, "speaker": "Narrator", "motion": "pan-spread-left", "text": "In deep space, humanity is fighting an endless war against monsters known as the Gauna."},
    {"id": "02", "act": 1, "page": 3, "speaker": "Narrator", "motion": "scroll-down", "text": "These creatures can regenerate almost instantly. Normal weapons don't even scratch them."},
    {"id": "03", "act": 1, "page": 5, "speaker": "Narrator", "motion": "zoom-top-to-bottom", "text": "The only way to kill one is to pierce its core with a heavy mecha called a Garde."},
    {"id": "04", "act": 1, "page": 7, "speaker": "Narrator", "motion": "scroll-down", "text": "One clean hit. Target down."},
    {"id": "05", "act": 1, "page": 9, "speaker": "Narrator", "motion": "scroll-down", "text": "Except this wasn't real space. It was an underground simulation pod, piloted by a starving kid named Nagate who held every high score on the ship."},

    # ACT 2: THE HUNGER
    {"id": "06", "act": 2, "page": 10, "speaker": "Narrator", "motion": "scroll-down", "text": "Nagate grew up completely isolated in the underground tunnels. When his grandfather died three years ago, he was left all on his own."},
    {"id": "07", "act": 2, "page": 12, "speaker": "Nagate", "motion": "scroll-down", "text": "Nothing. There's not a single grain of rice left."},
    {"id": "08", "act": 2, "page": 14, "speaker": "Narrator", "motion": "scroll-up", "text": "Starving after two days without food, Nagate broke his grandfather's strict rule and climbed up the air ducts."},
    {"id": "09", "act": 2, "page": 17, "speaker": "Nagate", "motion": "scroll-down", "text": "Whoa! Oof!"},
    {"id": "10", "act": 2, "page": 17, "speaker": "Narrator", "motion": "pan-spread-left", "text": "He found a massive rice silo, but immediately fell straight into the sorting machine."},

    # ACT 3: THE CHASE & THE SKY
    {"id": "11", "act": 3, "page": 19, "speaker": "Worker", "motion": "scroll-down", "text": "Intruder in Sector 8! It's a rice thief! Grab him!"},
    {"id": "12", "act": 3, "page": 19, "speaker": "Nagate", "motion": "zoom-top-to-bottom", "text": "Wait, please! I'm just hungry!"},
    {"id": "13", "act": 3, "page": 21, "speaker": "Narrator", "motion": "pan-spread-left", "text": "Cornered in the vents, Nagate kicked through a window and tumbled outside."},
    {"id": "14", "act": 3, "page": 23, "speaker": "Narrator", "motion": "scroll-down", "text": "For the first time in his life, he saw the city above. But completely out of energy, he passed out on the pavement."},
    {"id": "15", "act": 3, "page": 24, "speaker": "Investigator", "motion": "scroll-down", "text": "Your grandfather died seventeen years ago, and you aren't in any database. Who are you?"},
    {"id": "16", "act": 3, "page": 24, "speaker": "Nagate", "motion": "zoom-top-to-bottom", "text": "Can I stand up? Everything's spinning..."},

    # ACT 4: MEDICAL BAY & PHOTOSYNTHESIS
    {"id": "17", "act": 4, "page": 25, "speaker": "Ochiai", "motion": "scroll-down", "text": "Two days without food and you faint. Sucks that you can't photosynthesize like the rest of us."},
    {"id": "18", "act": 4, "page": 25, "speaker": "Nagate", "motion": "zoom-top-to-bottom", "text": "Don't turn me into fertilizer!"},
    {"id": "19", "act": 4, "page": 28, "speaker": "Ochiai", "motion": "scroll-down", "text": "Relax. Someone important wants to sponsor you. Name's Ochiai. You got lucky, kid."},
    {"id": "20", "act": 4, "page": 27, "speaker": "Narrator", "motion": "scroll-up", "text": "People on Sidonia produce energy from sunlight, but Nagate is a regular human who needs real food to survive."},
    {"id": "21", "act": 4, "page": 30, "speaker": "Kobayashi", "motion": "scroll-down", "text": "Nagate Tanikaze. Follow me. I have something to show you."},
    {"id": "22", "act": 4, "page": 31, "speaker": "Lala", "motion": "scroll-down", "text": "Here's your room, Nagate. Those clothes stink, so put this uniform on."},
    {"id": "23", "act": 4, "page": 31, "speaker": "Nagate", "motion": "zoom-top-to-bottom", "text": "Wait... you're a talking bear with a robot arm?"},

    # ACT 5: ACADEMY BLUNDER
    {"id": "24", "act": 5, "page": 33, "speaker": "Shizuka", "motion": "scroll-down", "text": "Hey, you're that boy from earlier. What are you doing here?"},
    {"id": "25", "act": 5, "page": 34, "speaker": "Instructor", "motion": "scroll-down", "text": "Hey! Hook your safety belt to the wall rail! If we hit turbulence, you'll fly into the wall and die. Go check every bolt in this hallway!"},
    {"id": "26", "act": 5, "page": 36, "speaker": "Narrator", "motion": "pan-spread-left", "text": "Attached to the wall rail, Nagate followed the line right into an open room."},
    {"id": "27", "act": 5, "page": 37, "speaker": "Cadets", "motion": "scroll-down", "text": "Kyaaa! Pervert! Get out!"},
    {"id": "28", "act": 5, "page": 37, "speaker": "Nagate", "motion": "zoom-top-to-bottom", "text": "Wait! It's a mistake, the belt pulled me in!"},
    {"id": "29", "act": 5, "page": 39, "speaker": "Nagate", "motion": "scroll-down", "text": "Hi everyone. My name is Nagate Tanikaze."},
    {"id": "30", "act": 5, "page": 40, "speaker": "Honoka", "motion": "scroll-down", "text": "Hi everyone? What a weird guy."},

    # ACT 6: IMMORTAL COUNCIL
    {"id": "31", "act": 6, "page": 42, "speaker": "Elder", "motion": "scroll-down", "text": "A Gauna cluster has entered our sector, within three light years."},
    {"id": "32", "act": 6, "page": 45, "speaker": "Kobayashi", "motion": "zoom-top-to-bottom", "text": "We can't negotiate with them. If we want to survive, we have to fight."},
    {"id": "33", "act": 6, "page": 46, "speaker": "Narrator", "motion": "scroll-down", "text": "The cadets thought the Gauna were just history, but the captain knew the war was starting again."},

    # ACT 7: SEED SHIP SIDONIA & TSUGUMORI
    {"id": "34", "act": 7, "page": 47, "speaker": "Narrator", "motion": "pan-spread-left", "text": "This is the starship Sidonia, traveling through deep space a thousand years after Earth was destroyed."},
    {"id": "35", "act": 7, "page": 49, "speaker": "Nagate", "motion": "scroll-up", "text": "So this is what real space looks like."},
    {"id": "36", "act": 7, "page": 50, "speaker": "Narrator", "motion": "scroll-down", "text": "Waiting in the hangar was the Type 17 Tsugumori, the legendary mecha his grandfather once flew."},
    {"id": "37", "act": 7, "page": 50, "speaker": "Kobayashi", "motion": "zoom-top-to-bottom", "text": "Will you pilot this machine and protect Sidonia, Nagate?"},
    {"id": "38", "act": 7, "page": 50, "speaker": "Nagate", "motion": "pan-spread-left", "text": "And of course, I said yes. That was the day I became a pilot."}
]

async def generate_single(item):
    voice = VOICE_MAP.get(item["speaker"], "en-US-ChristopherNeural")
    out_file = f"line_{item['id']}.mp3"
    out_path = os.path.join(output_dir, out_file)
    
    # Generate speech
    communicate = edge_tts.Communicate(item["text"], voice, rate="+2%", pitch="+0Hz")
    await communicate.save(out_path)
    
    audio = MP3(out_path)
    dur = round(audio.info.length, 2)
    frames = max(45, int(dur * 30))
    
    item["audio_file"] = f"Knights_of_Sidonia/audio/{out_file}"
    item["duration_sec"] = dur
    item["duration_frames"] = frames + 16 # Exact audio duration + smooth natural 0.5s pause
    print(f"Generated line {item['id']} ({item['speaker']}) - {dur:.2f}s: \"{item['text']}\"")
    return item

async def main():
    print("Generating 38 humanized conversational voiceover lines...")
    tasks = [generate_single(line) for line in lines]
    results = await asyncio.gather(*tasks)
    
    # Save manifest
    manifest_path = "/Users/sandesh/Documents/Manga/my-video/public/Knights_of_Sidonia/audio_manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(results, f, indent=2)
        
    print("All humanized voice lines synthesized successfully!")

if __name__ == "__main__":
    asyncio.run(main())
