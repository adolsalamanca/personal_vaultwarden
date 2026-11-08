# Vaultwarden + Tailscale

A self-hosted password manager and uptime monitor for a family. It works with the official Bitwarden apps (Android, iOS, macOS, Windows, Linux, and browser extensions).

- You do not need port forwarding or a domain.
- Tailscale supplies a valid HTTPS certificate for `https://vault.<your-tailnet>.ts.net`.
- Only devices on your Tailscale network can connect.

## Quick start

```bash
mkdir -p tailscale/state vw-data uptime-kuma-data caddy-data
set -a && source .env && set +a && envsubst < tailscale/serve.json.template > tailscale/serve.json
docker compose up -d
uv run setup-monitors.py
```

Complete `.env` and `vaultwarden.env` before you start. The [setup guide](docs/setup.md) gives each step.

## Documentation

| Document | Contents |
|---|---|
| [Architecture](docs/architecture.md) | Containers, request path, and repository files |
| [Setup](docs/setup.md) | Tailscale, configuration, first start, and accounts |
| [Usage](docs/usage.md) | Shared passwords, Bitwarden apps, and account security |
| [Monitoring](docs/monitoring.md) | Uptime Kuma and alerts |
| [Backups](docs/backups.md) | Backup schedule and restore |
| [Updates](docs/updates.md) | Renovate and deployment of image updates |
| [Troubleshooting](docs/troubleshooting.md) | Common problems and fixes |
