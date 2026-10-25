import csv, json


def write_output(rows, path, expected_rows=None):
    rows = sorted(rows, key=lambda r: r["case_id"])
    ids = [r["case_id"] for r in rows]
    assert len(ids) == len(set(ids)), "duplicate case_id"
    if expected_rows is not None:
        assert len(rows) == expected_rows, f"expected {expected_rows} rows, got {len(rows)}"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["case_id", "deletion_status", "steps_json"])
        for r in rows:
            if r["deletion_status"] == "NOT_APPLICABLE":
                assert r["steps"] == [], "NOT_APPLICABLE must have []"
            w.writerow([r["case_id"], r["deletion_status"], json.dumps(r["steps"], separators=(",", ":"))])
