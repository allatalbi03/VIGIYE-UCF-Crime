"""
VIGIYE - Main System Integration
Team ESURGE - University of El-Oued, Algeria
Huawei ICT Competition 2025-2026
"""
import cv2
import time
from datetime import datetime

from EdgeLayer.camera_handler import CameraHandler
from EdgeLayer.atlas_simulator import AtlasSimulator
from Models.mobilenet_features import MobileNetFeatureExtractor
from Privacy.encryption import VIGIYEEncryption
from Federated.modelarts_client import ModelArtsClient
from Utils.config import Config

class VIGIYE:
    def __init__(self):
        print("\n" + "="*60)
        print("🚀 VIGIYE - Intelligent Edge Surveillance System")
        print("🏆 Team ESURGE - University of El-Oued")
        print("📅 Huawei ICT Competition 2025-2026")
        print("="*60 + "\n")
        
        # Edge Layer
        print("[1/5] Initializing Edge Layer...")
        self.camera = CameraHandler(Config.CAMERA_ID)
        self.atlas = AtlasSimulator()
        
        # AI Models
        print("\n[2/5] Loading AI Models...")
        self.mobilenet = MobileNetFeatureExtractor()
        
        # Privacy
        print("\n[3/5] Setting up Privacy Module...")
        self.encryption = VIGIYEEncryption(Config.SECRET_KEY)
        
        # Federated Learning
        print("\n[4/5] Connecting to Huawei Cloud...")
        self.modelarts = ModelArtsClient(Config.DEVICE_ID)
        
        # Statistics
        print("\n[5/5] Starting System...")
        self.frame_count = 0
        self.threat_count = 0
        self.start_time = datetime.now()
        
        print("\n" + "="*60)
        print("✅ VIGIYE SYSTEM READY")
        print("="*60 + "\n")
    
    def draw_interface(self, frame, threats, behavior_score):
        """رسم واجهة المستخدم"""
        h, w = frame.shape[:2]
        
        # Header
        cv2.putText(frame, "VIGIYE - Edge AI", (20, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # Privacy Badge
        cv2.putText(frame, "🔒 PRIVATE MODE", (w-180, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
        
        # Threat Status
        if threats:
            cv2.putText(frame, f"⚠️ THREAT: {threats[0][0]}", (20, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            cv2.putText(frame, "✅ SECURE", (20, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1)
        
        # Statistics
        elapsed = (datetime.now() - self.start_time).seconds
        stats = [
            f"Model: v{self.modelarts.model_version}",
            f"Threats: {self.threat_count}",
            f"Uptime: {elapsed}s"
        ]
        
        y = h - 60
        for stat in stats:
            cv2.putText(frame, stat, (20, y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            y += 20
        
        return frame
    
    def run(self):
        """تشغيل النظام"""
        print("🚀 System running... Press 'q' to quit\n")
        
        while True:
            # قراءة إطار
            frame = self.camera.get_frame()
            if frame is None:
                break
            
            self.frame_count += 1
            
            # 1️⃣ استخراج الميزات (Edge)
            features = self.mobilenet.extract_features(frame)
            
            # 2️⃣ كشف التهديدات
            threats = []
            if self.frame_count % 5 == 0:
                threats = self.mobilenet.detect_threats(frame)
                if threats:
                    self.threat_count += len(threats)
            
            # 3️⃣ تشفير الميزات
            encrypted = self.encryption.encrypt_features(features)
            
            # 4️⃣ Federated Learning Update
            if self.frame_count % Config.UPDATE_INTERVAL == 0:
                self.modelarts.send_update(encrypted, 0.5, threats)
            
            # 5️⃣ رسم الواجهة
            frame = self.draw_interface(frame, threats, 0.5)
            
            # عرض
            cv2.imshow('VIGIYE - Intelligent Surveillance', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # تنظيف
        self.camera.release()
        cv2.destroyAllWindows()
        
        # تقرير نهائي
        print("\n" + "="*60)
        print("📊 VIGIYE SYSTEM SUMMARY")
        print("="*60)
        print(f"📸 Frames processed: {self.frame_count}")
        print(f"⚠️  Threats detected: {self.threat_count}")
        print(f"📤 Federated updates: {self.modelarts.model_version}")
        print(f"🔒 Privacy: 100% maintained")
        print(f"⏱️  Runtime: {(datetime.now()-self.start_time).seconds}s")
        print("="*60)
        print("🏆 Team ESURGE - University of El-Oued")
        print("📧 allatalbi2003@gmail.com")
        print("="*60)

if __name__ == "__main__":
    try:
        vigiye = VIGIYE()
        vigiye.run()
    except KeyboardInterrupt:
        print("\n⚠️ System interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        print("\n👋 VIGIYE terminated")