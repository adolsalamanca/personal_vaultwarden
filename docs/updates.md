# Updates

`docker-compose.yaml` pins each image as `name:tag@sha256:digest`. `docker compose pull` alone does not get new versions. Renovate updates the tags and digests.

## Renovate

`.github/workflows/renovate.yaml` runs Renovate every Monday at 05:17 UTC. To start a run manually:

```bash
gh workflow run renovate.yaml -f log_level=debug
```

`renovate.json` sets these rules:

- Renovate updates the Docker images and the GitHub Actions pins.
- Renovate waits 7 days after a release before it proposes the update.
- Renovate merges minor and patch updates automatically. This repository has no CI, so no tests run before the merge.
- Renovate opens a pull request for each major update. You must review and merge it manually. Read the release notes first, for example for the update to Uptime Kuma 2.

The workflow uses a GitHub App token. The `renovate` environment holds the App credentials, and only runs on `main` can read them:

| Name | Type |
|---|---|
| `RENOVATE_APP_CLIENT_ID` | Environment variable |
| `RENOVATE_APP_PRIVATE_KEY` | Environment secret |

## Deploy an update

A merge changes only the repository. The containers on the server keep the old images until these commands run:

```bash
git pull
docker compose pull
docker compose up -d
```

`vaultwarden.service` runs them at each start. `vaultwarden-update.timer` restarts the service every Monday at 08:13 local time, after the Renovate run. To deploy at a different time, run `sudo systemctl restart vaultwarden`.

To install the units:

```bash
sudo cp vaultwarden.service vaultwarden-update.service vaultwarden-update.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now vaultwarden-update.timer
``` If `git pull` or `docker compose pull` fails, the service starts the containers with the current images.

The Bitwarden apps update themselves. Some app versions need a recent Vaultwarden version. If an app stops connecting, deploy the latest updates first.
