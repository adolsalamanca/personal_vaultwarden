# Setup

## Requirements

- A machine that stays on and has Docker and Docker Compose. For example: a NAS, a Raspberry Pi 4/5, a mini PC, or a VPS.
- A free Tailscale account. The Personal plan allows up to 6 users.

## 1. Configure Tailscale

Do these steps one time, in the Tailscale web dashboard.

1. Create an account at tailscale.com. Install the app on all your devices.
2. To invite another person, go to **Admin → Users → Invite users**.
3. Go to **Admin → DNS**:
   - Enable **MagicDNS**.
   - Enable **HTTPS Certificates**.
   - Copy your **Tailnet name** (for example, `tail1234ab.ts.net`).
4. Go to **Admin → Settings → Keys → Generate auth key**. Copy the key (`tskey-auth-…`).

## 2. Complete the configuration

In `.env`, replace `tskey-auth-xxxxxxxx` with the key from step 1.4. Replace `tail1234ab.ts.net` with your Tailnet name from step 1.3.

```
TS_AUTHKEY=tskey-auth-xxxxxxxx
TS_HOSTNAME=vault
TAILNET_DOMAIN=tail1234ab.ts.net
UPTIME_KUMA_USER=admin
UPTIME_KUMA_PASSWORD=your_uptime_kuma_password
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
HC_PING_URL=https://hc-ping.com/your-check-uuid
```

For `vaultwarden.env`, generate a hash of the admin panel password:

```bash
docker run --rm -it vaultwarden/server /vaultwarden hash
```

Enter a password. Put the `$argon2id$...` result in single quotes:

```
ADMIN_TOKEN='$argon2id$v=19$m=65540,t=3,p=4$...'
SIGNUPS_ALLOWED=true
WEBSOCKET_ENABLED=true
DOMAIN=https://vault.tail1234ab.ts.net
```

## 3. Start the containers

```bash
mkdir -p tailscale/state vw-data uptime-kuma-data caddy-data
set -a && source .env && set +a && envsubst < tailscale/serve.json.template > tailscale/serve.json
docker compose up -d
docker compose logs -f tailscale
```

Wait until the machine shows as connected. Press Ctrl+C to stop the log output.

Create the Uptime Kuma monitors. You must do this one time only:

```bash
uv run setup-monitors.py
```

When you first open the web UI, Tailscale can need a few seconds to issue the certificate.

## 4. Create the accounts

1. Connect the device to Tailscale. Open `https://vault.<your-tailnet>.ts.net`.
2. Each person creates an account with an email and a **strong master password**. You cannot recover a lost master password.
3. Close registration. Set `SIGNUPS_ALLOWED=false` in `vaultwarden.env`, then run:

   ```bash
   docker compose up -d
   ```

Next: [Usage](usage.md).
