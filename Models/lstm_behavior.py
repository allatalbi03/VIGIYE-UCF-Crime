"""
LSTM Behavior Analysis Module
Violence detection through sequence analysis
"""

import numpy as np
import tensorflow as tf
from datetime import datetime

class LSTMBehaviorAnalyzer:
    def __init__(self, sequence_length=30, feature_dim=1280):
        """
        LSTM for behavior analysis
        Args:
            sequence_length: عدد الإطارات في التسلسل (30 = 3 ثواني)
            feature_dim: أبعاد الميزات (1280 من MobileNet)
        """
        self.sequence_length = sequence_length
        self.feature_dim = feature_dim
        self.feature_sequence = []
        self.behavior_history = []
        
        # إنشاء نموذج LSTM
        self.model = self._create_model()
        print(f"✅ LSTM Behavior Analyzer ready (seq_len={sequence_length})")
    
    def _create_model(self):
        """إنشاء نموذج LSTM لتحليل السلوك"""
        model = tf.keras.Sequential([
            # LSTM layers لتحليل التسلسل الزمني
            tf.keras.layers.LSTM(128, return_sequences=True, 
                                input_shape=(self.sequence_length, self.feature_dim)),
            tf.keras.layers.Dropout(0.3),
            
            tf.keras.layers.LSTM(64, return_sequences=True),
            tf.keras.layers.Dropout(0.3),
            
            tf.keras.layers.LSTM(32),
            tf.keras.layers.Dropout(0.3),
            
            # Dense layers للتصنيف
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')  # 0=عادي, 1=عنف
        ])
        
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def add_features(self, features):
        """إضافة ميزات جديدة للتسلسل"""
        self.feature_sequence.append(features)
        
        # الحفاظ على طول التسلسل
        if len(self.feature_sequence) > self.sequence_length:
            self.feature_sequence.pop(0)
    
    def analyze(self, features=None):
        """
        تحليل السلوك الحالي
        Returns: score من 0 إلى 1 (أعلى = عنف)
        """
        if features is not None:
            self.add_features(features)
        
        # نحتاج على الأقل sequence_length إطار للتحليل
        if len(self.feature_sequence) < self.sequence_length:
            return 0.0
        
        # تجهيز التسلسل للتحليل
        sequence = np.array([self.feature_sequence])
        
        # توقع السلوك
        try:
            score = self.model.predict(sequence, verbose=0)[0][0]
        except:
            # لو النموذج مش مدرب، نستخدم حركة بسيطة
            score = self._calculate_motion_score()
        
        # حفظ في التاريخ
        self.behavior_history.append({
            'timestamp': datetime.now().isoformat(),
            'score': float(score)
        })
        
        return float(score)
    
    def _calculate_motion_score(self):
        """حساب مؤشر الحركة (بديل مؤقت)"""
        if len(self.feature_sequence) < 2:
            return 0.0
        
        # حساب الفرق بين الإطارات
        diffs = []
        for i in range(1, len(self.feature_sequence)):
            diff = np.mean(np.abs(self.feature_sequence[i] - self.feature_sequence[i-1]))
            diffs.append(diff)
        
        avg_motion = np.mean(diffs) if diffs else 0
        # تطبيع إلى 0-1
        return min(1.0, avg_motion / 1000)
    
    def get_status(self, score):
        """تحويل النتيجة إلى حالة مفهومة"""
        if score > 0.7:
            return "🔴 VIOLENT", (0, 0, 255)
        elif score > 0.4:
            return "🟡 SUSPICIOUS", (0, 255, 255)
        else:
            return "🟢 NORMAL", (0, 255, 0)
    
    def reset_sequence(self):
        """إعادة تعيين التسلسل"""
        self.feature_sequence = []
    
    def get_statistics(self):
        """إحصائيات التحليل"""
        if not self.behavior_history:
            return {
                'average_score': 0,
                'max_score': 0,
                'violent_events': 0
            }
        
        scores = [h['score'] for h in self.behavior_history]
        return {
            'average_score': float(np.mean(scores)),
            'max_score': float(np.max(scores)),
            'violent_events': sum(1 for s in scores if s > 0.7)
        }