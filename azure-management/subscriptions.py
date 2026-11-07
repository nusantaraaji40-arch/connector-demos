#!/usr/bin/env python3
"""Demo daftar subscription Azure (Azure Resource Manager).

Pola mengikuti dokumentasi Microsoft (learn.microsoft.com):
- Base URL: https://management.azure.com
- Auth: OAuth 2.0, header `Authorization: Bearer <access_token>`.
- Azure Resource Manager TIDAK punya API key. Token didapat dari
  Entra ID, misal lewat Azure CLI:
      az login
      az account get-access-token --query accessToken --output tsv
  lalu isi AZURE_ACCESS_TOKEN dengan token itu (berlaku ~1 jam).
- Scope token: https://management.azure.com/.default
  (atau user_impersonation untuk delegated flow).

Token dibaca dari environment, tidak pernah ditulis di repo.
"""
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_BASE_URL = "https://management.azure.com"
API_VERSION = "2024-01-01"


def main():
    token = os.environ.get("AZURE_ACCESS_TOKEN", "")
    base = os.environ.get("AZURE_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    if not token:
        print("AZURE_ACCESS_TOKEN kosong.", file=sys.stderr)
        print("Dapatkan token: az account get-access-token --query accessToken --output tsv",
              file=sys.stderr)
        return 2
    request = urllib.request.Request(
        f"{base}/subscriptions?api-version={API_VERSION}"
    )
    request.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        print(f"Gagal ({e.code}): {raw}", file=sys.stderr)
        if e.code in (401, 403):
            print("Token kedaluwarsa / kurang izin. Minta token baru lewat Azure CLI.",
                  file=sys.stderr)
        return 1
    items = body.get("value", [])
    if not items:
        print("Tidak ada subscription yang terlihat token ini.")
        return 0
    for sub in items:
        print(f"- {sub.get('displayName')}  ({sub.get('subscriptionId')}, "
              f"{sub.get('state')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
