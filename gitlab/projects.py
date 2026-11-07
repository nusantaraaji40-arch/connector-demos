#!/usr/bin/env python3
"""Demo baca akun dan daftar project GitLab.

Pola mengikuti dokumentasi GitLab (docs.gitlab.com, REST API v4):
- Base URL: https://gitlab.com/api/v4
- Auth: header `PRIVATE-TOKEN: <token>` (personal access token).
- Token dibuat di GitLab -> Preferences -> Access Tokens.
  Untuk demo ini token butuh scope `read_user` dan `read_api`
  (atau token fine-grained dengan User: Read + Project: Read).

Token dibaca dari environment, tidak pernah ditulis di repo.
"""
import json
import os
import sys
import urllib.error
import urllib.request
import urllib.parse

DEFAULT_BASE_URL = "https://gitlab.com"


def call_gitlab(path, token):
    request = urllib.request.Request(path)
    request.add_header("PRIVATE-TOKEN", token)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            return e.code, json.loads(raw)
        except ValueError:
            return e.code, {"raw": raw}


def main():
    token = os.environ.get("GITLAB_TOKEN", "")
    base = os.environ.get("GITLAB_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    if not token:
        print("GITLAB_TOKEN kosong. Isi dari .env (lihat .env.example).", file=sys.stderr)
        return 2
    status, body = call_gitlab(f"{base}/api/v4/user", token)
    if status == 403:
        print("Token ditolak 403: kurang scope (butuh User: Read).", file=sys.stderr)
        print(f"Detail: {json.dumps(body)}", file=sys.stderr)
        return 1
    if status != 200:
        print(f"GET /user gagal ({status}): {json.dumps(body, indent=2)}", file=sys.stderr)
        return 1
    print(f"Akun: {body.get('username')} <{body.get('email')}> (id: {body.get('id')})")
    query = urllib.parse.urlencode({"membership": "true", "per_page": 20, "simple": "true"})
    status, body = call_gitlab(f"{base}/api/v4/projects?{query}", token)
    if status != 200:
        print(f"GET /projects gagal ({status}): {json.dumps(body, indent=2)}", file=sys.stderr)
        return 1
    if not body:
        print("Tidak ada project yang kamu ikuti.")
        return 0
    for project in body:
        print(f"- {project.get('path_with_namespace')}  ({project.get('visibility')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
