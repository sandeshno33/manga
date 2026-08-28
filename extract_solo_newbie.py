import os, sys, time, re, asyncio, ssl, urllib.request
from playwright.async_api import async_playwright

BASE_OUTPUT_DIR = "/Users/sandesh/Documents/Manga/Solo_Max_Level_Newbie"
os.makedirs(BASE_OUTPUT_DIR, exist_ok=True)

# For a 1-hour recap video, 15 to 18 chapters gives the perfect Season 1 Opening Arc (~50-65 min)
CHAPTER_NUMS = list(range(1, 19)) # Chapters 1 to 18

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Referer': 'https://www.toongod.org/',
}

async def download_image(url, out_path, sem):
    async with sem:
        if os.path.exists(out_path) and os.path.getsize(out_path) > 5000:
            return True
        for attempt in range(4):
            try:
                req = urllib.request.Request(url, headers=HEADERS)
                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, lambda: urllib.request.urlopen(req, context=ctx, timeout=15).read())
                with open(out_path, 'wb') as f:
                    f.write(data)
                return True
            except Exception as e:
                if attempt == 3:
                    print(f"    ❌ Failed to download {url}: {e}")
                await asyncio.sleep(1.0)
        return False

async def process_chapter(browser, ch_num):
    url = f"https://www.toongod.org/webtoon/solo-max-level-newbie/chapter-{ch_num}/"
    ch_dir = os.path.join(BASE_OUTPUT_DIR, f"chapter_{ch_num}")
    os.makedirs(ch_dir, exist_ok=True)
    
    print(f"\n=======================================================")
    print(f"📖 Extracting Chapter {ch_num} from: {url}")
    print(f"=======================================================")
    
    page = await browser.new_page()
    img_urls = []
    
    try:
        await page.goto(url, timeout=45000, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        
        # Scroll down to trigger lazy loading if needed
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
        await page.wait_for_timeout(1000)
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(1000)
        
        img_urls = await page.evaluate('''() => {
            const elements = document.querySelectorAll('.reading-content img');
            return Array.from(elements)
                .map(img => img.getAttribute('data-src') || img.getAttribute('src') || img.src)
                .filter(u => u && !u.includes('dflazy.jpg') && (u.startsWith('http') || u.startsWith('//')));
        }''')
        
    except Exception as e:
        print(f"  ⚠️ Browser navigation warning: {e}")
    finally:
        await page.close()
        
    # Clean URLs
    cleaned_urls = []
    for u in img_urls:
        u = u.strip()
        if u.startswith('//'):
            u = 'https:' + u
        if u not in cleaned_urls:
            cleaned_urls.append(u)
            
    print(f"  Found {len(cleaned_urls)} high-resolution panels for Chapter {ch_num}.")
    
    sem = asyncio.Semaphore(6)
    dl_tasks = []
    for idx, img_url in enumerate(cleaned_urls):
        ext = ".jpg"
        if ".png" in img_url.lower():
            ext = ".png"
        elif ".webp" in img_url.lower():
            ext = ".webp"
        out_file = os.path.join(ch_dir, f"page_{idx+1:03d}{ext}")
        dl_tasks.append(download_image(img_url, out_file, sem))
        
    results = await asyncio.gather(*dl_tasks)
    success_count = sum(1 for r in results if r)
    print(f"  ✔ Downloaded {success_count}/{len(cleaned_urls)} pages into Solo_Max_Level_Newbie/chapter_{ch_num}/")
    return {"chapter": ch_num, "total_pages": len(cleaned_urls), "downloaded": success_count}

async def main():
    print(f"🚀 Starting Solo Max-Level Newbie High-Speed Extractor")
    print(f"Targeting Chapters 1 to {CHAPTER_NUMS[-1]} for 1-Hour Long Video Recap...")
    
    summary = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
        )
        
        for ch in CHAPTER_NUMS:
            res = await process_chapter(browser, ch)
            summary.append(res)
            await asyncio.sleep(1.0)
            
        await browser.close()
        
    print("\n=======================================================")
    print("🎉 ALL CHAPTERS EXTRACTED SUCCESSFULLY!")
    print("=======================================================")
    total_pages = sum(s["downloaded"] for s in summary)
    print(f"Total Chapters Extracted: {len(summary)}")
    print(f"Total High-Resolution Pages: {total_pages}")
    print(f"Directory: {BASE_OUTPUT_DIR}")

if __name__ == "__main__":
    asyncio.run(main())
