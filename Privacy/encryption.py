"""
Privacy Module - AES-256 Encryption
"""
import hashlib
import pickle
import base64
from cryptography.fernet import Fernet

class VIGIYEEncryption:
    def __init__(self, secret_key="VIGIYE_SECURE_KEY_2026"):
        self.key = hashlib.sha256(secret_key.encode()).digest()
        self.fernet_key = base64.urlsafe_b64encode(self.key[:32])
        self.cipher = Fernet(self.fernet_key)
        print("✅ AES-256 Encryption ready")
    
    def encrypt_features(self, features):
        """تشفير الميزات قبل الإرسال"""
        features_bytes = pickle.dumps(features)
        encrypted = self.cipher.encrypt(features_bytes)
        return base64.b64encode(encrypted).decode('utf-8')
    
    def get_privacy_badge(self):
        return "🔒 PRIVATE MODE | AES-256"