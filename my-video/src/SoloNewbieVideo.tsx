import React from "react";
import { Audio, Sequence, staticFile } from "remotion";
import { SOLO_SCENES } from "./soloNewbieStoryData";
import { ManhwaPanel } from "./components/ManhwaPanel";

const ACT_BGM_MAP: Record<number, string> = {
  1: "Solo_Max_Level_Newbie/audio/bgm_tower_manifest.wav",
  2: "Solo_Max_Level_Newbie/audio/bgm_level_grind.wav",
  3: "Solo_Max_Level_Newbie/audio/bgm_level_grind.wav",
  4: "Solo_Max_Level_Newbie/audio/bgm_boss_battle.wav",
  5: "Solo_Max_Level_Newbie/audio/bgm_tower_manifest.wav",
  6: "Solo_Max_Level_Newbie/audio/bgm_vampire_crypt.wav",
  7: "Solo_Max_Level_Newbie/audio/bgm_level_grind.wav",
  8: "Solo_Max_Level_Newbie/audio/bgm_boss_battle.wav",
  9: "Solo_Max_Level_Newbie/audio/bgm_frost_peaks.wav",
};

export const SoloNewbieVideo: React.FC = () => {
  // Compute Act ranges for smooth, soothing ambient BGM layering
  const actInfo: Record<number, { startFrame: number; durationInFrames: number; bgmFile: string }> = {};

  let currentFrameCount = 0;
  SOLO_SCENES.forEach((scene) => {
    const actNum = scene.act;
    if (!actInfo[actNum]) {
      actInfo[actNum] = {
        startFrame: currentFrameCount,
        durationInFrames: 0,
        bgmFile: ACT_BGM_MAP[actNum] || "Solo_Max_Level_Newbie/audio/bgm_tower_manifest.wav",
      };
    }
    actInfo[actNum].durationInFrames += scene.durationInFrames;
    currentFrameCount += scene.durationInFrames;
  });

  let accumulatedFrames = 0;

  return (
    <div
      style={{
        width: 1920,
        height: 1080,
        backgroundColor: "#000000",
        overflow: "hidden",
        position: "relative",
      }}
    >
      {/* 1. Peaceful, Soothing Ambient Soundscape Layer (Sleep / Meditation friendly) */}
      {Object.entries(actInfo).map(([actNum, info]) => (
        <Sequence
          key={`solo-peaceful-bgm-${actNum}`}
          from={info.startFrame}
          durationInFrames={info.durationInFrames}
          name={`Ambient Soundscape Act ${actNum}`}
        >
          <Audio
            src={staticFile(info.bgmFile)}
            volume={0.16}
            loop
          />
        </Sequence>
      ))}

      {/* 2. Visual Manhwa Panels with Clear, Smooth Voiceover Dialogue (Zero harsh SFX) */}
      {SOLO_SCENES.map((scene, index) => {
        const startFrame = accumulatedFrames;
        const duration = scene.durationInFrames;
        accumulatedFrames += duration;

        return (
          <Sequence
            key={`solo-scene-${scene.id}`}
            from={startFrame}
            durationInFrames={duration}
            name={`Scene ${scene.id} - ${scene.speaker} (Ch ${scene.chapter})`}
          >
            {/* Manhwa Panel with Gentle Floating Camera Motion */}
            <ManhwaPanel
              pagePath={scene.pagePath}
              motion={scene.motion}
              slideDirection={scene.slideDirection}
              sceneIndex={index}
              durationInFrames={duration}
            />

            {/* Clear, Smooth Narration / Dialogue Voice */}
            {scene.audioFile && (
              <Audio
                src={staticFile(scene.audioFile)}
                volume={0.92}
                startFrom={0}
              />
            )}
          </Sequence>
        );
      })}
    </div>
  );
};
