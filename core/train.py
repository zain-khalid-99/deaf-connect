import numpy as np
import os
import json
import tensorflow as tf
from tensorflow.keras.callbacks import (
    EarlyStopping, 
    ReduceLROnPlateau, 
    ModelCheckpoint, 
    CSVLogger
)
from sklearn.utils import class_weight
from model import build_asl_model

# Constants
EPOCHS = 150
BATCH_SIZE = 32
MODEL_PATH = 'models/asl_model.keras'
BEST_MODEL_PATH = 'models/best_model.keras'
LOG_PATH = 'models/training_history.json'
CSV_LOG_PATH = 'models/training_log.csv'

def augment_landmarks(X):
    """
    Professional Data Augmentation for Landmark Sequences.
    Applied only to training data.
    """
    augmented_X = X.copy()
    
    # 1. Scaling (Size variation)
    scale = np.random.uniform(0.9, 1.1)
    augmented_X = augmented_X * scale
    
    # 2. Translation (Position variation)
    translation = np.random.uniform(-0.05, 0.05, size=(3,))
    augmented_X = augmented_X + translation
    
    # 3. Gaussian Noise (Sensor noise simulation)
    noise = np.random.normal(0, 0.002, augmented_X.shape)
    augmented_X = augmented_X + noise
    
    # 4. Rotation (Hand tilt simulation)
    # Simple z-axis rotation for 3D landmarks
    theta = np.random.uniform(-0.1, 0.1)
    c, s = np.cos(theta), np.sin(theta)
    rotation_matrix = np.array([
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1]
    ])
    # Reshape for matrix multiplication
    orig_shape = augmented_X.shape
    augmented_X = augmented_X.reshape(-1, 3) @ rotation_matrix
    augmented_X = augmented_X.reshape(orig_shape)
    
    return augmented_X

def load_data(data_dir='dataset/processed'):
    """Loads processed datasets from NumPy files"""
    X_train = np.load(os.path.join(data_dir, 'X_train.npy'))
    y_train = np.load(os.path.join(data_dir, 'y_train.npy'))
    X_val = np.load(os.path.join(data_dir, 'X_val.npy'))
    y_val = np.load(os.path.join(data_dir, 'y_val.npy'))
    
    return X_train, y_train, X_val, y_val

def train():
    """Main training pipeline with augmentation and class weights"""
    if not os.path.exists('models'):
        os.makedirs('models')
        
    print("--- [PHASE 1] Loading Datasets ---")
    X_train, y_train, X_val, y_val = load_data()
    
    with open('dataset/labels.json', 'r') as f:
        labels_map = json.load(f)
    num_classes = len(labels_map)
    
    print(f"Num Classes: {num_classes}")
    print(f"Original Train Shape: {X_train.shape}")
    
    # Apply Augmentation to Training Data
    print("--- [PHASE 2] Applying Data Augmentation ---")
    X_train_aug = augment_landmarks(X_train)
    X_train = np.concatenate([X_train, X_train_aug], axis=0)
    y_train = np.concatenate([y_train, y_train], axis=0)
    print(f"Augmented Train Shape: {X_train.shape}")
    
    # Compute Class Weights
    print("--- [PHASE 3] Computing Class Weights ---")
    weights = class_weight.compute_class_weight(
        'balanced',
        classes=np.unique(y_train),
        y=y_train
    )
    class_weights = dict(enumerate(weights))
    
    print("--- [PHASE 4] Building Model ---")
    model = build_asl_model((30, 63), num_classes)
    
    # Callbacks
    callbacks = [
        EarlyStopping(monitor='val_accuracy', patience=25, restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=15, min_lr=0.00001, verbose=1),
        ModelCheckpoint(BEST_MODEL_PATH, monitor='val_accuracy', save_best_only=True, verbose=1),
        CSVLogger(CSV_LOG_PATH)
    ]
    
    print("--- [PHASE 5] Starting Training ---")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        class_weight=class_weights,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save final artifacts
    model.save(MODEL_PATH)
    with open(LOG_PATH, 'w') as f:
        json.dump(history.history, f)
    
    print(f"--- [OK] Training Complete. Best model saved at {BEST_MODEL_PATH} ---")

if __name__ == "__main__":
    train()
