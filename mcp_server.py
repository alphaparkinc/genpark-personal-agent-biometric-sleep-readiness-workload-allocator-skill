#!/usr/bin/env python3
import json
import sys
from client import PersonalAgentBiometricWorkloadAllocator

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        allocator = PersonalAgentBiometricWorkloadAllocator()
        bio = {"sleep_hours": 8.0, "deep_rem_hours": 2.5, "hrv_baseline_ratio": 1.1}
        tasks = [
            {"name": "Distributed Consensus Design", "cognitive_demand": "HIGH", "duration_mins": 90},
            {"name": "Email Triage", "cognitive_demand": "LOW", "duration_mins": 30}
        ]
        res = allocator.allocate_cognitive_workload(bio, tasks)
        assert res["readiness_score"] >= 80.0
        assert res["tasks_schedule"][0]["schedule_status"] == "SCHEDULED_PRIME_TIME"
        print(f"[TEST PASS] Bio Readiness Score: {res['readiness_score']}/100")
        sys.exit(0)

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            if method == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"serverInfo": {"name": "genpark-bio-workload-allocator", "version": "1.0.0"}}}))
            elif method == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [{"name": "allocate_cognitive_workload", "description": "Biometric sleep and HRV workload scheduling"}]}}))
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                allocator = PersonalAgentBiometricWorkloadAllocator()
                out = allocator.allocate_cognitive_workload(args.get("biometrics", {}), args.get("planned_tasks", []))
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(out)}]}}))
            else:
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
