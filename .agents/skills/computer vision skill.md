# Computer Vision Skill — ASL Recognition Project

## Purpose
This skill covers OpenCV and MediaPipe usage for real-time hand detection, landmark extraction, frame processing, and webcam handling in the ASL recognition system.

## When to Apply
- Writing `core/landmark_extractor.py`
- Processing webcam frames in Streamlit
- Drawing hand skeleton overlays on video frames
- Debugging hand detection issues

---

## MediaPipe Hands Setup

### Initialization
```python
import mediapipe as mp
import numpy as np
import cv2

class LandmarkExtractor:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,      # False = video mode (faster)
            max_num_hands=1,              # Only track dominant hand
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
```

### 21 Hand Landmarks Reference
```
Wrist:          0
Thumb:          1(CMC) 2(MCP) 3(IP)  4(TIP)
Index finger:   5(MCP) 6(PIP) 7(DIP) 8(TIP)
Middle finger:  9(MCP) 10(PIP) 11(DIP) 12(TIP)
Ring finger:    13(MCP) 14(PIP) 15(DIP) 16(TIP)
Pinky:          17(MCP) 18(PIP) 19(DIP) 20(TIP)
```

---

## Landmark Extraction

### Extract and Normalize Landmarks
```python
def extract(self, frame: np.ndarray) -> np.ndarray | None:
    """
    Extract and normalize 21 hand landmarks from a frame.
    Returns array of shape (63,) or None if no hand detected.
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

    # Scale by wrist-to-middle-fingertip distance
    middle_tip = landmarks[12]
    scale = np.linalg.norm(middle_tip)
    if scale > 0:
        landmarks /= scale

    return landmarks.flatten()  # shape: (63,)
```

---

## Drawing Hand Skeleton on Frames

### Draw Landmarks and Connections
```python
def draw_landmarks(self, frame: np.ndarray,
                   results) -> np.ndarray:
    """Draw hand skeleton on frame. Returns annotated frame."""
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            self.mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_draw.DrawingSpec(
                    color=(0, 255, 0),   # Green dots
                    thickness=2,
                    circle_radius=3
                ),
                self.mp_draw.DrawingSpec(
                    color=(255, 255, 255),  # White lines
                    thickness=2
                )
            )
    return frame
```

### Draw Prediction Text on Frame
```python
def draw_prediction(self, frame: np.ndarray,
                    word: str, confidence: float) -> np.ndarray:
    h, w = frame.shape[:2]
    # Background rectangle for text
    cv2.rectangle(frame, (0, h-60), (w, h), (0, 0, 0), -1)
    # Word text
    cv2.putText(frame, word.upper(),
                (10, h-30), cv2.FONT_HERSHEY_SIMPLEX,
                1.2, (0, 255, 100), 2)
    # Confidence text
    cv2.putText(frame, f"{confidence*100:.0f}%",
                (w-80, h-30), cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (200, 200, 200), 2)
    return frame
```

---

## Frame Processing for Training

### Extract Exactly 30 Frames from Video
```python
def extract_frames(video_path: str, target_frames: int = 30) -> list:
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames == 0:
        cap.release()
        return []

    # Calculate evenly spaced frame indices
    indices = np.linspace(0, total_frames - 1,
                          target_frames, dtype=int)
    frames = []

    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            frames.append(frame)
        else:
            # Pad with last good frame if read fails
            if frames:
                frames.append(frames[-1])

    cap.release()

    # Pad if still short
    while len(frames) < target_frames:
        frames.append(frames[-1] if frames else np.zeros((480, 640, 3), dtype=np.uint8))

    return frames[:target_frames]
```

---

## Real-Time Webcam in Streamlit (streamlit-webrtc)

### VideoProcessor Class Pattern
```python
from streamlit_webrtc import VideoTransformerBase
import av

class ASLVideoProcessor(VideoTransformerBase):
    def __init__(self):
        self.extractor = LandmarkExtractor()
        self.inference = InferenceEngine()

    def transform(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")

        # Extract landmarks
        landmarks = self.extractor.extract(img)

        if landmarks is not None:
            # Add to rolling buffer and run inference
            word, confidence = self.inference.update(landmarks)
            if word:
                img = self.extractor.draw_prediction(img, word, confidence)

        # Draw skeleton
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.extractor.hands.process(rgb)
        img = self.extractor.draw_landmarks(img, results)

        return av.VideoFrame.from_ndarray(img, format="bgr24")
```

---

## Common Issues and Fixes

| Problem | Cause | Fix |
|---------|-------|-----|
| No hand detected | Wrong color space | Convert BGR→RGB before MediaPipe |
| Jittery landmarks | `static_image_mode=True` | Set to `False` for video |
| Landmarks off-screen | No normalization | Always normalize relative to wrist |
| Slow FPS in Streamlit | Heavy processing per frame | Keep transform() lightweight |
| Two hands confusing model | `max_num_hands=2` | Set to `1`, use dominant hand only |
| Black frame in WebRTC | Wrong av format | Use `format="bgr24"` |

---

## Do Not
- Process raw pixels as model input — use landmarks only
- Skip BGR→RGB conversion before MediaPipe
- Use `static_image_mode=True` for live webcam (it's slower)
- Forget to release `cap` after OpenCV video reading
- Draw on the original frame before extracting landmarks
