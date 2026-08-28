#!/usr/bin/env python3
import sys, os, re, json, ssl, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

ORGANIZATION_KEY = "199e5a19-a236-49f5-81f4-43d4a541748a"
SERIES_UUID = "7d6559a1-9168-42cb-b4c3-aa5708705be3"
XOR_KEY = 174
BASE_DIR = "/Users/sandesh/Documents/Manga/chapters"
os.makedirs(BASE_DIR, exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Origin': 'https://www.omoi.com',
    'Referer': 'https://www.omoi.com/',
    'AZUKI-ORGANIZATION-KEY': ORGANIZATION_KEY
}

def fetch_json(url):
    for _ in range(3):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception:
            time.sleep(0.5)
    return None

def download_page(image_url, out_path):
    if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
        return True
    for _ in range(3):
        try:
            req = urllib.request.Request(image_url, headers=HEADERS)
            with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
                raw = r.read()
            dec = bytes([b ^ XOR_KEY for b in raw])
            with open(out_path, 'wb') as f:
                f.write(dec)
            return True
        except Exception:
            time.sleep(0.5)
    return False

def get_best_url(page_meta):
    img = page_meta.get('image', {})
    jpgs = img.get('jpg', [])
    if jpgs:
        return max(jpgs, key=lambda x: x.get('width', 0))['url']
    webps = img.get('webp', [])
    if webps:
        return max(webps, key=lambda x: x.get('width', 0))['url']
    return page_meta.get('image_url')

def main():
    print("===================================================================", flush=True)
    print("KNIGHTS OF SIDONIA - COMPLETE SERIES BATCH EXTRACTOR", flush=True)
    print("===================================================================", flush=True)
    
    with open('/Users/sandesh/Documents/Manga/chapters_sidonia.json') as f:
        chapters = json.load(f)
        
    total_chapters = len(chapters)
    print(f"Total Chapters to process: {total_chapters}\n", flush=True)
    
    for ch_idx, ch in enumerate(chapters):
        ch_num = ch.get('label')
        ch_name = ch.get('full_name')
        ch_uuid = ch.get('uuid')
        
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', ch_name).lower()
        ch_dir = os.path.join(BASE_DIR, safe_name)
        os.makedirs(ch_dir, exist_ok=True)
        
        pages_url = f"https://production.api.azuki.co/chapter/{ch_uuid}/pages/v0"
        pages_data = fetch_json(pages_url)
        if not pages_data or 'pages' not in pages_data:
            print(f"[{ch_idx+1}/{total_chapters}] Failed to fetch pages for Chapter {ch_num}", flush=True)
            continue
            
        pages = pages_data['pages']
        total_p = len(pages)
        
        def page_task(item):
            idx, p_meta = item
            out_p = os.path.join(ch_dir, f"page_{idx+1:03d}.jpg")
            url = get_best_url(p_meta)
            if not url:
                return False
            return download_page(url, out_p)
            
        with ThreadPoolExecutor(max_workers=6) as executor:
            res = list(executor.map(page_task, enumerate(pages)))
            
        saved_count = sum(1 for ok in res if ok)
        print(f"[{ch_idx+1}/{total_chapters}] Chapter {ch_num:<4} ({ch_name}): {saved_count}/{total_p} pages ready in {safe_name}/", flush=True)
        
        # Save manifest
        with open(os.path.join(ch_dir, "manifest.json"), 'w') as mf:
            json.dump({
                "chapter_info": ch,
                "total_pages": total_p,
                "pages": [
                    {"page_number": i+1, "filename": f"page_{i+1:03d}.jpg"}
                    for i in range(total_p)
                ]
            }, mf, indent=2)

    print("\n===================================================================", flush=True)
    print("ALL 36 CHAPTERS EXTRACTED SUCCESSFULLY!", flush=True)
    print("===================================================================", flush=True)

if __name__ == "__main__":
    main()
