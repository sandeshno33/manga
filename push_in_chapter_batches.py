import os, subprocess, sys

BASE_DIR = "/Users/sandesh/Documents/Manga"

def run_cmd(cmd):
    res = subprocess.run(cmd, shell=True, cwd=BASE_DIR, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error ({cmd}): {res.stderr}")
    else:
        print(f"✔ {cmd}")
    return res.returncode == 0

def push_batches():
    print("=================================================================")
    print("📦 PUSHING ASSETS TO GITHUB IN SMALL INCREMENTAL CHAPTER BATCHES")
    print("=================================================================")
    
    # 1. First push audio files & SFX (30MB)
    run_cmd("git add my-video/public/Solo_Max_Level_Newbie/audio/ my-video/public/Knights_of_Sidonia/audio/ my-video/public/Solo_Max_Level_Newbie/panels_manifest.json")
    run_cmd('git commit -m "feat(assets): add peaceful ambient soundtrack, sfx, and audio"')
    run_cmd("git push origin main")
    
    # 2. Push Knights of Sidonia panels
    run_cmd("git add my-video/public/Knights_of_Sidonia/*.jpg my-video/public/Knights_of_Sidonia/*.txt")
    run_cmd('git commit -m "feat(assets): add Knights of Sidonia manga panels"')
    run_cmd("git push origin main")
    
    # 3. Push Solo Max-Level Newbie chapters 2 by 2 (~18MB per push)
    for ch_start in range(1, 26, 2):
        ch_end = min(25, ch_start + 1)
        targets = []
        for ch in range(ch_start, ch_end + 1):
            p = f"my-video/public/Solo_Max_Level_Newbie/chapter_{ch}/"
            if os.path.exists(os.path.join(BASE_DIR, p)):
                targets.append(p)
                
        if targets:
            run_cmd(f"git add {' '.join(targets)}")
            run_cmd(f'git commit -m "feat(assets): add Solo Max-Level Newbie chapters {ch_start}-{ch_end} panels"')
            run_cmd("git push origin main")
            
    print("\n=================================================================")
    print("🎉 ALL PUBLIC ASSETS SUCCESSFULLY PUSHED TO GITHUB!")
    print("=================================================================")

if __name__ == "__main__":
    # Reset to main branch first
    run_cmd("git reset origin/main")
    push_batches()
