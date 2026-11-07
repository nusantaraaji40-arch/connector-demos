#!/usr/bin/env python3
"""Demo baca akun Codeberg (Forgejo).

Codeberg memakai API yang sama dengan Gitea (Forgejo):
- Base URL: https://codeberg.org/api/v1
- Auth: header `Authorization: token <token>` (kata `token` literal).
- Token dibuat di Codeberg -> Settings -> Applications -> Manage Access Tokens.
- Versi server terkonfirmasi: Forgejo 16.0.0-dev.

Token dibaca dari environment, tidak pernah ditulis di repo.
"""
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_BASE_URL = "https://codeberg.org"


def main():
    token = os.environ.get("CODEBERG_TOKEN", "")
    base = os.environ.get("CODEBERG_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    if not token:
        print("CODEBERG_TOKEN kosong. Isi dari .env (lihat .env.example).", file=sys.stderr)
        return 2
    request = urllib.request.Request(f"{base}/api/v1/user")
    request.add_header("Authorization", "token " + token)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        print(f"Gagal ({e.code}): {raw}", file=sys.stderr)
        return 1
    print(f"Akun: {body.get('login')} <{body.get('email')}> (id: {body.get('id')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
