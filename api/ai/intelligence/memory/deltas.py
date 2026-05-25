from typing import Dict, Any

class DeltaCalculator:
    def calculate(self, current, snap_24h, snap_7d) -> Dict[str, float]:
        deltas = {}
        
        if snap_24h:
            v_curr = current.velocity_score
            v_old = snap_24h.velocity_score
            if v_old > 0:
                deltas["velocity_24h_pct"] = round(((v_curr - v_old) / v_old) * 100, 1)
            else:
                deltas["velocity_24h_pct"] = 100.0 if v_curr > 0 else 0.0
                
        if snap_7d:
            v_curr = current.velocity_score
            v_old = snap_7d.velocity_score
            if v_old > 0:
                deltas["velocity_7d_pct"] = round(((v_curr - v_old) / v_old) * 100, 1)
            else:
                deltas["velocity_7d_pct"] = 100.0 if v_curr > 0 else 0.0
                
        return deltas

delta_calculator = DeltaCalculator()
