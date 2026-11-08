# Troubleshooting

| Symptom | Solution |
|---|---|
| The web UI does not load | Make sure that Tailscale is connected on that device. |
| Certificate error | Make sure that **HTTPS Certificates** is enabled in Admin → DNS. |
| The machine does not show in Tailscale | The auth key expired or was already used. Generate a new key and put it in `.env`. Delete the contents of `tailscale/state/`. Run `docker compose up -d`. |
| An app stops connecting after an update | Run `git pull && docker compose pull && docker compose up -d`. See [Updates](updates.md). |
