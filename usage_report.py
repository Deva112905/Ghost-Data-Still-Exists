import json, os, sys, collections


def build(n_requests, log="evaluation/usage_log.jsonl", cfg_path="config.json", out="evaluation/usage_report.md"):
    cfg = json.load(open(cfg_path))["llm"]
    rows = [json.loads(l) for l in open(log)] if os.path.exists(log) else []
    per = collections.defaultdict(lambda: [0, 0, 0])
    for r in rows:
        p = per[(r["provider"], r["model"])]
        p[0] += 1; p[1] += r["input_tokens"]; p[2] += r["output_tokens"]
    cost = lambda i, o: i / 1e6 * cfg["price_per_mtok_input"] + o / 1e6 * cfg["price_per_mtok_output"]
    L = ["# Usage report", "", f"Requests audited: {n_requests}", "",
         "| Provider | Model | Calls | Input tokens | Output tokens | Est. cost (USD) |", "|---|---|---|---|---|---|"]
    ti = to = tc = 0
    for (pv, m), (c, i, o) in per.items():
        L.append(f"| {pv} | {m} | {c} | {i} | {o} | {cost(i, o):.4f} |"); ti += i; to += o; tc += c
    tot = cost(ti, to)
    L += ["", f"**Overall:** {tc} calls, {ti} input tokens, {to} output tokens, ${tot:.4f} total.",
          f"**Per request:** {(ti + to) / max(n_requests, 1):.1f} tokens, ${tot / max(n_requests, 1):.6f}.",
          "", "Prices come from config.json and must match the provider's current price list."]
    open(out, "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    build(int(sys.argv[1]))
