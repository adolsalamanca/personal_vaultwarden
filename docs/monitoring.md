# Monitoring

Uptime Kuma is at `http://vault.<your-tailnet>.ts.net:3001`. Any device on your tailnet can open it.

`setup-monitors.py` creates the monitors from `monitors.json`. It creates one monitor for Vaultwarden and one for each container. You do not need to configure monitors manually.

## Alerts

`setup-monitors.py` also configures two types of alert:

- **Service alerts (Telegram through Uptime Kuma).** If Vaultwarden or a container stops, Uptime Kuma sends a Telegram message. This alert needs `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in `.env`.
- **Server alerts (Healthchecks.io to Telegram).** Uptime Kuma sends a ping to Healthchecks.io every 60 seconds. If the server goes offline, the pings stop and Healthchecks.io sends a Telegram alert. This alert needs `HC_PING_URL` in `.env` and Telegram configured in your Healthchecks.io check.

To open the Healthchecks.io dashboard, go to `https://vault.<your-tailnet>.ts.net/alerting`. Caddy redirects this path.
