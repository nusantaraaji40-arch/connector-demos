# Sumber

Pola tiap demo di repo ini mengikuti dokumentasi resmi dan sampel
open source publik berikut. Kodenya ditulis sendiri (stdlib Python
saja) mengikuti pola URL dan header autentikasi yang didokumentasikan.

## Grok (xAI) — docs.x.ai

- Autentikasi: `Authorization: Bearer <xAI API key>`, base `https://api.x.ai/v1`.
- Key dibuat di console.x.ai -> API Keys, setelah membeli kredit prepaid.
- Endpoint verifikasi: `GET /v1/models`, `GET /v1/me`.

## Cursor — docs.cursor.com

- Cloud Agents API menerima `Authorization: Bearer <key>`,
  Admin API menerima Basic auth (key sebagai username).
- Key dibuat di cursor.com/dashboard -> API Keys, scope `admin:*`.
- Endpoint: `GET /v1/me`, `GET /v1/agents`.

## GitLab — docs.gitlab.com

- REST API v4 di `gitlab.com/api/v4`, auth header `PRIVATE-TOKEN`.
- Endpoint: `GET /user`, `GET /projects?membership=true`.
- Token fine-grained butuh User: Read + Project: Read.

## Gitea — docs.gitea.com

- API v1 di `gitea.com/api/v1`, auth `Authorization: token <token>`.
- Token dibuat di Settings -> Applications -> Manage Access Tokens.

## Codeberg — codeberg.org (Forgejo)

- API sama dengan Gitea, di `codeberg.org/api/v1`.
- Versi server terkonfirmasi: Forgejo `16.0.0-dev`.

## SourceForge — sourceforge.net (Allura)

- REST API di `sourceforge.net/rest/`, endpoint proyek
  `GET /rest/p/<project>/`, profil `GET /rest/u/<username>/profile`.
- Bearer token dibuat di `sourceforge.net/auth/oauth/`.
- Pesan server: jangan pakai token di URL, pakai header
  `Authorization: Bearer`.

## Azure Management — learn.microsoft.com

- Azure Resource Manager di `management.azure.com`, auth OAuth 2.0
  Bearer dari Entra ID, scope `https://management.azure.com/.default`.
- Token via Azure CLI: `az account get-access-token`.
- Endpoint: `GET /subscriptions?api-version=2024-01-01`.

## Azure OpenAI — repo terpisah

- Demo lengkap di repo `azure-openai-api-key-demo`.
- Auth header `api-key`, URL deployment-based (lihat SOURCES.md di sana).
