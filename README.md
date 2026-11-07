# connector-demos

Kumpulan demo kecil untuk setiap konektor yang baru tersambung ke Muse —
dirakit sendiri dari dokumentasi resmi dan sampel open source publik.
Satu demo per layanan, satu file Python, tanpa dependency di luar
standard library.

Repo ini dibuat dari hasil **screening konektor**: tiap demo disertai
status verifikasi jujur di `STATUS.md` — mana yang sudah terbukti jalan,
mana yang ketahan paket gratis / scope / token.

## Daftar demo

| Demo | Layanan | Auth | Jalankan |
|---|---|---|---|
| `grok/chat.py` | Grok (xAI) | API key, `Authorization: Bearer` | `python3 grok/chat.py "halo"` |
| `cursor/agents.py` | Cursor Cloud Agents | API key, `Authorization: Bearer` | `python3 cursor/agents.py` |
| `gitlab/projects.py` | GitLab | `PRIVATE-TOKEN` | `python3 gitlab/projects.py` |
| `gitea/me.py` | Gitea | `Authorization: token` | `python3 gitea/me.py` |
| `codeberg/me.py` | Codeberg (Forgejo) | `Authorization: token` | `python3 codeberg/me.py` |
| `sourceforge/project.py` | SourceForge (Allura) | `Authorization: Bearer` | `python3 sourceforge/project.py` |
| `azure-management/subscriptions.py` | Azure Resource Manager | OAuth 2.0 Bearer | `python3 azure-management/subscriptions.py` |
| [azure-openai-api-key-demo](https://github.com/nusantaraaji40-arch/azure-openai-api-key-demo) | Azure OpenAI | header `api-key` | repo terpisah |

## Cara pakai

```bash
cp .env.example .env
# isi .env hanya dengan key/token milikmu sendiri
python3 grok/chat.py --list-models
python3 gitlab/projects.py
```

Tiap demo membaca konfigurasinya dari environment (lihat `.env.example`).
Untuk pengetesan lokal, tiap demo juga menerima override base URL,
misal `GROK_BASE_URL=http://127.0.0.1:8766`.

## Keamanan

- **Jangan pernah commit file `.env`, key, atau token ke repo.**
  `.env` sudah masuk `.gitignore`. Semua kredensial hanya dibaca dari
  environment.
- Key/token yang pernah tampil di chat atau ter-commit harus dirotasi
  di layanan masing-masing.
- Demo-demo ini hanya **membaca** (list / me / chat sekali). Tidak ada
  yang membuat, menghapus, atau mengubah resource — kecuali Grok dan
  Azure OpenAI yang memakai token berbayar tiap pemanggilan model.

## Biaya

- Grok (xAI) dan Azure OpenAI: **berbayar per token, tanpa free tier**.
- Cursor Cloud Agents: **butuh paket Pro**; akun gratis ditolak
  `plan_required` (lihat `STATUS.md`).
- GitLab, Gitea, Codeberg, SourceForge, Azure Management: API-nya
  gratis, tapi resource Azure-nya sendiri berbayar pay-as-you-go.

## Sumber

Lihat `SOURCES.md` untuk dokumen dan repo publik yang dipakai sebagai acuan.
Lihat `STATUS.md` untuk hasil screening tiap konektor.

## Lisensi

MIT — lihat `LICENSE`.
