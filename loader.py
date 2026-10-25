import csv, os


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


class Dataset:
    def __init__(self, root):
        r = lambda n: read_csv(os.path.join(root, n))
        self.requests = r("deletion_requests.csv")
        self.identities = r("user_identities.csv")
        self.audit_log = r("user_audit_log.csv")
        self.activity = r("system_activity.csv")
        self.rules = r("deletion_rules.csv")
        self.evidence = r("evidence_files.csv")
        self.root = root
