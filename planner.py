"""Turns audited items into status + ordered steps.

An item is one thing the policy has a requirement for:
  {system_id, resource_id, required, actual, evidence_id}
  required: ABSENT | REDACTED | ANONYMIZED | PRESENT | DISABLED | BLOCKED   (from deletion_rules.csv)
  actual:   the state found at audit_at (same vocabulary; ACTIVE/PRESENT mean "still exposed")
"""
from .ordering import sort_and_number

FINDING_OP = {"ABSENT": "REPORT_REMAINING_RECORD", "REDACTED": "REPORT_EXPOSED_PII", "ANONYMIZED": "REPORT_EXPOSED_PII",
              "DISABLED": "REPORT_ACTIVE_DATA_FLOW", "BLOCKED": "REPORT_RESTORE_RISK"}
FIX_OP = {"ABSENT": "DELETE_RECORD", "REDACTED": "REDACT_RECORD", "ANONYMIZED": "ANONYMIZE_RECORD",
          "DISABLED": "DISABLE_DATA_FLOW", "BLOCKED": "BLOCK_RESTORE"}
VERIFY_OP = {"ABSENT": "VERIFY_RECORD_ABSENT", "PRESENT": "VERIFY_RECORD_PRESENT", "REDACTED": "VERIFY_RECORD_REDACTED",
             "ANONYMIZED": "VERIFY_RECORD_ANONYMIZED", "DISABLED": "VERIFY_DATA_FLOW_DISABLED",
             "BLOCKED": "VERIFY_RESTORE_BLOCKED"}


def compliant(item):
    return item["actual"] == item["required"]


def plan(items, verify_all_in_incomplete=True):
    """Return (status, steps). status is COMPLETE or INCOMPLETE."""
    bad = [i for i in items if not compliant(i) and i["required"] in FIX_OP]
    steps = []
    if not bad:
        for i in items:
            steps.append(_s("VERIFICATION", VERIFY_OP[i["required"]], i, i.get("evidence_id", "")))
        return "COMPLETE", sort_and_number(steps)
    for i in bad:
        steps.append(_s("FINDING", FINDING_OP[i["required"]], i, i.get("evidence_id", "")))
        steps.append(_s("REMEDIATION", FIX_OP[i["required"]], i, ""))
    for i in (items if verify_all_in_incomplete else bad):
        steps.append(_s("VERIFICATION", VERIFY_OP[i["required"]], i, ""))
    return "INCOMPLETE", sort_and_number(steps)


def _s(phase, op, item, evidence_id):
    return {"phase": phase, "operation": op, "system_id": item["system_id"],
            "resource_id": item["resource_id"], "evidence_id": evidence_id}
