import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CameraMotion, SlideDirection } from "../types";

interface MangaPageProps {
  pagePath: string;
  motion: CameraMotion;
  slideDirection?: SlideDirection;
  sceneIndex: number;
  durationInFrames: number;
}

const ROTATING_DIRECTIONS: SlideDirection[] = [
  "from-right",
  "from-left",
  "from-bottom",
  "from-top-right",
  "from-left",
  "from-top",
  "from-bottom-left",
  "zoom-snap",
];

export const MangaPage: React.FC<MangaPageProps> = ({
  pagePath,
  motion,
  slideDirection,
  sceneIndex,
  durationInFrames,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 1. High-Energy Snappy Spring Physics for Fast Pacing
  const snapSpring = spring({
    frame,
    fps,
    config: {
      damping: 12,
      stiffness: 175,
      mass: 0.4,
    },
  });

  const effectiveDirection =
    slideDirection && slideDirection !== "auto"
      ? slideDirection
      : ROTATING_DIRECTIONS[sceneIndex % ROTATING_DIRECTIONS.length];

  let slideInX = 0;
  let slideInY = 0;
  let slideScaleMultiplier = 1.0;
  let slideRotate = 0;

  switch (effectiveDirection) {
    case "from-left":
      slideInX = interpolate(snapSpring, [0, 1], [-320, 0]);
      break;

    case "from-top":
      slideInY = interpolate(snapSpring, [0, 1], [-260, 0]);
      break;

    case "from-bottom":
      slideInY = interpolate(snapSpring, [0, 1], [260, 0]);
      break;

    case "from-top-right":
      slideInX = interpolate(snapSpring, [0, 1], [260, 0]);
      slideInY = interpolate(snapSpring, [0, 1], [-180, 0]);
      slideRotate = interpolate(snapSpring, [0, 1], [1.2, 0]);
      break;

    case "from-bottom-left":
      slideInX = interpolate(snapSpring, [0, 1], [-260, 0]);
      slideInY = interpolate(snapSpring, [0, 1], [180, 0]);
      slideRotate = interpolate(snapSpring, [0, 1], [-1.2, 0]);
      break;

    case "zoom-snap":
      slideScaleMultiplier = interpolate(snapSpring, [0, 1], [0.82, 1.0]);
      slideRotate = interpolate(snapSpring, [0, 1], [-1.5, 0]);
      break;

    case "from-right":
    default:
      slideInX = interpolate(snapSpring, [0, 1], [320, 0]);
      break;
  }

  const fadeIn = interpolate(frame, [0, 4], [0.5, 1], {
    extrapolateRight: "clamp",
  });

  // 2. Full-Page Reading Motion (Always dynamic and in sync with fast pacing)
  const progress = interpolate(frame, [0, durationInFrames], [0, 1], {
    extrapolateRight: "clamp",
  });

  let baseScale = 1.55;
  let moveX = 0;
  let moveY = 0;

  switch (motion) {
    case "scroll-down":
      baseScale = interpolate(frame, [0, durationInFrames], [1.52, 1.62]);
      moveY = interpolate(progress, [0, 1], [580, -580]);
      break;

    case "scroll-up":
      baseScale = interpolate(frame, [0, durationInFrames], [1.52, 1.62]);
      moveY = interpolate(progress, [0, 1], [-580, 580]);
      break;

    case "zoom-top-to-bottom":
      baseScale = interpolate(frame, [0, durationInFrames], [1.82, 1.68]);
      moveY = interpolate(progress, [0, 1], [620, -620]);
      break;

    case "pan-spread-left":
      baseScale = 1.45;
      moveX = interpolate(progress, [0, 1], [320, -320]);
      moveY = interpolate(progress, [0, 1], [100, -100]);
      break;

    case "pan-spread-right":
      baseScale = 1.45;
      moveX = interpolate(progress, [0, 1], [-320, 320]);
      moveY = interpolate(progress, [0, 1], [-100, 100]);
      break;

    case "zoom-overview-dive":
      baseScale = interpolate(progress, [0, 0.35, 1], [1.2, 1.55, 1.85]);
      moveY = interpolate(progress, [0, 0.35, 1], [0, 200, -300]);
      break;

    case "slow-drift-center":
    default:
      baseScale = interpolate(progress, [0, 1], [1.4, 1.6]);
      moveY = interpolate(progress, [0, 1], [120, -120]);
      break;
  }

  const finalScale = baseScale * slideScaleMultiplier;
  const finalTranslateX = moveX + slideInX;
  const finalTranslateY = moveY + slideInY;
  const imageSrc = staticFile(pagePath);

  return (
    <div
      style={{
        position: "relative",
        width: 1920,
        height: 1080,
        backgroundColor: "#020617",
        overflow: "hidden",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        opacity: fadeIn,
      }}
    >
      {/* 1. Ambient Blurred Background */}
      <div
        style={{
          position: "absolute",
          top: -80,
          left: -80,
          right: -80,
          bottom: -80,
          backgroundImage: `url(${imageSrc})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          filter: "blur(45px) brightness(0.25) saturate(1.4)",
          transform: `scale(${finalScale * 1.05})`,
          zIndex: 1,
        }}
      />

      {/* 2. Soft Edge Vignette */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          background:
            "radial-gradient(ellipse at center, transparent 70%, rgba(2, 6, 23, 0.5) 90%, rgba(2, 6, 23, 0.85) 100%)",
          zIndex: 2,
          pointerEvents: "none",
        }}
      />

      {/* 3. Main Full-Page Manga Image with Fast-Paced Dynamic Action */}
      <div
        style={{
          position: "absolute",
          width: "100%",
          height: "100%",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          transform: `translate(${finalTranslateX}px, ${finalTranslateY}px) scale(${finalScale}) rotate(${slideRotate}deg)`,
          transformOrigin: "center center",
          willChange: "transform",
          zIndex: 10,
        }}
      >
        <Img
          src={imageSrc}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "contain",
            filter: "contrast(1.06) brightness(1.02)",
          }}
        />
      </div>
    </div>
  );
};
