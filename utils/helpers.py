import os
import numpy as np
import json
import logging
from utils.config import DATASET_PROCESSED_DIR, LABELS_JSON_PATH

def get_dataset_stats():
    """Returns basic statistics about the processed dataset."""
    stats = {
        "status": "Incomplete",
        "total_samples": 0,
        "classes": 0,
        "splits": {"train": 0, "val": 0, "test": 0}
    }
    
    if not os.path.exists(DATASET_PROCESSED_DIR):
        return stats

    try:
        X_train = np.load(os.path.join(DATASET_PROCESSED_DIR, 'X_train.npy'), mmap_mode='r')
        X_val = np.load(os.path.join(DATASET_PROCESSED_DIR, 'X_val.npy'), mmap_mode='r')
        X_test = np.load(os.path.join(DATASET_PROCESSED_DIR, 'X_test.npy'), mmap_mode='r')
        
        stats["splits"]["train"] = len(X_train)
        stats["splits"]["val"] = len(X_val)
        stats["splits"]["test"] = len(X_test)
        stats["total_samples"] = len(X_train) + len(X_val) + len(X_test)
        stats["status"] = "Healthy" if stats["total_samples"] > 0 else "Empty"
    except Exception as e:
        stats["status"] = "Error"
        logging.error(f"Error reading dataset stats: {e}")

    if os.path.exists(LABELS_JSON_PATH):
        with open(LABELS_JSON_PATH, 'r') as f:
            labels = json.load(f)
            stats["classes"] = len(labels)

    return stats

def clean_processed_data():
    """Removes all processed datasets."""
    if os.path.exists(DATASET_PROCESSED_DIR):
        for f in os.listdir(DATASET_PROCESSED_DIR):
            os.remove(os.path.join(DATASET_PROCESSED_DIR, f))
        logging.info("Processed data cleaned.")
