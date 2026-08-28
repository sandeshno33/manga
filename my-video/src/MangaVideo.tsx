import React from "react";
import { Audio, Sequence, staticFile } from "remotion";
import { SCENES } from "./storyData";
import { MangaPage } from "./components/MangaPage";

export const MangaVideo: React.FC = () => {
  // Compute Act start frames and total durations for BGM layering
  const actInfo: Record<number, { startFrame: number; durationInFrames: number; bgmFile: string }> = {};

  let currentFrameCount = 0;
  SCENES.forEach((scene) => {
    const actNum = scene.act;
    if (!actInfo[actNum]) {
      actInfo[actNum] = {
        startFrame: currentFrameCount,
        durationInFrames: 0,
        bgmFile: `Knights_of_Sidonia/audio/bgm_act${actNum}.wav`,
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
      {/* 1. Ambient Background Music (BGM) Layers for Acts 1 through 15 */}
      {Object.entries(actInfo).map(([actNum, info]) => (
        <Sequence
          key={`bgm-act-${actNum}`}
          from={info.startFrame}
          durationInFrames={info.durationInFrames}
          name={`BGM Act ${actNum}`}
        >
          <Audio
            src={staticFile(info.bgmFile)}
            volume={0.28}
            loop
          />
        </Sequence>
      ))}

      {/* 2. Visual Manga Panels with Multi-Directional Snap-Slides & Character Voiceover */}
      {SCENES.map((scene, index) => {
        const startFrame = accumulatedFrames;
        const duration = scene.durationInFrames;
        accumulatedFrames += duration;

        // Custom SFX triggers for cinematic impact
        let sfxPath: string | null = null;
        if (scene.id === "46") sfxPath = "Knights_of_Sidonia/audio/sfx_catapult.wav";
        if (scene.id === "51") sfxPath = "Knights_of_Sidonia/audio/sfx_alarm.wav";
        if (scene.id === "60") sfxPath = "Knights_of_Sidonia/audio/sfx_thruster.wav";
        if (scene.id === "64") sfxPath = "Knights_of_Sidonia/audio/sfx_impact.wav";

        return (
          <Sequence
            key={scene.id}
            from={startFrame}
            durationInFrames={duration}
            name={`Scene ${scene.id} - ${scene.speaker} (Pg ${scene.page})`}
          >
            {/* Manga Page with Dynamic Directional Slide Transitions & Full Reading Scroll */}
            <MangaPage
              pagePath={scene.pagePath}
              motion={scene.motion}
              slideDirection={scene.slideDirection}
              sceneIndex={index}
              durationInFrames={duration}
            />

            {/* Character & Narrator Voiceover Audio */}
            {scene.audioFile && (
              <Audio
                src={staticFile(scene.audioFile)}
                volume={1.0}
                startFrom={0}
              />
            )}

            {/* Cinematic SFX Trigger */}
            {sfxPath && (
              <Audio
                src={staticFile(sfxPath)}
                volume={0.45}
                startFrom={0}
              />
            )}
          </Sequence>
        );
      })}
    </div>
  );
};
