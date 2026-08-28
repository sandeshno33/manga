import os, re, sys, asyncio, ssl, urllib.request
from PIL import Image
import numpy as np

step_mapping_extra = {
    16: "/Users/sandesh/.gemini/antigravity-ide/brain/1104cbdb-de87-4c1f-85a0-37ba23a0c480/.system_generated/steps/1136/content.md",
    17: "/Users/sandesh/.gemini/antigravity-ide/brain/1104cbdb-de87-4c1f-85a0-37ba23a0c480/.system_generated/steps/1138/content.md",
    18: "/Users/sandesh/.gemini/antigravity-ide/brain/1104cbdb-de87-4c1f-85a0-37ba23a0c480/.system_generated/steps/1140/content.md",
    19: "/Users/sandesh/.gemini/antigravity-ide/brain/1104cbdb-de87-4c1f-85a0-37ba23a0c480/.system_generated/steps/1142/content.md",
    20: "/Users/sandesh/.gemini/antigravity-ide/brain/1104cbdb-de87-4c1f-85a0-37ba23a0c480/.system_generated/steps/1144/content.md",
    21: "/Users/sandesh/.gemini/antigravity-ide/brain/1104cbdb-de87-4c1f-85a0-37ba23a0c480/.system_generated/steps/1146/content.md",
    22: "/Users/sandesh/.gemini/antigravity-ide/brain/1104cbdb-de87-4c1f-85a0-37ba23a0c480/.system_generated/steps/1148/content.md",
    23: "/Users/sandesh/.gemini/antigravity-ide/brain/1104cbdb-de87-4c1f-85a0-37ba23a0c480/.system_generated/steps/1150/content.md",
    24: "/Users/sandesh/.gemini/antigravity-ide/brain/1104cbdb-de87-4c1f-85a0-37ba23a0c480/.system_generated/steps/1152/content.md",
    25: "/Users/sandesh/.gemini/antigravity-ide/brain/1104cbdb-de87-4c1f-85a0-37ba23a0c480/.system_generated/steps/1154/content.md",
}

OUT_BASE = "/Users/sandesh/Documents/Manga/Solo_Max_Level_Newbie"
PUBLIC_BASE = "/Users/sandesh/Documents/Manga/my-video/public/Solo_Max_Level_Newbie"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Referer': 'https://www.toongod.org/',
}

async def download_file(url, target_paths, sem):
    async with sem:
        if all(os.path.exists(p) and os.path.getsize(p) > 5000 for p in target_paths):
            return True
        for attempt in range(4):
            try:
                req = urllib.request.Request(url, headers=HEADERS)
                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, lambda: urllib.request.urlopen(req, context=ctx, timeout=15).read())
                for p in target_paths:
                    with open(p, 'wb') as f:
                        f.write(data)
                return True
            except Exception:
                await asyncio.sleep(0.8)
        return False

def split_and_clean_chapter(ch_num):
    ch_src = os.path.join(OUT_BASE, f"chapter_{ch_num}")
    ch_pub = os.path.join(PUBLIC_BASE, f"chapter_{ch_num}")
    p_dir_1 = os.path.join(ch_src, "panels")
    p_dir_2 = os.path.join(ch_pub, "panels")
    os.makedirs(p_dir_1, exist_ok=True)
    os.makedirs(p_dir_2, exist_ok=True)
    
    # Import our panel splitter logic
    from split_all_webtoon_panels import split_strip_into_panels
    
    page_files = sorted([f for f in os.listdir(ch_src) if f.startswith("page_") and f.endswith(('.jpg', '.png', '.webp'))])
    
    raw_panels = []
    for f in page_files:
        p_path = os.path.join(ch_src, f)
        # Check if first page is credit/title card
        if f == "page_001.jpg":
            with Image.open(p_path) as test_img:
                w, h = test_img.size
                if (h / w) < 2.0 or h < 1200:
                    continue # skip credit card
        # Check if last page is promo banner
        if f == page_files[-1]:
            with Image.open(p_path) as test_img:
                w, h = test_img.size
                if (h / w) < 1.0 or h < 600:
                    continue # skip promo banner
                    
        panels = split_strip_into_panels(p_path)
        for p in panels:
            raw_panels.append(p)
            
    # Now merge isolated speech bubbles (< 600px) with adjacent panels
    merged = []
    i = 0
    while i < len(raw_panels):
        curr = raw_panels[i]
        cw, ch = curr.size
        if ch < 600 and i + 1 < len(raw_panels):
            nxt = raw_panels[i+1]
            nw, nh = nxt.size
            mw = max(cw, nw)
            mh = ch + nh
            comb = Image.new("RGB", (mw, mh), (255, 255, 255))
            comb.paste(curr, (0, 0))
            comb.paste(nxt, (0, ch))
            merged.append(comb)
            i += 2
        elif ch < 500 and len(merged) > 0:
            prev = merged.pop()
            pw, ph = prev.size
            mw = max(pw, cw)
            mh = ph + ch
            comb = Image.new("RGB", (mw, mh), (255, 255, 255))
            comb.paste(prev, (0, 0))
            comb.paste(curr, (0, ph))
            merged.append(comb)
            i += 1
        else:
            merged.append(curr)
            i += 1
            
    # Save all final panels
    for idx, p_img in enumerate(merged):
        fname = f"panel_{idx+1:03d}.jpg"
        p1 = os.path.join(p_dir_1, fname)
        p2 = os.path.join(p_dir_2, fname)
        p_img.save(p1, format="JPEG", quality=94, optimize=True)
        p_img.save(p2, format="JPEG", quality=94, optimize=True)
        
    print(f"✔ Chapter {ch_num:02d}: {len(merged)} pure story panels ready in chapter_{ch_num}/panels/")
    return len(merged)

async def main():
    print("=================================================================")
    print("🚀 DOWNLOADING & PROCESSING CHAPTERS 16 TO 25 (FOR 1-HR VIDEO)")
    print("=================================================================")
    
    sem = asyncio.Semaphore(10)
    for ch_num, md_file in step_mapping_extra.items():
        if not os.path.exists(md_file):
            continue
        with open(md_file, 'r', encoding='utf-8') as f:
            html = f.read()
            
        reading_match = re.search(r'class="reading-content">(.*?)class="(?:related-reading-content|entry-header)', html, re.DOTALL)
        search_area = reading_match.group(1) if reading_match else html
        img_matches = re.findall(r'data-src=[\'\"]\s*(https?://[^\'\"]+)[\'\"]', search_area)
        
        cleaned = [u.strip() for u in img_matches if 'dflazy' not in u and ('tngcdn.com' in u or 'uploads' in u)]
        
        ch_dir_1 = os.path.join(OUT_BASE, f"chapter_{ch_num}")
        ch_dir_2 = os.path.join(PUBLIC_BASE, f"chapter_{ch_num}")
        os.makedirs(ch_dir_1, exist_ok=True)
        os.makedirs(ch_dir_2, exist_ok=True)
        
        tasks = []
        for idx, url in enumerate(cleaned):
            ext = ".jpg"
            if ".png" in url.lower(): ext = ".png"
            elif ".webp" in url.lower(): ext = ".webp"
            fname = f"page_{idx+1:03d}{ext}"
            tasks.append(download_file(url, [os.path.join(ch_dir_1, fname), os.path.join(ch_dir_2, fname)], sem))
            
        await asyncio.gather(*tasks)
        split_and_clean_chapter(ch_num)
        
    print("=================================================================")
    print("🎉 ALL 25 CHAPTERS DOWNLOADED, CLEANED & SPLIT SUCCESSFULLY!")
    print("=================================================================")

if __name__ == "__main__":
    asyncio.run(main())
