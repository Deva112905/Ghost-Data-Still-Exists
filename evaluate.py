"""python evaluation/evaluate.py predicted.csv truth.csv  -> prints metrics, writes evaluation/evaluation_report.md
Use with sample_output.csv as truth after running run.py on sample_deletion_requests.csv."""
import csv, json, sys, collections

FIELDS = ["phase", "system_id", "resource_id", "operation", "state", "evidence_id"]


def load(p):
    return {r["case_id"]: (r["deletion_status"], json.loads(r["steps_json"] or "[]"))
            for r in csv.DictReader(open(p, newline="", encoding="utf-8-sig"))}


def tup(s):
    return tuple(s.get(f, "") for f in FIELDS)


def score(pred, truth):
    n = len(truth)
    status_ok = seq_ok = 0
    tp = fp = fn = 0
    field_ok = collections.Counter(); field_n = 0
    wrong = []
    for cid, (ts, tsteps) in truth.items():
        ps, psteps = pred.get(cid, ("MISSING", []))
        status_ok += ps == ts
        a, b = collections.Counter(map(tup, psteps)), collections.Counter(map(tup, tsteps))
        inter = sum((a & b).values()); tp += inter; fp += sum(a.values()) - inter; fn += sum(b.values()) - inter
        for p, t in zip(psteps, tsteps):
            field_n += 1
            for f in FIELDS:
                field_ok[f] += p.get(f, "") == t.get(f, "")
        exact = ps == ts and [tup(s) for s in psteps] == [tup(s) for s in tsteps]
        seq_ok += exact
        if not exact:
            wrong.append(cid)
    prec = tp / (tp + fp) if tp + fp else 1.0
    rec = tp / (tp + fn) if tp + fn else 1.0
    return {"cases": n, "status_accuracy": status_ok / n, "step_precision": prec, "step_recall": rec,
            "step_f1": 2 * prec * rec / (prec + rec) if prec + rec else 0.0,
            "field_accuracy": {f: field_ok[f] / field_n if field_n else None for f in FIELDS},
            "sequence_exact_match": seq_ok / n, "failing_cases": wrong}


if __name__ == "__main__":
    m = score(load(sys.argv[1]), load(sys.argv[2]))
    print(json.dumps(m, indent=2))
    with open("evaluation/evaluation_report.md", "w") as f:
        f.write("# Evaluation report\n\n```json\n" + json.dumps({k: v for k, v in m.items() if k != "failing_cases"}, indent=2)
                + "\n```\n\nFailing cases: " + ", ".join(m["failing_cases"][:50]) + "\n\n"
                "## Additional cases\nSee evaluation/extra_cases/ and tests/test_planner.py.\n\n"
                "## Failures found and improvements made\n(fill in after each iteration)\n")
