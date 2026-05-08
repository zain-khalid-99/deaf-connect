import mediapipe as mp
import numpy as np
import cv2
from utils.config import LANDMARK_DIMENSIONS, MIN_HAND_CONFIDENCE, MIN_TRACKING_CONFIDENCE

class LandmarkExtractor:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,      # False = video mode (faster)
            max_num_hands=1,              # Only track dominant hand
            min_detection_confidence=MIN_HAND_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE
        )

    def extract(self, frame: np.ndarray) -> np.ndarray | None:
        """
        Extracts and normalizes 21 landmarks from a single frame.
        Normalizes relative to wrist and scales by hand size.
        Returns shape (63,) or None if no hand detected.
        """
        # MediaPipe requires RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        if not results.multi_hand_landmarks:
            return None
            
        # Get first detected hand
        hand_landmarks = results.multi_hand_landmarks[0]
        
        # Extract raw coordinates
        landmarks = np.array([
            [lm.x, lm.y, lm.z]
            for lm in hand_landmarks.landmark
        ])  # shape: (21, 3)
        
        # Normalize relative to wrist (landmark 0)
        wrist = landmarks[0].copy()
        landmarks -= wrist
        
        # Scale by wrist-to-middle-fingertip distance (landmark 12)
        middle_tip = landmarks[12]
        scale = np.linalg.norm(middle_tip)
        
        if scale > 0:
            landmarks /= scale
            
        return landmarks.flatten()  # shape: (63,)

    def draw_landmarks(self, frame: np.ndarray, results) -> np.ndarray:
        """Draw hand skeleton on frame using MediaPipe drawing utils."""
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
                    self.mp_draw.DrawingSpec(color=(255, 255, 255), thickness=2)
                )
        return frame

    def close(self):
        self.hands.close()
