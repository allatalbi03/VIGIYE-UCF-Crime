"""
Logger Module - System Monitoring
"""

import logging
import os
from datetime import datetime

class VIGIYELogger:
    def __init__(self, log_file="vigiye.log", level="INFO"):
        """
        VIGIYE System Logger
        Args:
            log_file: اسم ملف السجل
            level: مستوى التسجيل (INFO, DEBUG, WARNING, ERROR)
        """
        self.log_file = log_file
        self.level = level
        
        # إنشاء مجلد logs إذا لم يكن موجوداً
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_path = os.path.join(log_dir, log_file)
        
        # إعداد logger
        self.logger = logging.getLogger('VIGIYE')
        self.logger.setLevel(getattr(logging, level))
        
        # File handler
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(getattr(logging, level))
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, level))
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        self.events = []
        print(f"✅ Logger initialized (Level: {level}, File: {log_file})")
    
    def info(self, message, component="System"):
        """تسجيل معلومات"""
        self.logger.info(f"[{component}] {message}")
        self._store_event('INFO', component, message)
    
    def debug(self, message, component="System"):
        """تسجيل تصحيح"""
        self.logger.debug(f"[{component}] {message}")
        self._store_event('DEBUG', component, message)
    
    def warning(self, message, component="System"):
        """تسجيل تحذير"""
        self.logger.warning(f"[{component}] {message}")
        self._store_event('WARNING', component, message)
    
    def error(self, message, component="System"):
        """تسجيل خطأ"""
        self.logger.error(f"[{component}] {message}")
        self._store_event('ERROR', component, message)
    
    def _store_event(self, level, component, message):
        """تخزين الحدث في الذاكرة"""
        self.events.append({
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'component': component,
            'message': message
        })
    
    def get_events(self, level=None, last_n=None):
        """استرجاع الأحداث المسجلة"""
        events = self.events
        if level:
            events = [e for e in events if e['level'] == level]
        if last_n:
            events = events[-last_n:]
        return events
    
    def get_summary(self):
        """ملخص التسجيلات"""
        summary = {
            'total_events': len(self.events),
            'by_level': {
                'INFO': len([e for e in self.events if e['level'] == 'INFO']),
                'DEBUG': len([e for e in self.events if e['level'] == 'DEBUG']),
                'WARNING': len([e for e in self.events if e['level'] == 'WARNING']),
                'ERROR': len([e for e in self.events if e['level'] == 'ERROR'])
            },
            'by_component': {}
        }
        
        for event in self.events:
            comp = event['component']
            if comp not in summary['by_component']:
                summary['by_component'][comp] = 0
            summary['by_component'][comp] += 1
        
        return summary
    
    def edge_event(self, message):
        """تسجيل حدث في Edge Layer"""
        self.info(message, "Edge")
    
    def cloud_event(self, message):
        """تسجيل حدث في Cloud Layer"""
        self.info(message, "Cloud")
    
    def privacy_event(self, message):
        """تسجيل حدث خصوصية"""
        self.info(message, "Privacy")
    
    def threat_event(self, threat_type, confidence):
        """تسجيل حدث تهديد"""
        self.warning(f"Threat detected: {threat_type} (conf={confidence:.2f})", "Security")