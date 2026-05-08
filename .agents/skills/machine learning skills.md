# Machine Learning Skill — ASL Recognition Project

## Purpose
This skill covers all ML decisions, patterns, and best practices for building, training, and evaluating the LSTM model for ASL word recognition.

## When to Apply
- Writing `core/model.py`, `core/train.py`, `core/evaluate.py`
- Making decisions about architecture, hyperparameters, or training strategy
- Interpreting training results or improving accuracy

---

## Model Architecture

### Why LSTM?
ASL signs are **temporal sequences** — the same hand shape held or moved differently means different words. LSTM captures time dependencies across the 30-frame sequence. A static CNN cannot do this.

### Input Shape
```
(batch_size, 30, 63)
 └── 30 frames
      └── 63 values = 21 landmarks × 3 (x, y, z)
```

### Full Architecture (model.py)
```python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.regularizers import l2

def build_model(num_classes: int = 50) -> Sequential:
    model = Sequential([
        LSTM(128, return_sequences=True, input_shape=(30, 63),
             kernel_regularizer=l2(0.001)),
        Dropout(0.4),

        LSTM(128, return_sequences=True,
             kernel_regularizer=l2(0.001)),
        Dropout(0.4),

        LSTM(64, return_sequences=False),
        Dropout(0.3),

        Dense(128, activation='relu', kernel_regularizer=l2(0.001)),
        BatchNormalization(),
        Dropout(0.3),

        Dense(64, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy', 'top_k_categorical_accuracy']
    )
    return model
```

---

## Training Configuration

### Callbacks (always use all of these)
```python
from tensorflow.keras.callbacks import (
    EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
)

callbacks = [
    EarlyStopping(
        monitor='val_accuracy',
        patience=20,
        restore_best_weights=True
    ),
    ModelCheckpoint(
        filepath='models/asl_model.h5',
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    ),
    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=10,
        min_lr=1e-6
    )
]
```

### Training Call
```python
history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=200,
    batch_size=32,
    callbacks=callbacks,
    class_weight=class_weights  # handle imbalanced classes
)
```

### Class Weights (handle imbalanced dataset)
```python
from sklearn.utils.class_weight import compute_class_weight
import numpy as np

class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(y_train_int),
    y=y_train_int
)
class_weight_dict = dict(enumerate(class_weights))
```

---

## Data Augmentation for Landmarks

Apply during preprocessing to triple effective dataset size:

```python
def augment_landmarks(sequence: np.ndarray) -> np.ndarray:
    """Apply random augmentation to a (30, 63) sequence."""
    # Random rotation (reshape to (30, 21, 3) for 3D rotation)
    seq = sequence.reshape(30, 21, 3)
    angle = np.random.uniform(-15, 15) * np.pi / 180
    rotation_matrix = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle),  np.cos(angle), 0],
        [0, 0, 1]
    ])
    seq = seq @ rotation_matrix.T

    # Random translation (small shift)
    shift = np.random.uniform(-0.05, 0.05, (1, 1, 3))
    seq = seq + shift

    return seq.reshape(30, 63)
```

---

## Expected Results

| Metric | Expected Range |
|--------|---------------|
| Training Accuracy | 93–97% |
| Validation Accuracy | 86–92% |
| Test Accuracy | 84–90% |
| Inference Speed | 15–40ms per prediction |
| Training Time (CPU) | 3–5 hours |
| Training Time (GPU) | 30–60 minutes |

---

## Evaluation (evaluate.py)

### Accuracy and Loss Curves
```python
import matplotlib.pyplot as plt

def plot_training_history(history):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.plot(history.history['accuracy'], label='Train')
    ax1.plot(history.history['val_accuracy'], label='Validation')
    ax1.set_title('Model Accuracy')
    ax1.legend()

    ax2.plot(history.history['loss'], label='Train')
    ax2.plot(history.history['val_loss'], label='Validation')
    ax2.set_title('Model Loss')
    ax2.legend()

    plt.savefig('evaluation/accuracy_loss_curves.png', dpi=150)
```

### Confusion Matrix
```python
from sklearn.metrics import confusion_matrix
import seaborn as sns

def plot_confusion_matrix(y_true, y_pred, labels):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(20, 18))
    sns.heatmap(cm, annot=True, fmt='d',
                xticklabels=labels, yticklabels=labels,
                cmap='Blues')
    plt.title('Confusion Matrix — 50 ASL Words')
    plt.savefig('evaluation/confusion_matrix.png', dpi=150, bbox_inches='tight')
```

### Classification Report
```python
from sklearn.metrics import classification_report
import pandas as pd

report = classification_report(y_true, y_pred,
                                target_names=word_labels,
                                output_dict=True)
df = pd.DataFrame(report).transpose()
df.to_csv('evaluation/classification_report.csv')
```

---

## Common Issues and Fixes

| Problem | Cause | Fix |
|---------|-------|-----|
| Validation accuracy stuck at ~2% | Labels not one-hot encoded | Apply `to_categorical()` |
| Model overfits after 20 epochs | Too few dropout layers | Increase dropout to 0.5 |
| Loss is NaN | Learning rate too high | Set lr to 0.0001 |
| All predictions same class | Class imbalance | Apply class weights |
| Slow training | No GPU / large batch | Reduce batch to 16 or use Colab |

---

## Do Not
- Train without early stopping — model will overfit
- Skip normalization of landmarks — position variance kills accuracy
- Use raw pixel frames as input — use landmarks only
- Train on all 2000 WLASL words — start with 50, accuracy will be much better
