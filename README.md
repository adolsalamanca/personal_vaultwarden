# Vaultwarden + Tailscale

Self-hosted password manager for a family, compatible with official Bitwarden apps (Android, iOS, macOS, Windows, Linux, and browser extensions).

- No port forwarding or domain purchase required.
- Automatic valid HTTPS at `https://vault.<your-tailnet>.ts.net`.
- Only accessible from devices connected to your Tailscale network.

## What's in this repo

| File | Purpose |
|---|---|
| `docker-compose.yml` | Defines the two containers (Tailscale + Vaultwarden) |
| `.env` | Tailscale key and network name. **Must be filled in. Never commit this.** |
| `vaultwarden.env` | Vaultwarden settings (registration, admin panel). **Must be filled in. Never commit this.** |
| `tailscale/serve.json.template` | Template for the Tailscale HTTPS proxy config. Generated into `serve.json` at setup. |
| `backup.sh` | Daily backup script |

## Requirements

- A machine that stays on with Docker and Docker Compose: NAS, Raspberry Pi 4/5, mini PC, or VPS.
- A free Tailscale account (Personal plan: up to 6 users).

## 1. Set up Tailscale (once, in the web dashboard)

1. Create an account at tailscale.com and install the app on all your devices.
2. To invite your partner: **Admin → Users → Invite users**.
3. **Admin → DNS**:
   - Enable **MagicDNS**.
   - Enable **HTTPS Certificates**.
   - Copy your **Tailnet name** (e.g. `tail1234ab.ts.net`).
4. **Admin → Settings → Keys → Generate auth key**. Copy the key (`tskey-auth-…`).

## 2. Fill in the configuration

In `.env` (replace `tskey-auth-xxxxxxxx` with the key from step 1.4, and `tail1234ab.ts.net` with your Tailnet name from step 1.3):

```
TS_AUTHKEY=tskey-auth-xxxxxxxx
TS_HOSTNAME=vault
TAILNET_DOMAIN=tail1234ab.ts.net
```

In `vaultwarden.env`, generate the admin panel password hash:

```bash
docker run --rm -it vaultwarden/server /vaultwarden hash
```

Enter a password and paste the resulting `$argon2id$...` string in single quotes:

```
ADMIN_TOKEN='$argon2id$v=19$m=65540,t=3,p=4$...'
SIGNUPS_ALLOWED=true
WEBSOCKET_ENABLED=true
DOMAIN=https://vault.tail1234ab.ts.net
```

## 3. Start

```bash
mkdir -p tailscale/state vw-data
set -a && source .env && set +a && envsubst < tailscale/serve.json.template > tailscale/serve.json
docker compose up -d
docker compose logs -f tailscale   # wait until the machine appears as connected; Ctrl+C to exit
```

The first time you open the web UI, Tailscale may take a few seconds to issue the certificate.

## 4. Create your accounts

1. With Tailscale active, open `https://vault.<your-tailnet>.ts.net`.
2. Each person creates their account with their email and a **strong master password** (cannot be recovered if lost).
3. **Close registration**: set `SIGNUPS_ALLOWED=false` in `vaultwarden.env` and run:

   ```bash
   docker compose up -d
   ```

## 5. Share passwords

1. In the web UI: **New organization** (e.g. "Home").
2. Invite the other person by email from **Members**. If SMTP is not configured, confirm the invitation from the admin panel at `https://vault.<your-tailnet>.ts.net/admin`.
3. Create collections ("Streaming", "Banking", "WiFi"…) and move shared items there. Everything outside the organization remains private.

## 6. Connect the official Bitwarden apps

On the login screen of any app or extension:

1. Server selector → **Self-hosted**.
2. Server URL: `https://vault.<your-tailnet>.ts.net`
3. Log in with your email and master password.

On mobile, keep **Tailscale always connected** so the app can sync.

## 7. Recommended

- **2FA for your vault**: Settings → Security → Two-step login. A stolen master password alone cannot open the vault without the second factor.
- **Emergency access** between the two of you: Settings → Emergency access. This lets your partner request read access to your vault if you are unavailable, after a waiting period you define.

## 8. Backups

```bash
chmod +x backup.sh
./backup.sh
```

To run it daily, add via `crontab -e`:

```
30 3 * * * /full/path/to/backup.sh >> /full/path/to/backups/backup.log 2>&1
```

Keep an occasional copy **off this machine** (external drive or cloud). The data is encrypted, but don't share those files.

**Restore**: `docker compose down`, delete `vw-data`, extract the backup (`tar -xzf backups/vw-data_DATE.tar.gz`), then `docker compose up -d`.

## 9. Updating (once a month)

Images are pinned by digest in `docker-compose.yml`, so `docker compose pull` alone will not fetch updates. The process:

1. Check for new releases: [vaultwarden](https://github.com/dani-garcia/vaultwarden/releases) and [Tailscale](https://github.com/tailscale/tailscale/releases).
2. Pull the new image and get its digest:
   ```bash
   docker pull vaultwarden/server:NEW_VERSION
   docker inspect vaultwarden/server:NEW_VERSION --format '{{index .RepoDigests 0}}'
   ```
3. Update the `image:` lines in `docker-compose.yml` with the new version tag and digest.
4. Apply:
   ```bash
   docker compose up -d
   ```

Bitwarden apps update themselves and sometimes require a recent Vaultwarden version. If an app stops connecting, update first.

## Troubleshooting

| Symptom | Solution |
|---|---|
| Web UI doesn't load | Is Tailscale connected on that device? |
| Certificate error | Check that **HTTPS Certificates** is enabled in Admin → DNS |
| Machine doesn't appear in Tailscale | Auth key expired or already used: generate a new one, put it in `.env`, clear `tailscale/state/`, and run `docker compose up -d` |
| App stops connecting after an update | `docker compose pull && docker compose up -d` |
