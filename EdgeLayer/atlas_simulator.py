"""
Edge Layer - Atlas 200 AI Module Simulator
"""
import time
import psutil

class AtlasSimulator:
    def __init__(self):
        self.temperature = 45  # درجة حرارة المحاكاة
        self.power_consumption = 5  # واط
        print("✅ Atlas 200 AI Module initialized (simulation)")
    
    def get_stats(self):
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        return {
            'temperature': self.temperature,
            'power': self.power_consumption,
            'cpu': cpu_percent,
            'memory': memory_percent,
            'status': 'active'
        }