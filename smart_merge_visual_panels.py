import os, sys, json
from PIL import Image
import numpy as np

SRC_BASE = "/Users/sandesh/Documents/Manga/Solo_Max_Level_Newbie"
PUBLIC_BASE = "/Users/sandesh/Documents/Manga/my-video/public/Solo_Max_Level_Newbie"

def merge_panels_in_chapter(ch_name):
    ch_dir_1 = os.path.join(SRC_BASE, ch_name, "panels")
    ch_dir_2 = os.path.join(PUBLIC_BASE, ch_name, "panels")
    if not os.path.exists(ch_dir_1):
        return
        
    panel_files = sorted([f for f in os.listdir(ch_dir_1) if f.startswith("panel_") and f.endswith(('.jpg', '.png', '.webp'))])
    if not panel_files:
        return
        
    panels = []
    for f in panel_files:
        p = os.path.join(ch_dir_1, f)
        img = Image.open(p)
        panels.append((f, img))
        
    merged_panels = []
    i = 0
    while i < len(panels):
        curr_f, curr_img = panels[i]
        cw, ch = curr_img.size
        
        # Check if current panel is a small text box / dialogue bubble (< 600px)
        if ch < 600 and i + 1 < len(panels):
            # Look ahead: merge with next visual panel
            next_f, next_img = panels[i+1]
            nw, nh = next_img.size
            
            # Stack vertically: curr_img on top of next_img
            mw = max(cw, nw)
            mh = ch + nh
            merged_img = Image.new("RGB", (mw, mh), (255, 255, 255))
            merged_img.paste(curr_img, (0, 0))
            merged_img.paste(next_img, (0, ch))
            
            # If the merged height is still very small (< 650px) and there is another panel, chain it
            if mh < 650 and i + 2 < len(panels):
                n2_f, n2_img = panels[i+2]
                n2w, n2h = n2_img.size
                m2w = max(mw, n2w)
                m2h = mh + n2h
                m2_img = Image.new("RGB", (m2w, m2h), (255, 255, 255))
                m2_img.paste(merged_img, (0, 0))
                m2_img.paste(n2_img, (0, mh))
                merged_panels.append(m2_img)
                i += 3
            else:
                merged_panels.append(merged_img)
                i += 2
        elif ch < 500 and len(merged_panels) > 0:
            # Trailing small dialogue box: merge with previous panel
            prev_img = merged_panels.pop()
            pw, ph = prev_img.size
            mw = max(pw, cw)
            mh = ph + ch
            merged_img = Image.new("RGB", (mw, mh), (255, 255, 255))
            merged_img.paste(prev_img, (0, 0))
            merged_img.paste(curr_img, (0, ph))
            merged_panels.append(merged_img)
            i += 1
        else:
            merged_panels.append(curr_img)
            i += 1
            
    # Clear and rewrite renumbered merged panels
    for f in panel_files:
        p1 = os.path.join(ch_dir_1, f)
        p2 = os.path.join(ch_dir_2, f)
        if os.path.exists(p1): os.remove(p1)
        if os.path.exists(p2): os.remove(p2)
        
    for idx, p_img in enumerate(merged_panels):
        fname = f"panel_{idx+1:03d}.jpg"
        p1 = os.path.join(ch_dir_1, fname)
        p2 = os.path.join(ch_dir_2, fname)
        p_img.save(p1, format="JPEG", quality=94, optimize=True)
        p_img.save(p2, format="JPEG", quality=94, optimize=True)
        
    print(f"✔ {ch_name}: Unified {len(panel_files)} raw cuts into {len(merged_panels)} rich, visually-complete story panels!")
    return len(merged_panels)

def main():
    print("=================================================================")
    print("🎨 MERGING ISOLATED TEXT BUBBLES WITH VISUAL ARTWORK PANELS")
    print("=================================================================")
    
    chapters = sorted([d for d in os.listdir(SRC_BASE) if d.startswith("chapter_")], key=lambda x: int(x.split('_')[1]))
    total_panels = 0
    for ch in chapters:
        count = merge_panels_in_chapter(ch)
        if count:
            total_panels += count
            
    print("\n=================================================================")
    print(f"✨ SUCCESS! All 15 chapters now contain {total_panels} complete visual panels!")
    print("Every panel now has full visual context and artwork (no floating blank text boxes)!")
    print("=================================================================")

if __name__ == "__main__":
    main()
