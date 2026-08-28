import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

interface ActCardProps {
  actTitle: string;
  durationInFrames: number;
}

export const ActCard: React.FC<ActCardProps> = ({
  actTitle,
  durationInFrames,
}) => {
  const frame = useCurrentFrame();

  const opacity = interpolate(
    frame,
    [0, 15, durationInFrames - 15, durationInFrames],
    [0, 1, 1, 0],
    { extrapolateRight: "clamp" }
  );

  const scale = interpolate(frame, [0, durationInFrames], [0.95, 1.05], {
    extrapolateRight: "clamp",
  });

  const scanlineY = interpolate(frame, [0, durationInFrames], [-200, 1200]);

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: 1920,
        height: 1080,
        backgroundColor: "rgba(3, 7, 18, 0.94)",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 80,
        opacity,
        overflow: "hidden",
      }}
    >
      {/* Scanning Laser Line */}
      <div
        style={{
          position: "absolute",
          top: scanlineY,
          left: 0,
          right: 0,
          height: 2,
          background: "linear-gradient(90deg, transparent, #06b6d4, transparent)",
          boxShadow: "0 0 15px #06b6d4",
        }}
      />

      <div
        style={{
          transform: `scale(${scale})`,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 16,
          padding: "40px 80px",
          background: "rgba(15, 23, 42, 0.8)",
          border: "2px solid rgba(6, 182, 212, 0.4)",
          borderRadius: 16,
          boxShadow: "0 0 60px rgba(6, 182, 212, 0.3)",
        }}
      >
        <div
          style={{
            color: "#38bdf8",
            fontFamily: "sans-serif",
            fontSize: 20,
            fontWeight: 800,
            letterSpacing: 4,
            textTransform: "uppercase",
          }}
        >
          KNIGHTS OF SIDONIA — CHAPTER 1
        </div>

        <div
          style={{
            color: "#ffffff",
            fontFamily: "sans-serif",
            fontSize: 48,
            fontWeight: 900,
            letterSpacing: 2,
            textAlign: "center",
            textTransform: "uppercase",
            textShadow: "0 0 20px rgba(6, 182, 212, 0.8)",
          }}
        >
          {actTitle}
        </div>
      </div>
    </div>
  );
};
