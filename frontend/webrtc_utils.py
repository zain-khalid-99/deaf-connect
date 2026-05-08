import threading
from typing import List, Optional
import av
import numpy as np
from streamlit_webrtc import VideoProcessorBase
from core.landmark_extractor import LandmarkExtractor

class SignLanguageProcessor(VideoProcessorBase):
    def __init__(self, model=None, labels=None):
        self.extractor = LandmarkExtractor()
        self.model = model
        self.labels = labels
        self.sequence_buffer = []
        self.last_prediction = ""
        self.confidence = 0.0
        
        # Thread safety
        self.result_lock = threading.Lock()
        self.predicted_word = None
        self.prediction_confidence = 0.0

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        
        # 1. Extract landmarks
        landmarks = self.extractor.extract(img)
        
        if landmarks is not None:
            # 2. Add to buffer
            self.sequence_buffer.append(landmarks)
            
            # Keep buffer size at 30 (Sequence Length)
            if len(self.sequence_buffer) > 30:
                self.sequence_buffer.pop(0)
            
            # 3. Perform Inference if buffer is full
            if len(self.sequence_buffer) == 30 and self.model:
                input_data = np.expand_dims(self.sequence_buffer, axis=0)
                prediction = self.model.predict(input_data, verbose=0)
                
                idx = np.argmax(prediction[0])
                confidence = prediction[0][idx]
                
                if confidence > 0.7: # Confidence threshold
                    word = self.labels.get(str(idx), "Unknown")
                    
                    with self.result_lock:
                        self.predicted_word = word
                        self.prediction_confidence = float(confidence)
            
            # 4. Optional: Draw landmarks on the frame
            # (MediaPipe process is already done in extract, but we might need to process again to draw)
            # For performance, we can skip drawing or optimize it.
            
        return av.VideoFrame.from_ndarray(img, format="bgr24")

    def get_results(self):
        with self.result_lock:
            return self.predicted_word, self.prediction_confidence
