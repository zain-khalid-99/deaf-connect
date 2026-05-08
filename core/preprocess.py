import os
import cv2
import numpy as np
import json
import logging
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from landmark_extractor import LandmarkExtractor
from utils.config import (
    DATASET_RAW_DIR, 
    DATASET_PROCESSED_DIR, 
    LABELS_JSON_PATH,
    SEQUENCE_LENGTH,
    LANDMARK_DIMENSIONS,
    VIDEO_EXTENSIONS,
    TRAIN_SPLIT,
    VAL_SPLIT,
    TEST_SPLIT
)

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("preprocessing.log"),
        logging.StreamHandler()
    ]
)

class ASLPreprocessor:
    def __init__(self):
        self.extractor = LandmarkExtractor()
        self.labels = {}
        self.skipped_videos = 0
        self.processed_samples = 0

    def get_labels(self):
        """Discovers labels from the raw dataset directory."""
        if not os.path.exists(DATASET_RAW_DIR):
            logging.error(f"Raw dataset directory not found: {DATASET_RAW_DIR}")
            return {}
        
        actions = sorted([d for d in os.listdir(DATASET_RAW_DIR) if os.path.isdir(os.path.join(DATASET_RAW_DIR, d))])
        self.labels = {action: i for i, action in enumerate(actions)}
        
        # Save labels for future reference
        with open(LABELS_JSON_PATH, 'w') as f:
            json.dump(self.labels, f, indent=4)
        
        logging.info(f"Discovered {len(actions)} classes: {actions}")
        return self.labels

    def process_video(self, video_path):
        """Processes a single video into a (30, 63) sequence."""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return None

        frames_landmarks = []
        last_valid_landmarks = np.zeros(LANDMARK_DIMENSIONS) # Fallback if first frame fails

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            landmarks = self.extractor.extract(frame)
            if landmarks is not None:
                frames_landmarks.append(landmarks)
                last_valid_landmarks = landmarks
            elif len(frames_landmarks) > 0:
                # Use previous frame's landmarks for continuity
                frames_landmarks.append(last_valid_landmarks)
            else:
                # If first frame fails, use zeros for now
                frames_landmarks.append(last_valid_landmarks)
        
        cap.release()

        # Frame Standardization (Temporal Resampling)
        total_frames = len(frames_landmarks)
        if total_frames == 0:
            return None

        if total_frames >= SEQUENCE_LENGTH:
            # Evenly sample 30 frames
            indices = np.linspace(0, total_frames - 1, SEQUENCE_LENGTH, dtype=int)
            standardized = [frames_landmarks[i] for i in indices]
        else:
            # Repeat last frame (Padding)
            standardized = list(frames_landmarks)
            last_valid = frames_landmarks[-1]
            while len(standardized) < SEQUENCE_LENGTH:
                standardized.append(last_valid)

        return np.array(standardized, dtype=np.float32)

    def run(self):
        """Executes the full pipeline."""
        if not self.labels:
            self.get_labels()

        X = []
        y = []

        logging.info("Starting professional preprocessing pipeline...")

        for action, label_idx in self.labels.items():
            action_path = os.path.join(DATASET_RAW_DIR, action)
            videos = [f for f in os.listdir(action_path) if f.endswith(VIDEO_EXTENSIONS)]
            
            logging.info(f"Processing '{action}' ({len(videos)} sources)")
            
            for video_name in tqdm(videos, desc=f"Analyzing {action}"):
                video_path = os.path.join(action_path, video_name)
                try:
                    sequence = self.process_video(video_path)
                    if sequence is not None:
                        X.append(sequence)
                        y.append(label_idx)
                        self.processed_samples += 1
                    else:
                        self.skipped_videos += 1
                        logging.warning(f"Skipped corrupted/empty video: {video_path}")
                except Exception as e:
                    self.skipped_videos += 1
                    logging.error(f"Fatal error processing {video_path}: {e}")

        # Final conversion to NumPy
        X = np.array(X)
        y = np.array(y)

        if len(X) == 0:
            logging.error("No data processed. Check dataset/raw directory.")
            return

        # Split: 80/10/10 Stratified
        logging.info("Splitting dataset (80/10/10 stratified)...")
        
        # First split off train
        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y, test_size=(VAL_SPLIT + TEST_SPLIT), stratify=y, random_state=42
        )
        
        # Split temp into val and test
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
        )

        # Save processed data
        if not os.path.exists(DATASET_PROCESSED_DIR):
            os.makedirs(DATASET_PROCESSED_DIR)

        np.save(os.path.join(DATASET_PROCESSED_DIR, 'X_train.npy'), X_train)
        np.save(os.path.join(DATASET_PROCESSED_DIR, 'X_val.npy'), X_val)
        np.save(os.path.join(DATASET_PROCESSED_DIR, 'X_test.npy'), X_test)
        np.save(os.path.join(DATASET_PROCESSED_DIR, 'y_train.npy'), y_train)
        np.save(os.path.join(DATASET_PROCESSED_DIR, 'y_val.npy'), y_val)
        np.save(os.path.join(DATASET_PROCESSED_DIR, 'y_test.npy'), y_test)

        logging.info(f"--- Pipeline Finished ---")
        logging.info(f"Processed Samples: {self.processed_samples}")
        logging.info(f"Skipped Videos: {self.skipped_videos}")
        logging.info(f"Train samples: {len(X_train)}")
        logging.info(f"Val samples: {len(X_val)}")
        logging.info(f"Test samples: {len(X_test)}")

if __name__ == "__main__":
    preprocessor = ASLPreprocessor()
    preprocessor.run()
