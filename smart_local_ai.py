"""
Enhanced Local AI with Machine Learning
Uses scikit-learn for local pattern recognition
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LinearRegression
import pickle
import os

class SmartLocalAI:
    def __init__(self):
        self.sms_classifier = None
        self.demand_predictor = None
        self.vectorizer = None
        self.load_or_train_models()
        
    def load_or_train_models(self):
        """Load existing models or train new ones"""
        if os.path.exists('sms_model.pkl'):
            self.load_models()
        else:
            self.train_models()
    
    def train_models(self):
        """Train local ML models with sample data"""
        # Sample SMS training data
        sms_data = [
            ("need water urgent", "urgent"),
            ("pump not working", "urgent"),
            ("water finished", "medium"),
            ("hello how are you", "not_water"),
            ("tank empty help", "urgent"),
            ("good morning", "not_water"),
            ("water please", "medium"),
            ("emergency no water", "urgent"),
            ("thank you", "not_water"),
            ("pump broken", "urgent")
        ]
        
        texts = [item[0] for item in sms_data]
        labels = [item[1] for item in sms_data]
        
        # Train SMS classifier
        self.vectorizer = TfidfVectorizer(max_features=100)
        X = self.vectorizer.fit_transform(texts)
        
        self.sms_classifier = MultinomialNB()
        self.sms_classifier.fit(X, labels)
        
        # Save models
        self.save_models()
        print("Local AI models trained and saved")
    
    def save_models(self):
        """Save trained models"""
        with open('sms_model.pkl', 'wb') as f:
            pickle.dump({
                'classifier': self.sms_classifier,
                'vectorizer': self.vectorizer
            }, f)
    
    def load_models(self):
        """Load saved models"""
        with open('sms_model.pkl', 'rb') as f:
            models = pickle.load(f)
            self.sms_classifier = models['classifier']
            self.vectorizer = models['vectorizer']
        print("Local AI models loaded")
    
    def classify_sms(self, message: str) -> Dict:
        """Classify SMS using local ML"""
        if not self.sms_classifier:
            return {"urgency": "medium", "confidence": 0.5}
        
        X = self.vectorizer.transform([message.lower()])
        prediction = self.sms_classifier.predict(X)[0]
        confidence = max(self.sms_classifier.predict_proba(X)[0])
        
        return {
            "urgency": prediction,
            "confidence": float(confidence),
            "is_water_request": prediction != "not_water"
        }

class AdvancedLocalBridge:
    def __init__(self):
        self.smart_ai = SmartLocalAI()
        self.demand_buffer = []
        
    def process_sms_smart(self, sender: str, message: str):
        """Smart SMS processing with ML"""
        analysis = self.smart_ai.classify_sms(message)
        
        # Village detection
        village = "A"
        if "village b" in message.lower() or "b" in sender.lower():
            village = "B"
        
        result = {
            "village": village,
            "urgency": analysis["urgency"],
            "confidence": analysis["confidence"],
            "is_water_request": analysis["is_water_request"]
        }
        
        print(f"Smart AI: {village} - {analysis['urgency']} ({analysis['confidence']:.2f} confidence)")
        return result
    
    def adaptive_pump_control(self, village_data: Dict):
        """Adaptive pump control based on patterns"""
        total_demand = sum(village_data.values())
        
        # Store demand history
        self.demand_buffer.append({
            'timestamp': time.time(),
            'demand': total_demand
        })
        
        # Keep only last 24 hours
        cutoff = time.time() - 86400
        self.demand_buffer = [d for d in self.demand_buffer if d['timestamp'] > cutoff]
        
        # Calculate trend
        if len(self.demand_buffer) > 5:
            recent_avg = np.mean([d['demand'] for d in self.demand_buffer[-5:]])
            older_avg = np.mean([d['demand'] for d in self.demand_buffer[-10:-5]]) if len(self.demand_buffer) > 10 else recent_avg
            
            trend = "increasing" if recent_avg > older_avg else "stable"
        else:
            trend = "stable"
        
        # Smart decisions
        if total_demand >= 6 or trend == "increasing":
            return {
                "pump1_action": "start",
                "pump2_action": "start",
                "reason": f"High demand ({total_demand}) or increasing trend"
            }
        elif total_demand >= 3:
            return {
                "pump1_action": "start",
                "pump2_action": "maintain",
                "reason": f"Medium demand ({total_demand})"
            }
        else:
            return {
                "pump1_action": "maintain",
                "pump2_action": "maintain", 
                "reason": f"Low demand ({total_demand})"
            }

# Simple setup script
def setup_local_ai():
    """Setup local AI bridge"""
    print("🤖 Setting up Local AI Bridge...")
    
    # Install required packages
    import subprocess
    import sys
    
    packages = ['scikit-learn', 'numpy', 'pyserial', 'requests']
    for package in packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
    
    print("✅ Local AI Bridge ready!")
    print("No external APIs needed - everything runs locally")

if __name__ == "__main__":
    setup_local_ai()
    
    # Run the bridge
    bridge = AdvancedLocalBridge()
    
    # Test SMS classification
    test_messages = [
        "need water urgent",
        "hello how are you", 
        "pump not working help",
        "thank you"
    ]
    
    for msg in test_messages:
        result = bridge.process_sms_smart("+254700000001", msg)
        print(f"'{msg}' -> {result}")
