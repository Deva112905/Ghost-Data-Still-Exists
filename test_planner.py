import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from audit.planner import plan
from audit.ordering import PHASES, OPS

cases = json.load(open(os.path.join(os.path.dirname(__file__), "..", "evaluation", "extra_cases", "cases.json")))


def test_extra_cases():
    for c in cases:
        status, steps = plan(c["items"])
        assert status == c["expect_status"], c["name"]
        assert [s["operation"] for s in steps if True] and sorted(s["operation"] for s in steps) == sorted(c["expect_ops"]), c["name"]
        assert [s["step_no"] for s in steps] == list(range(1, len(steps) + 1))
        keys = [(PHASES.index(s["phase"]), OPS[s["phase"]].index(s["operation"]), s["system_id"], s["resource_id"]) for s in steps]
        assert keys == sorted(keys), c["name"]
        if status == "COMPLETE":
            assert all(s["phase"] == "VERIFICATION" and s["evidence_id"] for s in steps)
        else:
            assert all(s["evidence_id"] == "" for s in steps if s["phase"] != "FINDING")


if __name__ == "__main__":
    test_extra_cases(); print("all tests passed")
