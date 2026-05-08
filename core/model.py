import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization, Input

def build_asl_model(input_shape, num_classes):
    """
    Professional Stacked LSTM Classifier for ASL Sequence Recognition.
    Optimized for landmark-based sequence classification.
    """
    model = Sequential([
        Input(shape=input_shape),
        
        # Layer 1: LSTM with 128 units
        LSTM(128, return_sequences=True),
        Dropout(0.3),
        
        # Layer 2: LSTM with 128 units
        LSTM(128, return_sequences=True),
        Dropout(0.3),
        
        # Layer 3: LSTM with 64 units
        LSTM(64),
        Dropout(0.3),
        
        # Layer 4: Dense 128
        Dense(128, activation='relu'),
        BatchNormalization(),
        
        # Layer 5: Dense 64
        Dense(64, activation='relu'),
        
        # Output Layer: Softmax for multi-class classification
        Dense(num_classes, activation='softmax')
    ])
    
    # Using Adam optimizer with default parameters
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
    
    model.compile(
        optimizer=optimizer,
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy', tf.keras.metrics.SparseTopKCategoricalAccuracy(k=5, name='top_5_accuracy')]
    )
    
    return model

if __name__ == "__main__":
    # Internal test of architecture
    model = build_asl_model((30, 63), 20)
    model.summary()
