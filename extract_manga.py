#!/usr/bin/env python3
"""
High-Speed Manga Page Extractor and Decryptor for Knights of Sidonia (Omoi / Azuki).
Downloads each chapter's pages with 12 parallel threads, automatically advancing through all chapters.
"""

import sys
import os
import re
import json
import ssl
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ORGANIZATION_KEY = "199e5a19-a236-49f5-81f4-43d4a541748a"
SERIES_UUID = "7d6559a1-9168-42cb-b4c3-aa5708705be3"  # Knights of Sidonia
XOR_KEY = 174  # 0xAE

def get_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def fetch_json(url: str, retries: int = 3):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Origin': 'https://www.omoi.com',
        'Referer': 'https://www.omoi.com/',
        'AZUKI-ORGANIZATION-KEY': ORGANIZATION_KEY
    }
    ctx = get_ssl_context()
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=ctx, timeout=12) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            if attempt == retries - 1:
                raise e
            time.sleep(0.8)

def get_all_chapters():
    url = f"https://production.api.azuki.co/series/{SERIES_UUID}/chapters/v0"
    return fetch_json(url)

def download_and_decrypt_page(image_url: str, output_path: str, retries: int = 3) -> bool:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Origin': 'https://www.omoi.com',
        'Referer': 'https://www.omoi.com/'
    }
    ctx = get_ssl_context()
    for attempt in range(retries):
        try:
            req = urllib.request.Request(image_url, headers=headers)
            with urllib.request.urlopen(req, context=ctx, timeout=12) as response:
                encrypted_bytes = response.read()

            decrypted_bytes = bytes([b ^ XOR_KEY for b in encrypted_bytes])
            with open(output_path, 'wb') as f:
                f.write(decrypted_bytes)
            return True
        except Exception as e:
            if attempt == retries - 1:
                raise e
            time.sleep(0.5)
    return False

def get_best_image_url(page_meta: dict) -> str:
    img_obj = page_meta.get('image', {})
    jpg_list = img_obj.get('jpg', [])
    if jpg_list:
        best = max(jpg_list, key=lambda x: x.get('width', 0))
        return best['url']
        
    webp_list = img_obj.get('webp', [])
    if webp_list:
        best = max(webp_list, key=lambda x: x.get('width', 0))
        return best['url']
        
    if 'image_url' in page_meta:
        return page_meta['image_url']
        
    raise ValueError(f"Could not find valid image URL: {page_meta}")

def extract_chapter(chapter_uuid: str, output_base_dir: str = "/Users/sandesh/Documents/Manga/chapters"):
    # 1. Fetch Chapter Metadata
    manifest_url = f"https://production.api.azuki.co/chapter/{chapter_uuid}/v1"
    manifest_data = fetch_json(manifest_url)
    chapter_info = manifest_data.get('chapter', {})
    chapter_name = chapter_info.get('full_name', f"Chapter_{chapter_uuid[:8]}")
    label = chapter_info.get('label', '1')
    
    safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', chapter_name).lower()
    chapter_dir = os.path.join(output_base_dir, safe_name)
    os.makedirs(chapter_dir, exist_ok=True)
    
    # 2. Fetch Pages List
    pages_url = f"https://production.api.azuki.co/chapter/{chapter_uuid}/pages/v0"
    pages_data = fetch_json(pages_url)
    pages = pages_data.get('pages', [])
    total_pages = len(pages)
    
    print(f"▶ [{chapter_name}] ({total_pages} pages)...", flush=True)
    
    # 3. Parallel Download & Decryption
    def worker(item):
        idx, page_meta = item
        out_filename = f"page_{idx+1:03d}.jpg"
        out_path = os.path.join(chapter_dir, out_filename)
        
        if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
            return idx + 1, True
        
        try:
            image_url = get_best_image_url(page_meta)
            download_and_decrypt_page(image_url, out_path)
            return idx + 1, True
        except Exception as e:
            return idx + 1, False

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(worker, enumerate(pages)))
    
    success_count = sum(1 for _, ok in results if ok)
    print(f"✔ [{chapter_name}] Completed ({success_count}/{total_pages} pages)", flush=True)
    
    # Save chapter manifest
    with open(os.path.join(chapter_dir, "manifest.json"), 'w') as f:
        json.dump({
            "chapter_info": chapter_info,
            "total_pages": total_pages,
            "pages": [
                {
                    "page_number": idx + 1,
                    "filename": f"page_{idx+1:03d}.jpg",
                    "spread_index": p.get("spread_index", 0),
                    "spread_position": p.get("spread_position", "single")
                }
                for idx, p in enumerate(pages)
            ]
        }, f, indent=2)
        
    return chapter_dir

def main():
    if len(sys.argv) < 2:
        print("Knights of Sidonia Manga Extractor")
        print("Usage:")
        print("  python3 extract_manga.py --list")
        print("  python3 extract_manga.py <chapter_number>")
        print("  python3 extract_manga.py <range> (e.g. 1-10)")
        print("  python3 extract_manga.py --all")
        return

    arg = sys.argv[1].strip()
    
    if arg in ["--list", "-l", "list"]:
        chapters = get_all_chapters()
        print(f"\nFound {len(chapters)} Chapters on Omoi / Azuki:")
        print("=" * 70)
        for c in chapters:
            print(f"Chapter {c.get('label'):<4} | Order {c.get('order_number'):<5} | UUID: {c.get('uuid')} | {c.get('full_name')}")
        print("=" * 70)
        return

    if arg in ["--all", "-a", "all"]:
        chapters = get_all_chapters()
        print(f"Starting batch extraction for all {len(chapters)} chapters...\n", flush=True)
        for idx, c in enumerate(chapters):
            print(f"[{idx+1}/{len(chapters)}] Starting: {c.get('full_name')}", flush=True)
            try:
                extract_chapter(c['uuid'])
            except Exception as e:
                print(f"Error extracting {c.get('full_name')}: {e}", flush=True)
        print("\nAll chapters successfully extracted!", flush=True)
        return

    if "-" in arg and arg.replace("-", "").isdigit():
        start, end = map(int, arg.split("-"))
        chapters = get_all_chapters()
        ch_map = {str(c.get('label')).strip(): c for c in chapters}
        targets = [ch_map[str(num)] for num in range(start, end + 1) if str(num) in ch_map]
        
        for idx, c in enumerate(targets):
            print(f"[{idx+1}/{len(targets)}] Starting: {c.get('full_name')}", flush=True)
            extract_chapter(c['uuid'])
        return

    if arg.isdigit() or (arg.startswith("ch") and arg[2:].isdigit()):
        num = arg.replace("ch", "").strip()
        chapters = get_all_chapters()
        for c in chapters:
            if str(c.get('label')).strip() == num:
                extract_chapter(c['uuid'])
                return
        print(f"Chapter {num} not found.")
        return

    uuid_pattern = r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'
    match = re.search(uuid_pattern, arg)
    if match:
        extract_chapter(match.group(0))
        return
    
    print(f"Could not understand argument: {arg}")

if __name__ == "__main__":
    main()
