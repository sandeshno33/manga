import React from "react";
import { SpeakerType } from "../types";

interface SubtitleBarProps {
  speaker: SpeakerType;
  text: string;
}

const SPEAKER_STYLES: Record<
  SpeakerType,
  { badgeBg: string; badgeBorder: string; badgeText: string; glow: string }
> = {
  Narrator: {
    badgeBg: "rgba(15, 23, 42, 0.85)",
    badgeBorder: "#38bdf8",
    badgeText: "#e0f2fe",
    glow: "rgba(56, 189, 248, 0.3)",
  },
  Nagate: {
    badgeBg: "rgba(22, 101, 52, 0.85)",
    badgeBorder: "#4ade80",
    badgeText: "#dcfce7",
    glow: "rgba(74, 222, 128, 0.35)",
  },
  Kunato: {
    badgeBg: "rgba(127, 29, 29, 0.85)",
    badgeBorder: "#f87171",
    badgeText: "#fee2e2",
    glow: "rgba(248, 113, 113, 0.35)",
  },
  Shizuka: {
    badgeBg: "rgba(131, 24, 67, 0.85)",
    badgeBorder: "#f472b6",
    badgeText: "#fce7f3",
    glow: "rgba(244, 114, 182, 0.35)",
  },
  Kobayashi: {
    badgeBg: "rgba(88, 28, 135, 0.85)",
    badgeBorder: "#c084fc",
    badgeText: "#f3e8ff",
    glow: "rgba(192, 132, 252, 0.35)",
  },
  Lala: {
    badgeBg: "rgba(120, 53, 15, 0.85)",
    badgeBorder: "#fbbf24",
    badgeText: "#fef3c7",
    glow: "rgba(251, 191, 36, 0.35)",
  },
  Instructor: {
    badgeBg: "rgba(124, 45, 18, 0.85)",
    badgeBorder: "#fb923c",
    badgeText: "#ffedd5",
    glow: "rgba(251, 146, 60, 0.35)",
  },
  Control: {
    badgeBg: "rgba(14, 116, 144, 0.85)",
    badgeBorder: "#22d3ee",
    badgeText: "#cffafe",
    glow: "rgba(34, 211, 238, 0.35)",
  },
  Ochiai: {
    badgeBg: "rgba(67, 56, 202, 0.85)",
    badgeBorder: "#818cf8",
    badgeText: "#e0e7ff",
    glow: "rgba(129, 140, 248, 0.35)",
  },
  Cadets: {
    badgeBg: "rgba(190, 24, 93, 0.85)",
    badgeBorder: "#f43f5e",
    badgeText: "#ffe4e6",
    glow: "rgba(244, 63, 94, 0.35)",
  },
  Honoka: {
    badgeBg: "rgba(13, 148, 136, 0.85)",
    badgeBorder: "#2dd4bf",
    badgeText: "#ccfbf1",
    glow: "rgba(45, 212, 191, 0.35)",
  },
  Elder: {
    badgeBg: "rgba(71, 85, 105, 0.85)",
    badgeBorder: "#94a3b8",
    badgeText: "#f1f5f9",
    glow: "rgba(148, 163, 184, 0.35)",
  },
  Worker: {
    badgeBg: "rgba(161, 98, 7, 0.85)",
    badgeBorder: "#facc15",
    badgeText: "#fef9c3",
    glow: "rgba(250, 204, 21, 0.35)",
  },
  Investigator: {
    badgeBg: "rgba(51, 65, 85, 0.85)",
    badgeBorder: "#64748b",
    badgeText: "#f8fafc",
    glow: "rgba(100, 116, 139, 0.35)",
  },
};

export const SubtitleBar: React.FC<SubtitleBarProps> = ({ speaker, text }) => {
  const style = SPEAKER_STYLES[speaker] || SPEAKER_STYLES.Narrator;

  return (
    <div
      style={{
        position: "absolute",
        bottom: 40,
        left: 0,
        right: 0,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 50,
        padding: "0 60px",
      }}
    >
      <div
        style={{
          background:
            "linear-gradient(180deg, rgba(15, 23, 42, 0.88) 0%, rgba(2, 6, 23, 0.96) 100%)",
          backdropFilter: "blur(16px)",
          borderRadius: 16,
          padding: "16px 28px",
          maxWidth: 1300,
          border: "1px solid rgba(255, 255, 255, 0.12)",
          boxShadow:
            "0 20px 40px -15px rgba(0,0,0,0.8), 0 0 25px rgba(56, 189, 248, 0.15)",
          display: "flex",
          alignItems: "center",
          gap: 20,
        }}
      >
        <span
          style={{
            background: style.badgeBg,
            color: style.badgeText,
            border: `1px solid ${style.badgeBorder}`,
            padding: "6px 14px",
            borderRadius: 8,
            fontSize: 18,
            fontWeight: 700,
            letterSpacing: "0.08em",
            textTransform: "uppercase",
            boxShadow: `0 0 14px ${style.glow}`,
            flexShrink: 0,
          }}
        >
          {speaker}
        </span>
        <p
          style={{
            color: "#f8fafc",
            fontSize: 24,
            fontWeight: 500,
            lineHeight: 1.45,
            margin: 0,
            textShadow: "0 2px 8px rgba(0,0,0,0.8)",
            letterSpacing: "0.01em",
          }}
        >
          {text}
        </p>
      </div>
    </div>
  );
};
