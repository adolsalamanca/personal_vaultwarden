# Usage

## Share passwords

1. In the web UI, select **New organization** (for example, "Home").
2. In **Members**, invite the other person by email. If SMTP is not configured, confirm the invitation in the admin panel at `https://vault.<your-tailnet>.ts.net/admin`.
3. Create collections ("Streaming", "Banking", "WiFi", and others). Move the shared items into them. Items outside the organization stay private.

## Connect the official Bitwarden apps

On the login screen of an app or browser extension:

1. In the server selector, select **Self-hosted**.
2. Enter the server URL: `https://vault.<your-tailnet>.ts.net`
3. Enter your email and master password.

On mobile devices, keep **Tailscale always connected**. The app cannot sync without it.

## Recommended settings

- **Two-step login**: go to Settings → Security → Two-step login. With it, a stolen master password alone cannot open the vault.
- **Emergency access**: go to Settings → Emergency access. The other person can then request read access to your vault if you are not available. Access starts after a waiting period that you set.
