"""SCHEMA-DEPENDENT PART. Implement once you have inspected the real CSV headers.

discover(case, ds) must return a list of items (see planner.py) for one case:
  1. identity : email -> user_id via ds.identities; then every historical email/phone/hash via ds.audit_log.
  2. state    : replay ds.activity up to case['audit_at'] (deletes, syncs, exports, backups, restores, indexing);
                confirm against evidence files listed in ds.evidence (SQL snapshots, logs, JSON, PDF, images).
                reported_status and operation 'success' results are CLAIMS, not proof.
  3. rules    : join each found record's data category to ds.rules for the required treatment
                (delete / redact / anonymize / retain), including account tombstones.
  4. flows    : active syncs/imports that can recreate data -> required DISABLED.
  5. restores : backups/restore paths that can bring data back -> required BLOCKED.
"""


def discover(case, ds):
    raise NotImplementedError("Implement audit/discover.py against the real dataset schema (see docstring).")
