"""
MobileNet Feature Extractor - Edge AI Processing
"""
import tensorflow as tf
import numpy as np
import cv2

class MobileNetFeatureExtractor:
    def __init__(self):
        print("📥 Loading MobileNetV2...")
        self.mobilenet = tf.keras.applications.MobileNetV2(weights='imagenet')
        self.extractor = tf.keras.Model(
            inputs=self.mobilenet.input,
            outputs=self.mobilenet.get_layer('global_average_pooling2d').output
        )
        self.threat_keywords = ['knife', 'gun', 'weapon', 'scissors', 'hammer']
        print("✅ MobileNet ready (1280 features per frame)")
    
    def extract_features(self, frame):
        """استخراج الميزات للـ LSTM"""
        img = cv2.resize(frame, (224, 224))
        img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
        img = np.expand_dims(img, axis=0)
        features = self.extractor.predict(img, verbose=0)[0]
        return features
    
    def detect_threats(self, frame):
        """كشف التهديدات المباشرة"""
        img = cv2.resize(frame, (224, 224))
        img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
        img = np.expand_dims(img, axis=0)
        
        preds = self.mobilenet.predict(img, verbose=0)
        decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=3)[0]
        
        threats = []
        for _, label, conf in decoded:
            if any(word in label.lower() for word in self.threat_keywords):
                threats.append((label, float(conf)))
        return threats