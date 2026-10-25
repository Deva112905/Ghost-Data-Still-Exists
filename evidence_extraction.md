You read one evidence file (scanned PDF or image) for a data-deletion audit.
Return JSON only: {"records":[{"system_id":"","resource_id":"","identifiers_visible":["email","name","phone","email_hash"],"state":"PRESENT|ABSENT|REDACTED|ANONYMIZED"}]}.
Report only what is visible. If unreadable, return {"records":[],"unreadable":true}. Do not guess.
