# Architecture

## Containers

`docker-compose.yaml` defines four containers. Caddy, Vaultwarden, and Uptime Kuma use the network of the Tailscale container (`network_mode: service:tailscale`). They connect to each other through `localhost`.

| Container | Purpose |
|---|---|
| `tailscale` | Connects the server to your tailnet and terminates HTTPS |
| `caddy` | Reverse proxy in front of Vaultwarden |
| `vaultwarden` | Bitwarden-compatible password server |
| `uptime-kuma` | Monitors the containers and sends alerts |

## Request path

```
https://vault.<your-tailnet>.ts.net:443  →  Tailscale (HTTPS)  →  Caddy :80  →  Vaultwarden :8080
```

Caddy has two routes:

- `/alerting` redirects to the Healthchecks.io dashboard.
- All other paths go to Vaultwarden.

Caddy does not manage certificates. Tailscale supplies them.

## Repository files

| File | Purpose |
|---|---|
| `docker-compose.yaml` | Defines the four containers |
| `Caddyfile` | Caddy routes |
| `.env` | Tailscale key, tailnet name, and alert settings. **You must complete it. Never commit it.** |
| `vaultwarden.env` | Vaultwarden settings (registration, admin panel). **You must complete it. Never commit it.** |
| `tailscale/serve.json.template` | Template for the Tailscale HTTPS proxy configuration. The setup generates `serve.json` from it. |
| `monitors.json` | Uptime Kuma monitor definitions |
| `setup-monitors.py` | Creates the monitors and alerts in Uptime Kuma |
| `backup.sh` | Backup script |
| `vaultwarden.service` | systemd unit: updates and starts the containers at boot |
| `vaultwarden-update.service`, `vaultwarden-update.timer` | systemd units: restart `vaultwarden.service` every Monday |
| `renovate.json` | Renovate configuration |
| `.github/workflows/renovate.yaml` | Weekly Renovate run |
