"""
Federated Learning Module
Model aggregation and distribution
"""

import numpy as np
import hashlib
import json
from datetime import datetime
from collections import defaultdict

class FederatedLearning:
    def __init__(self, federation_id="VIGIYE_FED_001"):
        """
        Federated Learning coordinator
        Args:
            federation_id: معرف المجموعة
        """
        self.federation_id = federation_id
        self.global_model_version = 0
        self.clients = {}  # الأجهزة المتصلة
        self.updates_buffer = []  # التحديثات الواردة
        self.aggregated_models = []
        
        print(f"✅ Federated Learning coordinator ready (ID: {federation_id})")
    
    def register_client(self, client_id, device_type="Atlas 200"):
        """تسجيل جهاز جديد في المجموعة"""
        self.clients[client_id] = {
            'id': client_id,
            'type': device_type,
            'registered_at': datetime.now().isoformat(),
            'last_update': None,
            'updates_count': 0,
            'status': 'active'
        }
        print(f"📱 Client {client_id} registered")
        return True
    
    def receive_update(self, client_id, encrypted_weights, metrics):
        """استقبال تحديث من جهاز"""
        if client_id not in self.clients:
            print(f"⚠️ Unknown client: {client_id}")
            return False
        
        update = {
            'client_id': client_id,
            'timestamp': datetime.now().isoformat(),
            'model_version': self.global_model_version,
            'encrypted_weights': encrypted_weights[:50] + "...",  # تخزين مختصر
            'metrics': metrics,
            'weight_hash': hashlib.sha256(str(encrypted_weights).encode()).hexdigest()[:16]
        }
        
        self.updates_buffer.append(update)
        self.clients[client_id]['last_update'] = datetime.now().isoformat()
        self.clients[client_id]['updates_count'] += 1
        
        print(f"📥 Received update from {client_id}")
        print(f"   ├─ Accuracy: {metrics.get('accuracy', 0):.2f}")
        print(f"   ├─ Samples: {metrics.get('num_samples', 0)}")
        print(f"   └─ Buffer: {len(self.updates_buffer)} updates")
        
        return True
    
    def aggregate_updates(self, min_updates=3):
        """دمج التحديثات (Federated Averaging)"""
        if len(self.updates_buffer) < min_updates:
            print(f"⏳ Waiting for more updates ({len(self.updates_buffer)}/{min_updates})")
            return None
        
        print(f"\n🔄 Aggregating {len(self.updates_buffer)} updates...")
        
        # محاكاة عملية الدمج
        aggregated_model = {
            'version': self.global_model_version + 1,
            'timestamp': datetime.now().isoformat(),
            'num_clients': len(self.updates_buffer),
            'aggregation_method': 'FedAvg',
            'clients': [u['client_id'] for u in self.updates_buffer],
            'average_accuracy': np.mean([u['metrics'].get('accuracy', 0) for u in self.updates_buffer]),
            'total_samples': sum([u['metrics'].get('num_samples', 0) for u in self.updates_buffer]),
            'model_hash': hashlib.sha256(str(self.updates_buffer).encode()).hexdigest()[:16]
        }
        
        self.aggregated_models.append(aggregated_model)
        self.global_model_version += 1
        
        print(f"✅ Aggregation complete - Global model v{self.global_model_version}")
        print(f"   ├─ Clients: {aggregated_model['num_clients']}")
        print(f"   ├─ Avg Accuracy: {aggregated_model['average_accuracy']:.2f}")
        print(f"   └─ Total samples: {aggregated_model['total_samples']}")
        
        # مسح المخزن المؤقت
        self.updates_buffer = []
        
        return aggregated_model
    
    def distribute_model(self, client_id=None):
        """توزيع النموذج المحدث على الأجهزة"""
        if not self.aggregated_models:
            print("⚠️ No aggregated model available")
            return None
        
        latest_model = self.aggregated_models[-1]
        
        if client_id:
            # توزيع على جهاز محدد
            print(f"📤 Distributing model v{latest_model['version']} to {client_id}")
            return latest_model
        else:
            # توزيع على كل الأجهزة
            print(f"📤 Broadcasting model v{latest_model['version']} to all clients")
            for client in self.clients:
                print(f"   ├─ Sent to {client}")
            return latest_model
    
    def get_federation_stats(self):
        """إحصائيات المجموعة"""
        return {
            'federation_id': self.federation_id,
            'global_version': self.global_model_version,
            'active_clients': len([c for c in self.clients.values() if c['status'] == 'active']),
            'total_clients': len(self.clients),
            'updates_in_buffer': len(self.updates_buffer),
            'aggregations_performed': len(self.aggregated_models),
            'total_updates_received': sum(c['updates_count'] for c in self.clients.values())
        }
    
    def simulate_training_round(self):
        """محاكاة جولة تدريب (للعرض)"""
        print("\n" + "🔄"*30)
        print("🔄 Federated Learning Round Simulation")
        print("🔄"*30)
        
        # محاكاة 3 أجهزة ترسل تحديثات
        clients = ["CAM_001", "CAM_002", "CAM_003"]
        for client in clients:
            if client not in self.clients:
                self.register_client(client)
            
            # محاكاة تحديث
            metrics = {
                'accuracy': 0.75 + np.random.random() * 0.2,
                'num_samples': 500 + int(np.random.random() * 500),
                'loss': 0.1 + np.random.random() * 0.3
            }
            fake_weights = f"encrypted_weights_v{self.global_model_version}_{'x'*50}"
            self.receive_update(client, fake_weights, metrics)
        
        # دمج التحديثات
        aggregated = self.aggregate_updates(min_updates=3)
        
        # توزيع النموذج
        self.distribute_model()
        
        return aggregated