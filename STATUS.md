# Hasil screening konektor (2026-11-07)

Status ini dicatat apa adanya dari tes baca pertama tiap konektor.
"Belum terverifikasi" bukan berarti layanan jelek — artinya bukti
tesnya belum lolos, dan penyebabnya ditulis supaya tidak ditebak.

## Grok (xAI) — `custom.grok`

- Konektor didaftarkan, kartu API key dikirim ulang 2026-11-07.
- **Belum dites**: key belum diisi, jadi belum ada panggilan terautentikasi.
- Auth: `Authorization: Bearer <key>` ke `https://api.x.ai/v1`.
- Tes yang akan dilakukan: `GET /v1/models`, lalu satu chat completion.
- Biaya: per token dari kredit prepaid, tanpa free tier.

## Cursor — `custom.cursor`

- Key **diterima** Cursor (bukan 401), tapi `GET /v1/me` dan
  `GET /v1/agents` balik **403 `plan_required`**: Cloud Agent tidak
  tersedia untuk pengguna gratis, harus upgrade ke Pro (berbayar).
- Admin API (`/teams/members`) balik 403 `permission_denied` —
  butuh Basic auth, bukan Bearer, di luar cakupan konektor ini.
- Cursor tidak menyediakan key read-only; key yang sama bisa
  meluncurkan Cloud Agents yang membuat branch dan PR.

## GitLab — `custom.gitlab`, `custom.gitlab2`, `custom.gitlab3`

- Akun 1: token sampai ke GitLab tapi ditolak **403
  `insufficient_granular_scope`** — `GET /user` butuh izin
  fine-grained User: Read, `GET /projects` butuh Project: Read.
- Akun 2 dan 3: **401 Unauthorized** untuk `/user` dan `/projects`
  padahal request terbukti membawa kredensial — nilai token
  salah / terpotong / dicabut / kedaluwarsa.
- Perbaikan: akun 1 tambah scope lalu reconnect; akun 2 dan 3
  reconnect dengan token baru yang lengkap.

## Gitea — `custom.gitea`

- `GET /user` ke `gitea.com/api/v1` balik 401 untuk varian header
  `token `, `Bearer`, maupun telanjang.
- **Koreksi penyebab** (dari bukti Codeberg): error Codeberg
  mengutip balik surrogate literal sebagai token yang diterima
  server — jadi header `token ` + surrogate kemungkinan tidak
  ditukar ke token asli saat egress. 401 ini kemungkinan besar
  penyebabnya mekanisme, **bukan** vonis nilai token salah.
- Demo di repo ini memakai token asli dari environment, jadi
  pola headernya benar saat dijalankan langsung oleh pemilik token.

## Codeberg — `custom.codeberg`

- `GET /user` ke `codeberg.org/api/v1` balik 401 dan badan error
  mengutip balik surrogate literal `hsurr:...` sebagai token yang
  diterima ("access token does not exist [sha: hsurr:...]") —
  bukti token asli tidak pernah sampai ke Codeberg.
- **Tidak boleh disimpulkan nilai tokennya salah** dari hasil ini.
- Perbaikan: daftar ulang dengan placement yang didukung swap
  (mis. token sebagai query param, atau OAuth Bearer), lalu tes ulang.

## SourceForge — `custom.sourceforge`

- Baca anonim `GET /rest/p/forge/` balik **200** — API Allura jalan.
- Baca terautentikasi dengan Bearer token tersimpan balik **401**;
  tes query param `access_token` juga 401 dan pesannya tegas:
  pakai header `Authorization: Bearer`, jangan token di URL.
- Kesimpulan: placement sudah benar, nilai token yang ditolak
  (salah / kedaluwarsa / dicabut, atau yang ditempel bukan bearer
  token melainkan consumer key/secret).
- Perbaikan: buat bearer token baru di
  `sourceforge.net/auth/oauth/` (Generate Bearer Token), reconnect.

## Azure Management — `custom.azure`

- Didaftarkan via OAuth 2.0 (Entra ID), scope
  `https://management.azure.com/user_impersonation offline_access`.
- **Belum dites**: menunggu user mendaftarkan aplikasi di Entra ID
  (redirect URI `https://agent.meta.ai/api/hatch/oauth/callback`),
  membuat client secret, dan menyelesaikan consent.
- Azure Resource Manager tidak punya API key — hanya OAuth 2.0.

## Azure OpenAI — repo terpisah

- Demo lengkap di repo `azure-openai-api-key-demo` (publik).
- Auth: header `api-key` ke endpoint resource sendiri.
- Diuji lokal dengan server mock: URL, header, dan body terverifikasi.
