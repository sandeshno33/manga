import os

BASE_DIRS = [
    "/Users/sandesh/Documents/Manga/Solo_Max_Level_Newbie",
    "/Users/sandesh/Documents/Manga/my-video/public/Solo_Max_Level_Newbie"
]

# Chapters with title header logo cards at panel_001
CHAPTERS_WITH_TITLE_LOGO = ["chapter_8", "chapter_12", "chapter_13", "chapter_14", "chapter_15"]

def remove_title_headers():
    print("=================================================================")
    print("🚫 REMOVING CHAPTER TITLE / LOGO INTRO CARDS")
    print("=================================================================")

    for base in BASE_DIRS:
        if not os.path.exists(base):
            continue
            
        print(f"\nProcessing base: {base}")
        for ch in CHAPTERS_WITH_TITLE_LOGO:
            ch_panel_dir = os.path.join(base, ch, "panels")
            if not os.path.exists(ch_panel_dir):
                continue
                
            panel_001 = os.path.join(ch_panel_dir, "panel_001.jpg")
            if os.path.exists(panel_001):
                os.remove(panel_001)
                print(f"  ❌ Removed Title Logo Card: {ch}/panel_001.jpg")
                
            # Renumber remaining panels
            remaining = sorted([f for f in os.listdir(ch_panel_dir) if f.startswith("panel_") and f.endswith(('.jpg', '.png', '.webp'))])
            temp_files = []
            for idx, f in enumerate(remaining):
                ext = os.path.splitext(f)[1]
                old_p = os.path.join(ch_panel_dir, f)
                temp_p = os.path.join(ch_panel_dir, f"temp_{idx+1:03d}{ext}")
                os.rename(old_p, temp_p)
                temp_files.append((temp_p, idx + 1, ext))
                
            for temp_p, idx, ext in temp_files:
                final_p = os.path.join(ch_panel_dir, f"panel_{idx:03d}{ext}")
                os.rename(temp_p, final_p)
                
            final_files = sorted([f for f in os.listdir(ch_panel_dir) if f.startswith("panel_") and f.endswith(('.jpg', '.png', '.webp'))])
            print(f"  ✔ {ch}: Cleaned & Renumbered ({len(final_files)} story panels starting on pure action)")

    print("\n=================================================================")
    print("✨ ALL TITLE LOGO CARDS PURGED SUCCESSFULLY!")
    print("=================================================================")

if __name__ == "__main__":
    remove_title_headers()
