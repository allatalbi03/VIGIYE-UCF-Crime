"""
Configuration File - VIGIYE System Settings
"""

import os
import json

class Config:
    """VIGIYE System Configuration"""
    
    # ===== System Info =====
    PROJECT_NAME = "VIGIYE"
    TEAM_NAME = "ESURGE"
    UNIVERSITY = "University of El-Oued, Algeria"
    COMPETITION = "Huawei ICT Competition 2025-2026"
    
    # ===== Edge Layer =====
    CAMERA_ID = 0  # 0 = laptop camera, 1 = external USB
    FRAME_WIDTH = 640
    FRAME_HEIGHT = 480
    FPS = 30
    
    # Atlas 200 Simulation
    ATLAS_TEMP_NORMAL = 45
    ATLAS_POWER_NORMAL = 5
    ATLAS_CPU_THRESHOLD = 80
    
    # ===== AI Models =====
    # MobileNet
    INPUT_SIZE = 224
    FEATURE_DIM = 1280
    THREAT_KEYWORDS = ['knife', 'gun', 'weapon', 'scissors', 'hammer', 
                       'axe', 'dagger', 'sword', 'pistol', 'rifle']
    
    # LSTM
    SEQUENCE_LENGTH = 30  # 3 seconds at 10 fps
    BEHAVIOR_THRESHOLD = {
        'NORMAL': 0.4,
        'SUSPICIOUS': 0.7,
        'VIOLENT': 1.0
    }
    
    # ===== Privacy & Encryption =====
    SECRET_KEY = "VIGIYE_SECURE_KEY_2026_ESURGE"
    ENCRYPTION_ALGO = "AES-256"
    PRIVACY_MODE = True  # No raw video leaves device
    
    # ===== Federated Learning =====
    DEVICE_ID = "VIGIYE_EDGE_001"
    REGION = "middle-east-1"  # Huawei Cloud MENA region
    UPDATE_INTERVAL = 100  # frames between updates
    MIN_CLIENTS_FOR_AGGREGATION = 3
    
    # OBS Storage
    OBS_BUCKET = "vigiye-model-weights"
    OBS_ENDPOINT = f"https://obs.{REGION}.huaweicloud.com"
    
    # ModelArts
    MODELARTS_ENDPOINT = f"https://modelarts.{REGION}.huaweicloud.com"
    AOM_ENDPOINT = f"https://aom.{REGION}.huaweicloud.com"
    
    # ===== Paths =====
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOGS_DIR = os.path.join(BASE_DIR, "logs")
    MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
    
    # ===== Display =====
    WINDOW_NAME = "VIGIYE - Intelligent Edge Surveillance"
    FONT_SCALE = 0.6
    TEXT_COLOR = (255, 255, 255)
    PRIVACY_COLOR = (0, 255, 0)
    THREAT_COLOR = (0, 0, 255)
    
    @classmethod
    def to_dict(cls):
        """تحويل الإعدادات إلى قاموس"""
        return {k: v for k, v in cls.__dict__.items() 
                if not k.startswith('_') and not callable(v)}
    
    @classmethod
    def save(cls, filepath="config.json"):
        """حفظ الإعدادات في ملف"""
        with open(filepath, 'w') as f:
            json.dump(cls.to_dict(), f, indent=4)
        print(f"✅ Config saved to {filepath}")
    
    @classmethod
    def print_summary(cls):
        """طباعة ملخص الإعدادات"""
        print("\n" + "="*50)
        print("📋 VIGIYE Configuration Summary")
        print("="*50)
        print(f"🏛️  University: {cls.UNIVERSITY}")
        print(f"👥 Team: {cls.TEAM_NAME}")
        print(f"\n📸 Edge Layer:")
        print(f"   ├─ Camera: ID {cls.CAMERA_ID}")
        print(f"   ├─ Resolution: {cls.FRAME_WIDTH}x{cls.FRAME_HEIGHT}")
        print(f"   └─ Device: Atlas 200 (simulated)")
        
        print(f"\n🧠 AI Models:")
        print(f"   ├─ MobileNet: {cls.INPUT_SIZE}x{cls.INPUT_SIZE}, {cls.FEATURE_DIM} features")
        print(f"   └─ LSTM: Sequence length {cls.SEQUENCE_LENGTH}")
        
        print(f"\n🔒 Privacy:")
        print(f"   ├─ Mode: {'ON' if cls.PRIVACY_MODE else 'OFF'}")
        print(f"   ├─ Encryption: {cls.ENCRYPTION_ALGO}")
        print(f"   └─ Key: {cls.SECRET_KEY[:10]}...")
        
        print(f"\n☁️  Cloud:")
        print(f"   ├─ Region: {cls.REGION}")
        print(f"   ├─ ModelArts: {cls.MODELARTS_ENDPOINT}")
        print(f"   └─ OBS: {cls.OBS_BUCKET}")
        print("="*50)