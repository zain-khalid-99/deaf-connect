# AI Training & Preprocessing Constants

# Dataset Structure
DATASET_RAW_DIR = 'dataset/raw'
DATASET_PROCESSED_DIR = 'dataset/processed'
LABELS_JSON_PATH = 'dataset/labels.json'

# Preprocessing Parameters
SEQUENCE_LENGTH = 30
LANDMARK_DIMENSIONS = 63  # 21 landmarks * 3 (x, y, z)
MAX_HANDS = 1

# Video Processing
VIDEO_EXTENSIONS = ('.mp4', '.avi', '.mov', '.mkv')
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Machine Learning Split
TRAIN_SPLIT = 0.8
VAL_SPLIT = 0.1
TEST_SPLIT = 0.1

# Normalization Settings
MIN_HAND_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5
