#!/usr/bin/env python3
"""Demo chat Grok (xAI) dengan API key.

Pola mengikuti dokumentasi resmi xAI (docs.x.ai):
- Base URL: https://api.x.ai/v1 (OpenAI-compatible)
- Auth: header `Authorization: Bearer <key>`, key berawalan `xai-`
- Key dibuat di console.x.ai -> API Keys, setelah membeli kredit prepaid.
- Tes key tanpa biaya token: python3 chat.py --list-models

Biaya: Grok API berbayar per token dari kredit prepaid, tanpa free tier.
Key dibaca dari environment, tidak pernah ditulis di repo.
"""
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_BASE_URL = "https://api.x.ai"
DEFAULT_MODEL = "grok-4.7"


def load_config():
    api_key = os.environ.get("GROK_API_KEY", "")
    model = os.environ.get("GROK_MODEL", DEFAULT_MODEL)
    base = os.environ.get("GROK_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    if not api_key:
        print("GROK_API_KEY kosong. Isi dari .env (lihat .env.example).", file=sys.stderr)
        sys.exit(2)
    return base, api_key, model


def call_grok(path, api_key, method="GET", payload=None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(path, data=data, method=method)
    request.add_header("Content-Type", "application/json")
    request.add_header("Authorization", "Bearer " + api_key)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            return e.code, json.loads(raw)
        except ValueError:
            return e.code, {"raw": raw}


def list_models(base, api_key):
    status, body = call_grok(f"{base}/v1/models", api_key)
    if status != 200:
        print(f"Gagal ({status}): {json.dumps(body, indent=2)}", file=sys.stderr)
        return 1
    for item in body.get("data", []):
        print(f"- {item.get('id')}")
    return 0


def chat(base, api_key, model, prompt):
    status, body = call_grok(
        f"{base}/v1/chat/completions",
        api_key,
        method="POST",
        payload={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 800,
        },
    )
    if status != 200:
        print(f"Gagal ({status}): {json.dumps(body, indent=2)}", file=sys.stderr)
        return 1
    choice = body["choices"][0]["message"]["content"]
    usage = body.get("usage", {})
    print(choice)
    print()
    print(
        f"[model: {model} | token: prompt {usage.get('prompt_tokens')}, "
        f"jawaban {usage.get('completion_tokens')}, total {usage.get('total_tokens')}]"
    )
    return 0


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    base, api_key, model = load_config()
    if "--list-models" in flags:
        return list_models(base, api_key)
    if not args:
        print('Pakai: python3 chat.py "pesan kamu"  atau  python3 chat.py --list-models',
              file=sys.stderr)
        return 2
    return chat(base, api_key, model, " ".join(args))


if __name__ == "__main__":
    sys.exit(main())
