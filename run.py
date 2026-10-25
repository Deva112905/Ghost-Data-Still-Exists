"""python run.py [--dry-run]   -> writes output.csv"""
import argparse, json
from audit.loader import Dataset
from audit.gate import is_deletion_request
from audit.discover import discover
from audit.planner import plan
from audit.writer import write_output
from audit import usage_report

ap = argparse.ArgumentParser()
ap.add_argument("--dry-run", action="store_true", help="only apply the NOT_APPLICABLE gate; deletion cases are skipped")
args = ap.parse_args()
cfg = json.load(open("config.json"))
ds = Dataset(cfg["dataset_dir"])
rows, skipped = [], 0
for case in ds.requests:
    if not is_deletion_request(case["request_text"], cfg["not_applicable_keywords_any_of_deletion"]):
        rows.append({"case_id": case["case_id"], "deletion_status": "NOT_APPLICABLE", "steps": []})
        continue
    if args.dry_run:
        skipped += 1
        continue
    status, steps = plan(discover(case, ds), cfg["verify_all_in_incomplete"])
    rows.append({"case_id": case["case_id"], "deletion_status": status, "steps": steps})
if args.dry_run:
    print(f"dry run: {len(rows)} NOT_APPLICABLE, {skipped} deletion cases not processed (output not written)")
else:
    write_output(rows, cfg["output_path"], expected_rows=len(ds.requests))
    usage_report.build(len(ds.requests))
    print(f"wrote {len(rows)} rows to {cfg['output_path']}")
