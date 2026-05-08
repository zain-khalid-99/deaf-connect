import numpy as np
import os
import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf
import time

def evaluate_model(model_path='models/best_model.keras', data_dir='dataset/processed', output_dir='evaluation'):
    """Complete evaluation pipeline for ASL model"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Load labels
    with open('dataset/labels.json', 'r') as f:
        labels_map = json.load(f)
    actions = list(labels_map.keys())
    
    # Load model and test dataset
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at {model_path}")
        return

    model = tf.keras.models.load_model(model_path)
    X_test = np.load(os.path.join(data_dir, 'X_test.npy'))
    y_test = np.load(os.path.join(data_dir, 'y_test.npy'))
    
    print(f"Running evaluation on {len(X_test)} samples...")
    
    # 1. Inference Speed Test
    start_time = time.time()
    y_pred_prob = model.predict(X_test, verbose=0)
    total_time = time.time() - start_time
    avg_speed = (total_time / len(X_test)) * 1000
    y_pred = np.argmax(y_pred_prob, axis=1)
    
    # 2. Classification Report
    report = classification_report(y_test, y_pred, target_names=actions, output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    report_df.to_csv(os.path.join(output_dir, 'classification_report.csv'))
    
    # 3. Per-Class Accuracy
    cm = confusion_matrix(y_test, y_pred)
    per_class_acc = cm.diagonal() / cm.sum(axis=1)
    per_class_df = pd.DataFrame({'Action': actions, 'Accuracy': per_class_acc})
    per_class_df.to_csv(os.path.join(output_dir, 'per_class_accuracy.csv'), index=False)
    
    # 4. Confusion Matrix Visualization
    plt.figure(figsize=(16, 14))
    sns.heatmap(cm, annot=True, fmt='d', xticklabels=actions, yticklabels=actions, cmap='YlGnBu')
    plt.title('Professional ASL Recognition Confusion Matrix')
    plt.xlabel('Predicted Label')
    plt.ylabel('Ground Truth Label')
    plt.savefig(os.path.join(output_dir, 'confusion_matrix.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Top-5 Confused Pairs
    flat_cm = cm.copy()
    np.fill_diagonal(flat_cm, 0)
    top_indices = np.unravel_index(np.argsort(flat_cm, axis=None)[-5:], flat_cm.shape)
    
    with open(os.path.join(output_dir, 'top_confused_pairs.txt'), 'w') as f:
        f.write("Top 5 Confused Sign Pairs:\n")
        f.write("-" * 30 + "\n")
        for i in range(4, -1, -1):
            actual = actions[top_indices[0][i]]
            pred = actions[top_indices[1][i]]
            count = flat_cm[top_indices[0][i], top_indices[1][i]]
            f.write(f"{actual} -> {pred}: {count} occurrences\n")
            
    # 6. Training History Analysis
    history_path = 'models/training_history.json'
    if os.path.exists(history_path):
        with open(history_path, 'r') as h:
            history = json.load(h)
        
        # Accuracy Curve
        plt.figure(figsize=(10, 6))
        plt.plot(history['accuracy'], label='Train', linewidth=2)
        plt.plot(history['val_accuracy'], label='Val', linewidth=2)
        plt.title('Model Accuracy History')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(loc='lower right')
        plt.grid(True, alpha=0.3)
        plt.savefig(os.path.join(output_dir, 'accuracy_curve.png'))
        plt.close()

        # Loss Curve
        plt.figure(figsize=(10, 6))
        plt.plot(history['loss'], label='Train', linewidth=2)
        plt.plot(history['val_loss'], label='Val', linewidth=2)
        plt.title('Model Loss History')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(loc='upper right')
        plt.grid(True, alpha=0.3)
        plt.savefig(os.path.join(output_dir, 'loss_curve.png'))
        plt.close()

    print(f"--- [OK] Evaluation artifacts created in {output_dir}/ ---")
    print(f"Avg Inference Speed: {avg_speed:.2f}ms")

if __name__ == "__main__":
    evaluate_model()
