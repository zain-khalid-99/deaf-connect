import { Hands, type Results, type LandmarkList } from '@mediapipe/hands';
import { Camera } from '@mediapipe/camera_utils';
import { CONFIG } from '../utils/config';

export class HandLandmarker {
  private hands: Hands;
  private camera: Camera | null = null;

  constructor(onResults: (results: Results) => void) {
    this.hands = new Hands({
      locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
      },
    });

    this.hands.setOptions({
      maxNumHands: CONFIG.MAX_HANDS,
      modelComplexity: 1,
      minDetectionConfidence: CONFIG.MIN_DETECTION_CONFIDENCE,
      minTrackingConfidence: CONFIG.MIN_TRACKING_CONFIDENCE,
    });

    this.hands.onResults(onResults);
  }

  public async start(videoElement: HTMLVideoElement) {
    this.camera = new Camera(videoElement, {
      onFrame: async () => {
        await this.hands.send({ image: videoElement });
      },
      width: CONFIG.FRAME_WIDTH,
      height: CONFIG.FRAME_HEIGHT,
    });
    await this.camera.start();
  }

  public stop() {
    this.camera?.stop();
    this.hands.close();
  }
}

/**
 * Normalizes landmarks relative to the wrist (landmark 0)
 */
export const extractAndNormalizeLandmarks = (landmarks: LandmarkList) => {
  if (!landmarks) return new Array(CONFIG.LANDMARK_DIMENSIONS).fill(0);

  const wrist = landmarks[0];
  // Flatten and normalize relative to wrist
  const flattened = landmarks.flatMap(lm => [
    lm.x - wrist.x,
    lm.y - wrist.y,
    lm.z - wrist.z
  ]);

  return flattened;
};

/**
 * Custom Sci-Fi Skeleton Drawing
 */
export const drawHandSkeleton = (ctx: CanvasRenderingContext2D, landmarks: LandmarkList) => {
  const connections = [
    [0, 1, 2, 3, 4], // thumb
    [0, 5, 6, 7, 8], // index
    [0, 9, 10, 11, 12], // middle
    [0, 13, 14, 15, 16], // ring
    [0, 17, 18, 19, 20], // pinky
    [5, 9, 13, 17, 5] // palm base
  ];

  ctx.lineWidth = 2;
  ctx.lineCap = 'round';

  connections.forEach(path => {
    ctx.beginPath();
    ctx.strokeStyle = CONFIG.SKELETON_COLORS.BONE;
    for (let i = 0; i < path.length; i++) {
      const lm = landmarks[path[i]];
      const x = lm.x * ctx.canvas.width;
      const y = lm.y * ctx.canvas.height;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();
  });

  // Joints
  landmarks.forEach((lm, i) => {
    const x = lm.x * ctx.canvas.width;
    const y = lm.y * ctx.canvas.height;
    ctx.beginPath();
    ctx.arc(x, y, i === 0 ? 5 : 2, 0, 2 * Math.PI);
    ctx.fillStyle = i === 0 ? CONFIG.SKELETON_COLORS.PALM : CONFIG.SKELETON_COLORS.JOINT;
    if (i === 0) {
      ctx.shadowBlur = 10;
      ctx.shadowColor = CONFIG.SKELETON_COLORS.PALM;
    }
    ctx.fill();
    ctx.shadowBlur = 0;
  });
};
