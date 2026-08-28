import urllib.request, json, ssl, base64, wave, os, time

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

api_key = os.environ.get("GEMINI_API_KEY", "")
model = "gemini-3.1-flash-tts-preview"

output_dir = "/Users/sandesh/Documents/Manga/my-video/public/Knights_of_Sidonia/audio"
os.makedirs(output_dir, exist_ok=True)

# 38 Dialogue & Narration Lines across all 7 scenes
lines = [
    # SCENE 1 (Pages 1-9)
    {"id": "01", "scene": 1, "page": 1, "speaker": "Narrator", "voice": "Charon", "text": "Deep space. A cold, unforgiving abyss where humanity's last survivors wage an endless war against cosmic horrors."},
    {"id": "02", "scene": 1, "page": 3, "speaker": "Narrator", "voice": "Charon", "text": "They are called the Gauna. Shapeshifting leviathans of indestructible biological mass, immune to almost every weapon known to man."},
    {"id": "03", "scene": 1, "page": 5, "speaker": "Narrator", "voice": "Charon", "text": "Only a Garde heavy mecha, striking with surgical precision at the hidden core beneath the placenta, stands any hope of victory."},
    {"id": "04", "scene": 1, "page": 7, "speaker": "Narrator", "voice": "Charon", "text": "One strike. Core pierced. Target destroyed."},
    {"id": "05", "scene": 1, "page": 9, "speaker": "Narrator", "voice": "Charon", "text": "Yet this battle was inside a subterranean simulation capsule... and the pilot was a starving boy named Nagate Tanikaze, holding top rank across thousands of combat sorties."},
    
    # SCENE 2 (Pages 10-17)
    {"id": "06", "scene": 2, "page": 10, "speaker": "Narrator", "voice": "Charon", "text": "For as long as he could remember, Nagate had lived in the forgotten catacombs beneath Sidonia. Three years ago, his grandfather passed away, leaving him alone in the dark."},
    {"id": "07", "scene": 2, "page": 12, "speaker": "Nagate", "voice": "Puck", "text": "Empty... not even a single grain of rice left..."},
    {"id": "08", "scene": 2, "page": 14, "speaker": "Narrator", "voice": "Charon", "text": "After two agonizing days without food, facing starvation, Nagate broke his grandfather's rule and climbed up the forbidden ventilation ducts."},
    {"id": "09", "scene": 2, "page": 17, "speaker": "Nagate", "voice": "Puck", "text": "Whoaaaa! Oof!"},
    {"id": "10", "scene": 2, "page": 17, "speaker": "Narrator", "voice": "Charon", "text": "He found thousands of tons of rice, but falling straight into the high-speed sorting hopper quickly blew his cover."},
    
    # SCENE 3 (Pages 18-24)
    {"id": "11", "scene": 3, "page": 19, "speaker": "Worker", "voice": "Fenrir", "text": "Intruder in Storage Hopper 8! It's a rice thief! Security, block the exits!"},
    {"id": "12", "scene": 3, "page": 19, "speaker": "Nagate", "voice": "Puck", "text": "Wait! Please! I just need a little food!"},
    {"id": "13", "scene": 3, "page": 21, "speaker": "Narrator", "voice": "Charon", "text": "Hunted through the maintenance chutes, Nagate kicked through a high glass window, breaking into the open world."},
    {"id": "14", "scene": 3, "page": 23, "speaker": "Narrator", "voice": "Charon", "text": "And in that breathless instant, the subterranean boy saw the sky—a monumental metropolis suspended inside the starship Sidonia. But exhausted from hunger, he collapsed on the spot."},
    {"id": "15", "scene": 3, "page": 24, "speaker": "Investigator", "voice": "Fenrir", "text": "Hiroki Saito died seventeen years ago, and no Nagate Tanikaze exists in our registry! Who are you really?!"},
    {"id": "16", "scene": 3, "page": 24, "speaker": "Nagate", "voice": "Puck", "text": "Please... can I stop kneeling? My head is spinning..."},
    
    # SCENE 4 (Pages 25-32)
    {"id": "17", "scene": 4, "page": 25, "speaker": "Ochiai", "voice": "Puck", "text": "A mere two days without food and you pass out cold. Must be tough, not being able to photosynthesize like the rest of us."},
    {"id": "18", "scene": 4, "page": 25, "speaker": "Nagate", "voice": "Puck", "text": "I-I'll never let you turn me into fertilizer in an organic-conversion reactor!"},
    {"id": "19", "scene": 4, "page": 28, "speaker": "Ochiai", "voice": "Puck", "text": "Relax. Someone powerful has taken an interest in you. The name's Ochiai. Consider this your lucky day."},
    {"id": "20", "scene": 4, "page": 27, "speaker": "Narrator", "voice": "Charon", "text": "Centuries ago, Sidonia's humans modified their DNA to photosynthesize solar energy. But Nagate was a natural, unmodified human—relying wholly on real food."},
    {"id": "21", "scene": 4, "page": 30, "speaker": "Kobayashi", "voice": "Aoede", "text": "Nagate Tanikaze, yes? Come. There is something I must show you."},
    {"id": "22", "scene": 4, "page": 31, "speaker": "Lala", "voice": "Puck", "text": "This will be your room, Nagate. Those rags smell terrible—change into this cadet uniform immediately."},
    {"id": "23", "scene": 4, "page": 31, "speaker": "Nagate", "voice": "Puck", "text": "A... a talking bear with a robotic arm?!"},
    
    # SCENE 5 (Pages 33-40)
    {"id": "24", "scene": 5, "page": 33, "speaker": "Shizuka", "voice": "Kore", "text": "Ah... you're that boy from the streets! Why are you here in cadet quarters?"},
    {"id": "25", "scene": 5, "page": 34, "speaker": "Instructor", "voice": "Fenrir", "text": "Hey! Your safety belt is unhooked! In a sudden gravity halt, you'll be splattered across the hull! Go inspect every rail fastener on this floor!"},
    {"id": "26", "scene": 5, "page": 36, "speaker": "Narrator", "voice": "Charon", "text": "Tethered to the guide-rail, Nagate blindly followed the line right through an open doorway..."},
    {"id": "27", "scene": 5, "page": 37, "speaker": "Cadets", "voice": "Kore", "text": "KYAAAAAAAH! PERVERT! INTRUDER!"},
    {"id": "28", "scene": 5, "page": 37, "speaker": "Nagate", "voice": "Puck", "text": "W-Wait! It's a mistake! The rail dragged me in—"},
    {"id": "29", "scene": 5, "page": 39, "speaker": "Nagate", "voice": "Puck", "text": "H-Hello, all! My name is Nagate Tanikaze..."},
    {"id": "30", "scene": 5, "page": 40, "speaker": "Honoka", "voice": "Kore", "text": "Hello all...? What an odd creature."},
    
    # SCENE 6 (Pages 41-46)
    {"id": "31", "scene": 6, "page": 42, "speaker": "Elder", "voice": "Fenrir", "text": "A Gauna cluster ship has entered Threat Range Level 3. Approaching within three light-years of Sidonia."},
    {"id": "32", "scene": 6, "page": 45, "speaker": "Kobayashi", "voice": "Aoede", "text": "There is zero chance for dialogue. The sole means of mankind's survival is the stern, unapologetic use of force."},
    {"id": "33", "scene": 6, "page": 46, "speaker": "Narrator", "voice": "Charon", "text": "To the young cadets, the Gauna were ancient legends. But the Captain knew the grim reality: the enemy had returned across the stars."},
    
    # SCENE 7 (Pages 47-50)
    {"id": "34", "scene": 7, "page": 47, "speaker": "Narrator", "voice": "Charon", "text": "The Interstellar Seed Ship Sidonia. One thousand years after the total annihilation of Earth, this lonely ark continues its voyage for human survival."},
    {"id": "35", "scene": 7, "page": 49, "speaker": "Nagate", "voice": "Puck", "text": "So this... this is the real universe...?"},
    {"id": "36", "scene": 7, "page": 50, "speaker": "Narrator", "voice": "Charon", "text": "Waiting in the shadows of the high hangar was the legendary Type 17 Tsugumori—the historic battle machine once commanded by his grandfather."},
    {"id": "37", "scene": 7, "page": 50, "speaker": "Kobayashi", "voice": "Aoede", "text": "Will you take its helm and become the shield of Sidonia, Nagate Tanikaze?"},
    {"id": "38", "scene": 7, "page": 50, "speaker": "Nagate", "voice": "Puck", "text": "And of course... I replied yes. That was the day I became a Garde pilot."}
]

def generate_voice_file(item):
    out_file = f"line_{item['id']}.wav"
    out_path = os.path.join(output_dir, out_file)
    
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        try:
            with wave.open(out_path, 'rb') as w:
                frames = w.getnframes()
                rate = w.getframerate()
                duration = frames / float(rate)
                item["audio_file"] = f"Knights_of_Sidonia/audio/{out_file}"
                item["duration_sec"] = round(duration, 2)
                item["duration_frames"] = max(45, int(duration * 30))
                return item
        except Exception:
            pass

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": item["text"]}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {
                        "voiceName": item["voice"]
                    }
                }
            }
        }
    }
    
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, context=ctx) as r:
                data = json.loads(r.read().decode())
                inline_data = data['candidates'][0]['content']['parts'][0]['inlineData']
                raw_pcm = base64.b64decode(inline_data['data'])
                
                with wave.open(out_path, 'wb') as wav:
                    wav.setnchannels(1)
                    wav.setsampwidth(2)
                    wav.setframerate(24000)
                    wav.writeframes(raw_pcm)
                
                duration = (len(raw_pcm) / (2 * 24000))
                item["audio_file"] = f"Knights_of_Sidonia/audio/{out_file}"
                item["duration_sec"] = round(duration, 2)
                item["duration_frames"] = max(45, int(duration * 30))
                print(f"Generated line {item['id']} ({item['speaker']}) - {duration:.2f}s", flush=True)
                time.sleep(0.5)
                return item
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait_time = 4 * (attempt + 1)
                print(f"Rate limit 429 on line {item['id']}, waiting {wait_time}s...", flush=True)
                time.sleep(wait_time)
            else:
                if item["voice"] != "Puck":
                    print(f"Voice {item['voice']} failed on line {item['id']}, fallback to Puck...", flush=True)
                    item["voice"] = "Puck"
                    payload["generationConfig"]["speechConfig"]["voiceConfig"]["prebuiltVoiceConfig"]["voiceName"] = "Puck"
                    time.sleep(1)
                else:
                    print(f"HTTP {e.code} on line {item['id']}: {e}", flush=True)
                    time.sleep(2)
        except Exception as e:
            print(f"Attempt {attempt+1} error for line {item['id']}: {e}", flush=True)
            time.sleep(2)
            
    # If network fails, set default duration
    item["duration_sec"] = 4.0
    item["duration_frames"] = 120
    return item

print(f"Starting voice generation for {len(lines)} lines with model {model}...", flush=True)
results = []
for idx, line in enumerate(lines):
    print(f"[{idx+1}/{len(lines)}] Processing line {line['id']}...", flush=True)
    res = generate_voice_file(line)
    results.append(res)

manifest_path = "/Users/sandesh/Documents/Manga/my-video/public/Knights_of_Sidonia/audio_manifest.json"
with open(manifest_path, 'w') as f:
    json.dump(results, f, indent=2)

print("Finished! Saved audio manifest to", manifest_path, flush=True)
