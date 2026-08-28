import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CameraMotion, SlideDirection } from "../types";

interface ManhwaPanelProps {
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
  "from-top",
  "zoom-snap",
  "from-right",
  "from-left",
];

export const ManhwaPanel: React.FC<ManhwaPanelProps> = ({
  pagePath,
  motion,
  slideDirection,
  sceneIndex,
  durationInFrames,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 1. Soft, Smooth Entrance Spring
  const smoothSpring = spring({
    frame,
    fps,
    config: {
      damping: 24,
      stiffness: 90,
      mass: 0.5,
    },
  });

  const effectiveDirection =
    slideDirection && slideDirection !== "auto"
      ? slideDirection
      : ROTATING_DIRECTIONS[sceneIndex % ROTATING_DIRECTIONS.length];

  let slideInX = 0;
  let slideInY = 0;
  let slideScaleMultiplier = 1.0;

  switch (effectiveDirection) {
    case "from-left":
      slideInX = interpolate(smoothSpring, [0, 1], [-120, 0]);
      break;

    case "from-top":
      slideInY = interpolate(smoothSpring, [0, 1], [-90, 0]);
      break;

    case "from-bottom":
      slideInY = interpolate(smoothSpring, [0, 1], [90, 0]);
      break;

    case "zoom-snap":
      slideScaleMultiplier = interpolate(smoothSpring, [0, 1], [0.95, 1.0]);
      break;

    case "from-right":
    default:
      slideInX = interpolate(smoothSpring, [0, 1], [120, 0]);
      break;
  }

  const fadeIn = interpolate(frame, [0, 6], [0.4, 1], {
    extrapolateRight: "clamp",
  });

  // 2. Subtle, Peaceful Camera Motion
  const progress = interpolate(frame, [0, durationInFrames], [0, 1], {
    extrapolateRight: "clamp",
  });

  let moveX = 0;
  let moveY = 0;

  switch (motion) {
    case "scroll-down":
      moveY = interpolate(progress, [0, 1], [30, -30]);
      break;

    case "scroll-up":
      moveY = interpolate(progress, [0, 1], [-30, 30]);
      break;

    case "pan-spread-left":
      moveX = interpolate(progress, [0, 1], [30, -30]);
      break;

    case "pan-spread-right":
      moveX = interpolate(progress, [0, 1], [-30, 30]);
      break;

    case "slow-drift-center":
    default:
      moveY = interpolate(progress, [0, 1], [15, -15]);
      break;
  }

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
      {/* 1. Ambient Blurred Backdrop for Full-Bleed 16:9 Widescreen */}
      <div
        style={{
          position: "absolute",
          top: -60,
          left: -60,
          right: -60,
          bottom: -60,
          backgroundImage: `url(${imageSrc})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          filter: "blur(55px) brightness(0.24) saturate(1.4)",
          transform: "scale(1.15)",
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
            "radial-gradient(ellipse at center, transparent 70%, rgba(2, 6, 23, 0.35) 88%, rgba(2, 6, 23, 0.85) 100%)",
          zIndex: 2,
          pointerEvents: "none",
        }}
      />

      {/* 3. Main Manhwa Panel Touching 100% Top and Bottom (Full Vertical Bleed) */}
      <div
        style={{
          position: "absolute",
          top: 0,
          bottom: 0,
          left: 0,
          right: 0,
          width: "100%",
          height: "100%",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          transform: `translate(${finalTranslateX}px, ${finalTranslateY}px) scale(${slideScaleMultiplier})`,
          transformOrigin: "center center",
          willChange: "transform",
          zIndex: 10,
        }}
      >
        <Img
          src={imageSrc}
          style={{
            height: "100%",
            width: "auto",
            maxHeight: "100%",
            objectFit: "contain",
            boxShadow:
              "0 0 60px rgba(0, 0, 0, 0.9), 0 0 120px rgba(0, 0, 0, 0.6)",
            filter: "contrast(1.03) brightness(1.01)",
          }}
        />
      </div>
    </div>
  );
};
