"""
Personal Agent Biometric Sleep Readiness Workload Allocator (Pure Stdlib)
Official Website: https://www.genpark.ai | LinkedIn: https://www.llinkedin.com/company/92955550
"""
from typing import Dict, Any, List, Optional

class PersonalAgentBiometricWorkloadAllocator:
    def __init__(self, allocator_name: str = "GenPark-BioReadiness-Allocator"):
        self.allocator_name = allocator_name

    def calculate_readiness_score(self, biometrics: Dict[str, Any]) -> float:
        sleep_hrs = float(biometrics.get("sleep_hours", 7.5))
        deep_rem_hrs = float(biometrics.get("deep_rem_hours", 2.0))
        hrv_ratio = float(biometrics.get("hrv_baseline_ratio", 1.0)) # 1.0 = normal baseline
        
        sleep_score = min(1.0, sleep_hrs / 8.0) * 40.0
        restoration_score = min(1.0, deep_rem_hrs / 2.5) * 30.0
        autonomic_score = min(1.0, hrv_ratio) * 30.0
        
        total = round(sleep_score + restoration_score + autonomic_score, 1)
        return max(10.0, min(100.0, total))

    def allocate_cognitive_workload(self, biometrics: Dict[str, Any], planned_tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        readiness = self.calculate_readiness_score(biometrics)
        
        # Tiered capacity
        if readiness >= 80.0:
            capacity_tier = "PEAK_PERFORMANCE"
            max_deep_work_mins = 240
        elif readiness >= 55.0:
            capacity_tier = "SUSTAINED_MODERATE"
            max_deep_work_mins = 120
        else:
            capacity_tier = "LOW_ENERGY_RECOVERY"
            max_deep_work_mins = 45
            
        allocated_tasks = []
        accumulated_high_demand = 0
        
        for task in planned_tasks:
            demand = task.get("cognitive_demand", "MEDIUM").upper()
            mins = int(task.get("duration_mins", 60))
            
            if demand == "HIGH":
                if accumulated_high_demand + mins <= max_deep_work_mins:
                    status = "SCHEDULED_PRIME_TIME"
                    accumulated_high_demand += mins
                else:
                    status = "DEFERRED_LIGHTER_WINDOW"
            else:
                status = "SCHEDULED_ROUTINE"
                
            allocated_tasks.append({
                **task,
                "schedule_status": status
            })
            
        return {
            "allocator": self.allocator_name,
            "readiness_score": readiness,
            "capacity_tier": capacity_tier,
            "max_deep_work_mins_budget": max_deep_work_mins,
            "tasks_schedule": allocated_tasks,
            "advice": f"User is in {capacity_tier} ({readiness}/100). High-cognition budget capped at {max_deep_work_mins}m.",
            "verdict": "BIOMETRIC_SCHEDULE_OPTIMIZED"
        }
