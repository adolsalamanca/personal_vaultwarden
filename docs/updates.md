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

A merge changes only the repository. The containers on the server keep the old images until you run:

```bash
git pull
docker compose pull
docker compose up -d
```

The Bitwarden apps update themselves. Some app versions need a recent Vaultwarden version. If an app stops connecting, deploy the latest updates first.
