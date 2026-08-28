import os, sys, time, json
import numpy as np
from PIL import Image

SRC_BASE = "/Users/sandesh/Documents/Manga/Solo_Max_Level_Newbie"
PUBLIC_BASE = "/Users/sandesh/Documents/Manga/my-video/public/Solo_Max_Level_Newbie"

def split_strip_into_panels(img_path, min_panel_h=180, min_gutter_h=25):
    try:
        img = Image.open(img_path)
    except Exception as e:
        print(f"Error opening {img_path}: {e}")
        return []
        
    w, h = img.size
    # If the image is already a standard single panel (< 1800px tall), keep as single panel
    if h <= 1800:
        return [img]

    # Convert to grayscale numpy array for fast row-by-row gutter detection
    gray = np.array(img.convert('L'))
    row_mean = np.mean(gray, axis=1)
    row_std = np.std(gray, axis=1)

    # Gutter = pure white (mean > 246, std < 10) or pure black (mean < 15, std < 5)
    is_gutter = (row_mean > 246) | ((row_mean < 15) & (row_std < 5))

    panels_coords = []
    in_panel = False
    start_y = 0
    gutter_count = 0

    for y in range(h):
        if not is_gutter[y]:
            if not in_panel:
                in_panel = True
                start_y = max(0, y - 8)
            gutter_count = 0
        else:
            if in_panel:
                gutter_count += 1
                if gutter_count >= min_gutter_h or y == h - 1:
                    end_y = min(h, y - gutter_count + 12)
                    if end_y - start_y >= min_panel_h:
                        panels_coords.append((start_y, end_y))
                    in_panel = False
                    gutter_count = 0

    if in_panel and (h - start_y >= min_panel_h):
        panels_coords.append((start_y, h))

    # If no gutters were found (e.g. unbroken action scene), segment into proportional cinematic cuts
    if len(panels_coords) == 0:
        chunk_h = 1400
        for y in range(0, h, chunk_h):
            ey = min(h, y + chunk_h)
            if ey - y >= min_panel_h:
                panels_coords.append((y, ey))

    # Split sub-panels if any single block is excessively long (> 3200px)
    final_coords = []
    for sy, ey in panels_coords:
        p_h = ey - sy
        if p_h > 3200:
            # Check for weaker inner gutters inside long panels
            sub_gray = gray[sy:ey]
            sub_row_mean = np.mean(sub_gray, axis=1)
            sub_gutters = (sub_row_mean > 240) | (sub_row_mean < 25)
            
            sub_starts = [0]
            for r in range(1200, p_h - 800, 1000):
                # find nearest gutter near interval
                window = sub_gutters[max(0, r-300):min(p_h, r+300)]
                g_indices = np.where(window)[0]
                if len(g_indices) > 0:
                    split_pt = max(0, r-300) + g_indices[len(g_indices)//2]
                    sub_starts.append(split_pt)
                else:
                    sub_starts.append(r)
            sub_starts.append(p_h)
            
            for i in range(len(sub_starts)-1):
                final_coords.append((sy + sub_starts[i], sy + sub_starts[i+1]))
        else:
            final_coords.append((sy, ey))

    # Crop and return PIL images
    cropped_panels = []
    for sy, ey in final_coords:
        if ey > sy + 50:
            cropped = img.crop((0, max(0, sy), w, min(h, ey)))
            cropped_panels.append(cropped)

    return cropped_panels

def main():
    print("=================================================================")
    print("✂️ BATCH SMART WEBTOON PANEL SPLITTER ACROSS ALL 15 CHAPTERS")
    print("=================================================================")

    manifest = {}
    total_panels_all_chapters = 0
    
    chapters = sorted([d for d in os.listdir(SRC_BASE) if d.startswith("chapter_")], key=lambda x: int(x.split('_')[1]))

    for ch in chapters:
        ch_num = int(ch.split('_')[1])
        ch_src_dir = os.path.join(SRC_BASE, ch)
        
        # Panel output directories
        ch_panel_dir_1 = os.path.join(SRC_BASE, ch, "panels")
        ch_panel_dir_2 = os.path.join(PUBLIC_BASE, ch, "panels")
        os.makedirs(ch_panel_dir_1, exist_ok=True)
        os.makedirs(ch_panel_dir_2, exist_ok=True)
        
        # Get all page strips (ignoring the panels folder itself)
        page_files = sorted([f for f in os.listdir(ch_src_dir) if f.startswith("page_") and f.endswith(('.jpg', '.png', '.webp'))])
        
        panel_count = 0
        chapter_panel_data = []

        print(f"\nProcessing {ch} ({len(page_files)} page strips)...")

        for page_file in page_files:
            page_path = os.path.join(ch_src_dir, page_file)
            panels = split_strip_into_panels(page_path)

            for p_img in panels:
                panel_count += 1
                fname = f"panel_{panel_count:03d}.jpg"
                p_out_1 = os.path.join(ch_panel_dir_1, fname)
                p_out_2 = os.path.join(ch_panel_dir_2, fname)
                
                # Save optimized high-res JPEG
                p_img.save(p_out_1, format="JPEG", quality=94, optimize=True)
                p_img.save(p_out_2, format="JPEG", quality=94, optimize=True)
                
                pw, ph = p_img.size
                chapter_panel_data.append({
                    "panel_id": panel_count,
                    "filename": fname,
                    "rel_path": f"Solo_Max_Level_Newbie/{ch}/panels/{fname}",
                    "width": pw,
                    "height": ph,
                    "aspect_ratio": round(ph / pw, 2),
                })

        manifest[ch] = {
            "chapter": ch_num,
            "total_panels": panel_count,
            "panels": chapter_panel_data,
        }
        total_panels_all_chapters += panel_count
        print(f"  ✔ {ch}: Created {panel_count} individual cropped panels in {ch}/panels/")

    manifest_path_1 = os.path.join(SRC_BASE, "panels_manifest.json")
    manifest_path_2 = os.path.join(PUBLIC_BASE, "panels_manifest.json")
    with open(manifest_path_1, 'w') as f:
        json.dump(manifest, f, indent=2)
    with open(manifest_path_2, 'w') as f:
        json.dump(manifest, f, indent=2)

    print("\n=================================================================")
    print("🎉 ALL 15 CHAPTERS SPLIT INTO INDIVIDUAL PANELS SUCCESSFULLY!")
    print(f"Total Individual Panels Generated: {total_panels_all_chapters} panels!")
    print(f"Manifest saved to: {manifest_path_1}")
    print("=================================================================")

if __name__ == "__main__":
    main()
