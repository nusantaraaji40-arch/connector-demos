#!/usr/bin/env python3
"""Demo baca akun dan daftar Cloud Agents Cursor.

Pola mengikuti dokumentasi Cursor (docs.cursor.com):
- Base URL: https://api.cursor.com
- Cloud Agents API menerima `Authorization: Bearer <key>`.
- Key dibuat di cursor.com/dashboard -> API Keys, scope `admin:*`,
  format `crsr_...`.

Perhatian:
- Akun gratis ditolak 403 `plan_required` — Cloud Agents butuh Pro.
- Cursor tidak menyediakan key read-only; key ini bisa meluncurkan
  agen yang membuat branch dan pull request.
- Key dibaca dari environment, tidak pernah ditulis di repo.
"""
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_BASE_URL = "https://api.cursor.com"


def call_cursor(path, api_key):
    request = urllib.request.Request(path)
    request.add_header("Authorization", "Bearer " + api_key)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            return e.code, json.loads(raw)
        except ValueError:
            return e.code, {"raw": raw}


def explain(status, body):
    error = body.get("error", {}) if isinstance(body, dict) else {}
    if status == 403 and error.get("code") == "plan_required":
        print("Akun ini paket gratis: Cloud Agent tidak tersedia.", file=sys.stderr)
        print("Upgrade ke Pro untuk memakai Cloud Agents API.", file=sys.stderr)
        return True
    if status == 401:
        print("Key ditolak (401). Periksa nilai key dan reconnect.", file=sys.stderr)
        return True
    return False


def main():
    api_key = os.environ.get("CURSOR_API_KEY", "")
    base = os.environ.get("CURSOR_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    if not api_key:
        print("CURSOR_API_KEY kosong. Isi dari .env (lihat .env.example).", file=sys.stderr)
        return 2
    status, body = call_cursor(f"{base}/v1/me", api_key)
    if status != 200:
        print(f"GET /v1/me gagal ({status}): {json.dumps(body, indent=2)}", file=sys.stderr)
        explain(status, body)
        return 1
    print(f"Akun: {body.get('name')} <{body.get('email')}> (id: {body.get('id')})")
    status, body = call_cursor(f"{base}/v1/agents", api_key)
    if status != 200:
        print(f"GET /v1/agents gagal ({status}): {json.dumps(body, indent=2)}", file=sys.stderr)
        explain(status, body)
        return 1
    items = body if isinstance(body, list) else body.get("agents", body.get("data", []))
    if not items:
        print("Tidak ada Cloud Agents.")
        return 0
    for item in items:
        print(f"- {item.get('id')}  status: {item.get('status')}  {item.get('name', '')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
