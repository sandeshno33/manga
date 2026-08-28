import json, os, re

manifest_path = "/Users/sandesh/Documents/Manga/my-video/public/Knights_of_Sidonia/audio_manifest.json"
story_path = "/Users/sandesh/Documents/Manga/my-video/src/storyData.ts"

if os.path.exists(manifest_path):
    with open(manifest_path, 'r') as f:
        audio_data = json.load(f)
    
    audio_map = {item["id"]: item for item in audio_data}
    
    with open(story_path, 'r') as f:
        code = f.read()

    for item in audio_data:
        line_id = item["id"]
        # Exact audio frames + 20 frames buffer (approx 0.66s pause)
        audio_frames = item.get("duration_frames", 120)
        target_frames = max(90, audio_frames + 20)
        
        # Replace durationInFrames for this id
        pattern = rf'(id:\s*"{line_id}",[\s\S]*?durationInFrames:\s*)\d+,'
        code = re.sub(pattern, rf'\g<1>{target_frames},', code)
    
    with open(story_path, 'w') as f:
        f.write(code)
    print("Successfully updated storyData.ts with exact audio durations!")
else:
    print("Manifest not ready yet.")
