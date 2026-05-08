/**
 * Deaf Connect Configuration Settings
 */

export const CONFIG = {
  // Recognition Parameters
  SEQUENCE_LENGTH: 30,         // Number of frames for temporal analysis (LSTM)
  LANDMARK_DIMENSIONS: 63,     // 21 landmarks * (x, y, z)
  MAX_HANDS: 1,                // Single-hand tracking for performance
  MIN_DETECTION_CONFIDENCE: 0.5,
  MIN_TRACKING_CONFIDENCE: 0.5,
  
  // UI / UX Settings
  CONFIDENCE_THRESHOLD: 0.75,
  COOLDOWN_SECONDS: 1.5,
  SENTENCE_TIMEOUT: 2.5,
  
  // Video Resolution
  FRAME_WIDTH: 640,
  FRAME_HEIGHT: 480,
  
  // Colors for drawing skeleton
  SKELETON_COLORS: {
    JOINT: '#3B82F6',
    BONE: 'rgba(255, 255, 255, 0.4)',
    PALM: '#8B5CF6'
  }
};
