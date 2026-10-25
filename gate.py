def is_deletion_request(text, keywords):
    """Heuristic first pass. Check it against the NOT_APPLICABLE rows in sample_output.csv and refine
    (or replace with an LLM call in audit/llm.py for ambiguous wording or negations)."""
    t = (text or "").lower()
    return any(k in t for k in keywords)
