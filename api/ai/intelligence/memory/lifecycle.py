class LifecycleClassifier:
    def classify(self, current, snap_24h, snap_7d) -> str:
        # Default state
        if not snap_24h:
            return "Emerging"
            
        v_curr = current.velocity_score
        v_24h = snap_24h.velocity_score
        
        # Calculate 24h delta
        if v_24h == 0:
            delta = 100.0 if v_curr > 0 else 0.0
        else:
            delta = ((v_curr - v_24h) / v_24h) * 100
            
        if delta > 50:
            return "Accelerating"
        elif delta > 10:
            return "Emerging"
        elif delta > -10:
            if v_curr > 80:
                return "Peaking"
            return "Stabilizing"
        elif delta > -50:
            return "Decaying"
        else:
            return "Dormant"

lifecycle_classifier = LifecycleClassifier()
