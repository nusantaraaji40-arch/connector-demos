#!/usr/bin/env python3
"""Demo baca project dan profil SourceForge (Allura REST API).

Pola mengikuti dokumentasi SourceForge:
- Base URL: https://sourceforge.net/rest
- Project publik bisa dibaca tanpa auth: GET /rest/p/<project>/
- Profil pengguna: GET /rest/u/<username>/profile
- Auth (bila ada): header `Authorization: Bearer <token>`.
  Bearer token dibuat di sourceforge.net/auth/oauth/
  (tombol Generate Bearer Token). JANGAN taruh token di URL —
  server menolaknya secara eksplisit.
- Allura tidak punya endpoint "me" tanpa username.

Token dibaca dari environment, tidak pernah ditulis di repo.
"""
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_BASE_URL = "https://sourceforge.net"


def call_sf(path, token=None):
    request = urllib.request.Request(path)
    if token:
        request.add_header("Authorization", "Bearer " + token)
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
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    project = args[0] if args else "forge"
    username = args[1] if len(args) > 1 else None
    token = os.environ.get("SOURCEFORGE_TOKEN", "")
    base = os.environ.get("SOURCEFORGE_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    status, body = call_sf(f"{base}/rest/p/{project}/", token or None)
    if status != 200:
        print(f"GET /rest/p/{project}/ gagal ({status}): {json.dumps(body, indent=2)}",
              file=sys.stderr)
        return 1
    print(f"Project: {body.get('shortname')} — {body.get('name')}")
    if username:
        status, body = call_sf(f"{base}/rest/u/{username}/profile", token or None)
        if status != 200:
            print(f"GET /rest/u/{username}/profile gagal ({status}): "
                  f"{json.dumps(body, indent=2)}", file=sys.stderr)
            return 1
        print(f"Pengguna: {body.get('username')} (id: {body.get('id')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
