import { Composition } from "remotion";
import { MangaVideo } from "./MangaVideo";
import { SCENES } from "./storyData";
import { SoloNewbieVideo } from "./SoloNewbieVideo";
import { SOLO_SCENES } from "./soloNewbieStoryData";

export const VideoComposition = () => {
  const sidoniaTotalFrames = SCENES.reduce((acc, s) => acc + s.durationInFrames, 0);
  const soloTotalFrames = SOLO_SCENES.reduce((acc, s) => acc + s.durationInFrames, 0);

  return (
    <>
      {/* 1. Knights of Sidonia (3-Chapter Saga) */}
      <Composition
        id="KnightsOfSidoniaChapter1"
        component={MangaVideo}
        durationInFrames={sidoniaTotalFrames || 10426}
        fps={30}
        width={1920}
        height={1080}
      />

      {/* 2. Solo Max-Level Newbie (15-Chapter Manhwa Master Saga) */}
      <Composition
        id="SoloMaxLevelNewbie"
        component={SoloNewbieVideo}
        durationInFrames={soloTotalFrames || 6000}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
