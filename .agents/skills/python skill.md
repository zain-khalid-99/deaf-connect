# Python Skill — ASL Recognition Project

## Purpose
This skill guides best practices for writing clean, efficient Python code across all modules in the ASL sign language recognition system.

## When to Apply
- Writing any `.py` file in the project
- Reviewing or refactoring existing Python code
- Debugging Python errors or exceptions

---

## Project-Specific Python Standards

### File Header Template
Every Python file must start with:
```python
"""
Module: <module_name>.py
Purpose: <one line description>
Author: <team member name>
Date: <date>
"""
```

### Import Order (always follow this)
```python
# 1. Standard library
import os
import json
import time
from collections import deque

# 2. Third-party libraries
import numpy as np
import cv2
import mediapipe as mp
import tensorflow as tf

# 3. Local imports
from core.inference import InferenceEngine
from utils.config import Config
```

### Class Structure Pattern
All core classes follow this pattern:
```python
class ClassName:
    def __init__(self, config: Config):
        self.config = config
        self._initialize()

    def _initialize(self):
        """Private setup method."""
        pass

    def process(self, input_data):
        """Main public method."""
        pass

    def _helper(self):
        """Private helper method."""
        pass
```

### Error Handling
Always wrap external calls (MediaPipe, TensorFlow, OpenCV) in try/except:
```python
try:
    results = self.hands.process(frame)
except Exception as e:
    print(f"[ERROR] MediaPipe processing failed: {e}")
    return None
```

### Type Hints
Always use type hints on function signatures:
```python
def extract_landmarks(self, frame: np.ndarray) -> np.ndarray | None:
```

### Constants
Never hardcode values. Always reference `utils/config.py`:
```python
# BAD
if confidence > 0.72:

# GOOD
if confidence > self.config.CONFIDENCE_THRESHOLD:
```

---

## Common Patterns Used in This Project

### Rolling Buffer with Deque
```python
from collections import deque
self.buffer = deque(maxlen=30)  # auto-drops oldest frame
self.buffer.append(new_landmarks)
if len(self.buffer) == 30:
    self.run_prediction()
```

### Loading JSON Labels
```python
with open(self.config.LABELS_PATH, 'r') as f:
    self.labels = json.load(f)
# labels = {"0": "hello", "1": "thank you", ...}
```

### Saving/Loading NumPy Arrays
```python
# Save
np.save('dataset/processed/X_train.npy', X_train)

# Load
X_train = np.load('dataset/processed/X_train.npy')
```

### Timing and Cooldown
```python
self.last_prediction_time = 0

def _is_cooldown_active(self) -> bool:
    return (time.time() - self.last_prediction_time) < self.config.COOLDOWN_TIME
```

---

## File-by-File Responsibilities

| File | Responsibility |
|------|---------------|
| `utils/config.py` | All constants and paths |
| `core/landmark_extractor.py` | MediaPipe wrapper only |
| `core/inference.py` | Model prediction only |
| `core/sentence_builder.py` | Word → sentence logic only |
| `core/train.py` | Training loop only |
| `core/preprocess.py` | Data pipeline only |
| `core/evaluate.py` | Metrics and charts only |

Each file does ONE thing. Never mix concerns.

---

## Debugging Tips

### Check NumPy Array Shapes
```python
print(f"X_train shape: {X_train.shape}")  # Expected: (N, 30, 63)
print(f"y_train shape: {y_train.shape}")  # Expected: (N, 50)
```

### Check Model Input/Output
```python
model.summary()
test_input = np.zeros((1, 30, 63))
output = model.predict(test_input)
print(f"Output shape: {output.shape}")  # Expected: (1, 50)
```

### Verify MediaPipe Detection
```python
if results.multi_hand_landmarks is None:
    print("[DEBUG] No hand detected in frame")
```

---

## Do Not
- Use global variables
- Hardcode file paths
- Skip type hints on public methods
- Mix training and inference logic in the same file
- Use `print()` for production logging — use Python `logging` module
