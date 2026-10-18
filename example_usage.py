from client import PersonalAgentBiometricWorkloadAllocator

def main():
    allocator = PersonalAgentBiometricWorkloadAllocator()
    bio = {"sleep_hours": 5.2, "deep_rem_hours": 0.8, "hrv_baseline_ratio": 0.72}
    tasks = [
        {"name": "System Architecture Review", "cognitive_demand": "HIGH", "duration_mins": 90},
        {"name": "Database Sharding Spec", "cognitive_demand": "HIGH", "duration_mins": 60},
        {"name": "Team Standup", "cognitive_demand": "LOW", "duration_mins": 15}
    ]
    res = allocator.allocate_cognitive_workload(bio, tasks)
    print("--- Biometric Workload Allocation ---")
    print(f"Readiness Score: {res['readiness_score']} | Tier: {res['capacity_tier']}")
    print(f"Advice: {res['advice']}")
    for t in res['tasks_schedule']:
        print(f"* [{t['schedule_status']}] {t['name']} ({t['duration_mins']}m, {t['cognitive_demand']})")

if __name__ == "__main__":
    main()
