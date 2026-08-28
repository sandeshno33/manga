# 🎬 Manga & Webtoon Motion Comic Studio

An automated AI-driven motion comic and manhwa recap video studio built with **Remotion**, **React**, **TypeScript**, **Python**, and **Edge-TTS**.

---

## 🌟 Features

- 📖 **Smart Webtoon Panel Splitter**: Automated gutter detection and seamless vertical text-box merging to transform vertical webtoon strips into high-resolution widescreen panels.
- 🎨 **Full-Bleed 16:9 Motion Engine**: Dynamic directional snap-slides (`from-right`, `from-left`, `from-top`, `zoom-snap`), color-matched ambient backdrop glow, and peaceful reading micro-drifts.
- 🎙️ **Multi-Character Neural Voice Acting**: Realistic character voiceovers using neural TTS models with customizable speech rates and tone calibration.
- 🍃 **Peaceful Sleep Ambient Soundscapes**: 432Hz harmonic meditation pads, dream drift lo-fi soundscapes, and clean, peaceful BGM layering.
- ⏱️ **Exact Video Runtime Synchronization**: Frame-perfect alignment ensuring zero cut-off dialogue and seamless multi-act story transitions.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd my-video
npm install
```

### 2. Launch Remotion Studio
```bash
npm run dev
# or from root:
npm run studio
```
Access the interactive video preview at `http://localhost:3001`.

### 3. Render High-Efficiency MP4
```bash
# Render Solo Max-Level Newbie Master Saga
npm run render:solo

# Render Knights of Sidonia Trilogy
npm run render:sidonia
```

---

## 📁 Project Structure

```
├── my-video/
│   ├── public/                # Static audio, SFX, and panel assets
│   │   ├── Solo_Max_Level_Newbie/
│   │   └── Knights_of_Sidonia/
│   ├── src/
│   │   ├── components/        # ManhwaPanel & MangaPanel components
│   │   ├── SoloNewbieVideo.tsx# Master Remotion composition
│   │   ├── soloNewbieStoryData.ts # Scene timeline definitions
│   │   └── Root.tsx           # Remotion Root registration
├── Solo_Max_Level_Newbie/     # Extracted 25-chapter raw & split panels
├── package.json               # Root scripts
└── README.md
```
