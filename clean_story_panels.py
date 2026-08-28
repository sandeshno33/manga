import os, shutil
from PIL import Image

BASE_DIRS = [
    "/Users/sandesh/Documents/Manga/Solo_Max_Level_Newbie",
    "/Users/sandesh/Documents/Manga/my-video/public/Solo_Max_Level_Newbie"
]

# Definite non-story credit / promo images identified
REMOVAL_TARGETS = {
    "chapter_1": ["page_001.jpg"],   # Asura Scans Staff Card (User Image 1)
    "chapter_2": ["page_001.jpg"],   # Asura Scans Staff Card
    "chapter_3": ["page_001.jpg"],   # Asura Scans Staff Card
    "chapter_4": ["page_001.jpg"],   # Asura Scans Staff Card
    "chapter_5": ["page_001.jpg"],   # Asura Scans Staff Card
    "chapter_6": ["page_001.jpg"],   # Asura Scans Staff Card
    "chapter_7": ["page_001.jpg"],   # Asura Scans Staff Card
    "chapter_8": ["page_001.jpg"],   # Scan Header Banner
    "chapter_9": ["page_001.jpg"],   # Asura Scans Staff Card
    "chapter_10": ["page_001.jpg"],  # Asura Scans Staff Card
    "chapter_11": ["page_001.jpg"],  # Scan Header Banner
    "chapter_12": ["page_001.jpg"],  # Scan Header Banner
    "chapter_13": ["page_001.jpg"],  # Scan Header Banner
    "chapter_14": ["page_032.jpg"],  # End Discord/Patreon Promo Banner
    "chapter_15": ["page_028.jpg"],  # Immortal Updates Staff Card (User Image 2)
}

def clean_and_renumber():
    print("=================================================================")
    print("🧹 REMOVING ALL SCANLATION CREDIT CARDS & PROMO BANNERS")
    print("=================================================================")
    
    total_removed = 0
    total_retained = 0
    
    for base in BASE_DIRS:
        if not os.path.exists(base):
            continue
            
        print(f"\nProcessing directory: {base}")
        chapters = sorted([d for d in os.listdir(base) if d.startswith("chapter_")], key=lambda x: int(x.split('_')[1]))
        
        for ch in chapters:
            ch_path = os.path.join(base, ch)
            files = sorted([f for f in os.listdir(ch_path) if f.endswith(('.jpg', '.png', '.webp'))])
            
            # Remove targets
            targets = REMOVAL_TARGETS.get(ch, [])
            for target in targets:
                target_path = os.path.join(ch_path, target)
                if os.path.exists(target_path):
                    os.remove(target_path)
                    print(f"  ❌ Removed Non-Story Card: {ch}/{target}")
                    total_removed += 1
                    
            # Re-read remaining files and renumber sequentially
            remaining = sorted([f for f in os.listdir(ch_path) if f.endswith(('.jpg', '.png', '.webp'))])
            
            # Rename temporarily to avoid collision
            temp_files = []
            for idx, f in enumerate(remaining):
                ext = os.path.splitext(f)[1]
                old_p = os.path.join(ch_path, f)
                temp_p = os.path.join(ch_path, f"temp_{idx+1:03d}{ext}")
                os.rename(old_p, temp_p)
                temp_files.append((temp_p, idx + 1, ext))
                
            for temp_p, idx, ext in temp_files:
                final_p = os.path.join(ch_path, f"page_{idx:03d}{ext}")
                os.rename(temp_p, final_p)
                
            final_files = sorted([f for f in os.listdir(ch_path) if f.endswith(('.jpg', '.png', '.webp'))])
            total_retained += len(final_files)
            print(f"  ✔ {ch}: Cleaned & Renumbered ({len(final_files)} pure story panels)")
            
    print("\n=================================================================")
    print(f"✨ CLEANUP COMPLETE!")
    print(f"Removed {total_removed // len(BASE_DIRS)} intro cards / promo banners.")
    print(f"Preserved {total_retained // len(BASE_DIRS)} 100% pure story action panels across 15 chapters!")
    print("=================================================================")

if __name__ == "__main__":
    clean_and_renumber()
