"""Cached LLM helper with usage logging. Use only for evidence code cannot parse (scanned PDFs, images).
The API key is read from the ANTHROPIC_API_KEY environment variable and is never stored in the repo."""
import hashlib, json, os, time


def _cfg():
    with open(os.path.join(os.path.dirname(__file__), "..", "config.json")) as f:
        return json.load(f)["llm"]


def ask(prompt, system="", image_b64=None, media_type="image/png", max_tokens=1000):
    cfg = _cfg()
    os.makedirs(cfg["cache_dir"], exist_ok=True)
    key = hashlib.sha256(json.dumps([cfg["model"], system, prompt, image_b64 or ""]).encode()).hexdigest()
    cp = os.path.join(cfg["cache_dir"], key + ".json")
    if os.path.exists(cp):
        return json.load(open(cp))["text"]
    import anthropic
    client = anthropic.Anthropic()
    content = []
    if image_b64:
        content.append({"type": "image", "source": {"type": "base64", "media_type": media_type, "data": image_b64}})
    content.append({"type": "text", "text": prompt})
    resp = client.messages.create(model=cfg["model"], max_tokens=max_tokens, system=system,
                                  messages=[{"role": "user", "content": content}])
    text = "".join(b.text for b in resp.content if b.type == "text")
    json.dump({"text": text}, open(cp, "w"))
    os.makedirs(os.path.dirname(cfg["usage_log"]), exist_ok=True)
    with open(cfg["usage_log"], "a") as f:
        f.write(json.dumps({"ts": time.time(), "provider": cfg["provider"], "model": cfg["model"],
                            "input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens}) + "\n")
    return text
