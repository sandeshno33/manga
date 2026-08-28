export type SpeakerType =
  | "Narrator"
  | "Nagate"
  | "Kunato"
  | "Shizuka"
  | "Kobayashi"
  | "Lala"
  | "Instructor"
  | "Control"
  | "Ochiai"
  | "Cadets"
  | "Honoka"
  | "Elder"
  | "Worker"
  | "Investigator";

export type CameraMotion =
  | "scroll-down"
  | "scroll-up"
  | "pan-spread-left"
  | "pan-spread-right"
  | "zoom-top-to-bottom"
  | "zoom-overview-dive"
  | "slow-drift-center";

export type SlideDirection =
  | "from-right"
  | "from-left"
  | "from-top"
  | "from-bottom"
  | "from-top-right"
  | "from-bottom-left"
  | "zoom-snap"
  | "auto";

export interface SceneItem {
  id: string;
  act: number;
  page: number;
  pagePath: string;
  speaker: SpeakerType;
  motion: CameraMotion;
  slideDirection?: SlideDirection;
  audioFile?: string;
  durationInFrames: number;
}
