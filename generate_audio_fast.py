import asyncio, edge_tts, os, json
from mutagen.mp3 import MP3

output_dir = "/Users/sandesh/Documents/Manga/my-video/public/Knights_of_Sidonia/audio"
os.makedirs(output_dir, exist_ok=True)

# Multi-Voice Mapping for Edge TTS
VOICE_MAP = {
    "Narrator": "en-US-ChristopherNeural",     # Deep, cinematic baritone
    "Nagate": "en-US-GuyNeural",               # Young male protagonist
    "Ochiai": "en-GB-RyanNeural",              # Smooth, suave agent
    "Kobayashi": "en-US-AriaNeural",           # Regal, commanding female leader
    "Lala": "en-US-EricNeural",                # Deep maternal bear with rumble
    "Shizuka": "en-US-JennyNeural",            # Gentle, polite female
    "Instructor": "en-US-RogerNeural",         # Strict drill officer
    "Cadets": "en-US-AnaNeural",               # High-pitched young female
    "Honoka": "en-US-AnaNeural",               # Deadpan unison clone
    "Elder": "en-US-SteffanNeural",            # Ancient cybernetic council
    "Worker": "en-US-BrianNeural",             # Industrial factory worker
    "Investigator": "en-US-ChristopherNeural", # Stern police officer
}

lines = [
    # SCENE 1 (Pages 1-9)
    {"id": "01", "speaker": "Narrator", "text": "Deep space. A cold, unforgiving abyss where humanity's last survivors wage an endless war against cosmic horrors."},
    {"id": "02", "speaker": "Narrator", "text": "They are called the Gauna. Shapeshifting leviathans of indestructible biological mass, immune to almost every weapon known to man."},
    {"id": "03", "speaker": "Narrator", "text": "Only a Garde heavy mecha, striking with surgical precision at the hidden core beneath the placenta, stands any hope of victory."},
    {"id": "04", "speaker": "Narrator", "text": "One strike. Core pierced. Target destroyed."},
    {"id": "05", "speaker": "Narrator", "text": "Yet this battle was inside a subterranean simulation capsule... and the pilot was a starving boy named Nagate Tanikaze, holding top rank across thousands of combat sorties."},
    
    # SCENE 2 (Pages 10-17)
    {"id": "06", "speaker": "Narrator", "text": "For as long as he could remember, Nagate had lived in the forgotten catacombs beneath Sidonia. Three years ago, his grandfather passed away, leaving him alone in the dark."},
    {"id": "07", "speaker": "Nagate", "text": "Empty... not even a single grain of rice left..."},
    {"id": "08", "speaker": "Narrator", "text": "After two agonizing days without food, facing starvation, Nagate broke his grandfather's rule and climbed up the forbidden ventilation ducts."},
    {"id": "09", "speaker": "Nagate", "text": "Whoaaaa! Oof!"},
    {"id": "10", "speaker": "Narrator", "text": "He found thousands of tons of rice, but falling straight into the high-speed sorting hopper quickly blew his cover."},
    
    # SCENE 3 (Pages 18-24)
    {"id": "11", "speaker": "Worker", "text": "Intruder in Storage Hopper 8! It's a rice thief! Security, block the exits!"},
    {"id": "12", "speaker": "Nagate", "text": "Wait! Please! I just need a little food!"},
    {"id": "13", "speaker": "Narrator", "text": "Hunted through the maintenance chutes, Nagate kicked through a high glass window, breaking into the open world."},
    {"id": "14", "speaker": "Narrator", "text": "And in that breathless instant, the subterranean boy saw the sky—a monumental metropolis suspended inside the starship Sidonia. But exhausted from hunger, he collapsed on the spot."},
    {"id": "15", "speaker": "Investigator", "text": "Hiroki Saito died seventeen years ago, and no Nagate Tanikaze exists in our registry! Who are you really?!"},
    {"id": "16", "speaker": "Nagate", "text": "Please... can I stop kneeling? My head is spinning..."},
    
    # SCENE 4 (Pages 25-32)
    {"id": "17", "speaker": "Ochiai", "text": "A mere two days without food and you pass out cold. Must be tough, not being able to photosynthesize like the rest of us."},
    {"id": "18", "speaker": "Nagate", "text": "I-I'll never let you turn me into fertilizer in an organic-conversion reactor!"},
    {"id": "19", "speaker": "Ochiai", "text": "Relax. Someone powerful has taken an interest in you. The name's Ochiai. Consider this your lucky day."},
    {"id": "20", "speaker": "Narrator", "text": "Centuries ago, Sidonia's humans modified their DNA to photosynthesize solar energy. But Nagate was a natural, unmodified human—relying wholly on real food."},
    {"id": "21", "speaker": "Kobayashi", "text": "Nagate Tanikaze, yes? Come. There is something I must show you."},
    {"id": "22", "speaker": "Lala", "text": "This will be your room, Nagate. Those rags smell terrible—change into this cadet uniform immediately."},
    {"id": "23", "speaker": "Nagate", "text": "A... a talking bear with a robotic arm?!"},
    
    # SCENE 5 (Pages 33-40)
    {"id": "24", "speaker": "Shizuka", "text": "Ah... you're that boy from the streets! Why are you here in cadet quarters?"},
    {"id": "25", "speaker": "Instructor", "text": "Hey! Your safety belt is unhooked! In a sudden gravity halt, you'll be splattered across the hull! Go inspect every rail fastener on this floor!"},
    {"id": "26", "speaker": "Narrator", "text": "Tethered to the guide-rail, Nagate blindly followed the line right through an open doorway..."},
    {"id": "27", "speaker": "Cadets", "text": "KYAAAAAAAH! PERVERT! INTRUDER!"},
    {"id": "28", "speaker": "Nagate", "text": "W-Wait! It's a mistake! The rail dragged me in—"},
    {"id": "29", "speaker": "Nagate", "text": "H-Hello, all! My name is Nagate Tanikaze..."},
    {"id": "30", "speaker": "Honoka", "text": "Hello all...? What an odd creature."},
    
    # SCENE 6 (Pages 41-46)
    {"id": "31", "speaker": "Elder", "text": "A Gauna cluster ship has entered Threat Range Level 3. Approaching within three light-years of Sidonia."},
    {"id": "32", "speaker": "Kobayashi", "text": "There is zero chance for dialogue. The sole means of mankind's survival is the stern, unapologetic use of force."},
    {"id": "33", "speaker": "Narrator", "text": "To the young cadets, the Gauna were ancient legends. But the Captain knew the grim reality: the enemy had returned across the stars."},
    
    # SCENE 7 (Pages 47-50)
    {"id": "34", "speaker": "Narrator", "text": "The Interstellar Seed Ship Sidonia. One thousand years after the total annihilation of Earth, this lonely ark continues its voyage for human survival."},
    {"id": "35", "speaker": "Nagate", "text": "So this... this is the real universe...?"},
    {"id": "36", "speaker": "Narrator", "text": "Waiting in the shadows of the high hangar was the legendary Type 17 Tsugumori—the historic battle machine once commanded by his grandfather."},
    {"id": "37", "speaker": "Kobayashi", "text": "Will you take its helm and become the shield of Sidonia, Nagate Tanikaze?"},
    {"id": "38", "speaker": "Nagate", "text": "And of course... I replied yes. That was the day I became a Garde pilot."}
]

async def generate_single(item):
    voice = VOICE_MAP.get(item["speaker"], "en-US-ChristopherNeural")
    out_file = f"line_{item['id']}.mp3"
    out_path = os.path.join(output_dir, out_file)
    
    communicate = edge_tts.Communicate(item["text"], voice)
    await communicate.save(out_path)
    
    # Get MP3 duration
    try:
        from mutagen.mp3 import MP3
        audio = MP3(out_path)
        duration = audio.info.length
    except Exception:
        # Estimate duration by file size
        duration = max(3.0, len(item["text"]) / 14.0)
        
    item["audio_file"] = f"Knights_of_Sidonia/audio/{out_file}"
    item["duration_sec"] = round(duration, 2)
    item["duration_frames"] = max(60, int(duration * 30))
    print(f"Generated line {item['id']} ({item['speaker']}) -> {out_file} ({duration:.2f}s)")
    return item

async def main():
    print(f"Synthesizing all {len(lines)} voiceover lines in parallel...")
    tasks = [generate_single(line) for line in lines]
    results = await asyncio.gather(*tasks)
    
    manifest_path = "/Users/sandesh/Documents/Manga/my-video/public/Knights_of_Sidonia/audio_manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(results, f, indent=2)
    print("All audio files generated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
