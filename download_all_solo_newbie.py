import os, re, sys, asyncio, ssl, urllib.request

step_mapping = {
    1: "/Users/sandesh/.gemini/antigravity-ide/brain/1104cbdb-de87-4c1f-85a0-37ba23a0c480/.system_generated/steps/837/content.md",
    2: "/Users/sandesh/.gemini/antigravity-ide/brain/1104cbdb-de87-4c1f-85a0-37ba23a0c480/.system_generated/steps/902/content.md",
    3: "/Users/sandesh/.gemini/antigravity-ide/brain/1104cbdb-de87-4c1f-85a0-37ba23a0c480/.system_generated/steps/904/content.md",
    4: "/Users/sandesh/.gemini/antigravity-ide/brain/1104cbdb-de87-4c1f-85a0-37ba23a0c480/.system_generated/steps/906/content.md",
    5: "/Users/sandesh/.gemini/antigravity-ide/brain/1104cbdb-de87-4c1f-85a0-37ba23a0c480/.system_generated/steps/908/content.md",
    6: "/Users/sandesh/.gemini/antigravity-ide/brain/1104cbdb-de87-4c1f-85a0-37ba23a0c480/.system_generated/steps/910/content.md",
    7: "/Users/sandesh/.gemini/antigravity-ide/brain/1104cbdb-de87-4c1f-85a0-37ba23a0c480/.system_generated/steps/912/content.md",
    8: "/Users/sandesh/.gemini/antigravity-ide/brain/1104cbdb-de87-4c1f-85a0-37ba23a0c480/.system_generated/steps/914/content.md",
    9: "/Users/sandesh/.gemini/antigravity-ide/brain/1104cbdb-de87-4c1f-85a0-37ba23a0c480/.system_generated/steps/916/content.md",
    10: "/Users/sandesh/.gemini/antigravity-ide/brain/1104cbdb-de87-4c1f-85a0-37ba23a0c480/.system_generated/steps/918/content.md",
    11: "/Users/sandesh/.gemini/antigravity-ide/brain/1104cbdb-de87-4c1f-85a0-37ba23a0c480/.system_generated/steps/920/content.md",
    12: "/Users/sandesh/.gemini/antigravity-ide/brain/1104cbdb-de87-4c1f-85a0-37ba23a0c480/.system_generated/steps/922/content.md",
    13: "/Users/sandesh/.gemini/antigravity-ide/brain/1104cbdb-de87-4c1f-85a0-37ba23a0c480/.system_generated/steps/924/content.md",
    14: "/Users/sandesh/.gemini/antigravity-ide/brain/1104cbdb-de87-4c1f-85a0-37ba23a0c480/.system_generated/steps/926/content.md",
    15: "/Users/sandesh/.gemini/antigravity-ide/brain/1104cbdb-de87-4c1f-85a0-37ba23a0c480/.system_generated/steps/928/content.md",
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
        # Check if already downloaded
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

async def main():
    print("=================================================================")
    print("🚀 DOWNLOADING ALL 15 CHAPTERS OF SOLO MAX-LEVEL NEWBIE (1 HR)")
    print("=================================================================")
    
    sem = asyncio.Semaphore(10)
    total_downloaded = 0
    
    for ch_num, md_file in step_mapping.items():
        if not os.path.exists(md_file):
            print(f"Missing file for Chapter {ch_num}")
            continue
            
        with open(md_file, 'r', encoding='utf-8') as f:
            html = f.read()
            
        # Extract images from reading-content section
        reading_match = re.search(r'class="reading-content">(.*?)class="(?:related-reading-content|entry-header)', html, re.DOTALL)
        if reading_match:
            search_area = reading_match.group(1)
        else:
            search_area = html
            
        img_matches = re.findall(r'data-src=[\'\"]\s*(https?://[^\'\"]+)[\'\"]', search_area)
        
        # Filter out icons/placeholders
        cleaned = []
        for u in img_matches:
            u = u.strip()
            if 'dflazy' not in u and ('tngcdn.com' in u or 'uploads' in u):
                if u not in cleaned:
                    cleaned.append(u)
                    
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
            p1 = os.path.join(ch_dir_1, fname)
            p2 = os.path.join(ch_dir_2, fname)
            tasks.append(download_file(url, [p1, p2], sem))
            
        res = await asyncio.gather(*tasks)
        success = sum(1 for r in res if r)
        total_downloaded += success
        print(f"✔ Chapter {ch_num:02d}: {success}/{len(cleaned)} high-res panels downloaded -> Solo_Max_Level_Newbie/chapter_{ch_num}/")
        
    print("=================================================================")
    print(f"🎉 EXTRACTION COMPLETE! Total {total_downloaded} pages across 15 chapters!")
    print(f"📁 Local Directory: {OUT_BASE}")
    print(f"📁 Public Video Directory: {PUBLIC_BASE}")
    print("=================================================================")

if __name__ == "__main__":
    asyncio.run(main())
