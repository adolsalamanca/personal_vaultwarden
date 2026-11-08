# Backups

## Run a backup

```bash
chmod +x backup.sh
./backup.sh
```

## Run it every day

Add this line with `crontab -e`:

```
30 3 * * * /full/path/to/backup.sh >> /full/path/to/backups/backup.log 2>&1
```

Keep a copy **on a different machine** from time to time, for example on an external drive or in cloud storage. The data is encrypted, but do not share the backup files.

## Restore

1. Run `docker compose down`.
2. Delete `vw-data`.
3. Extract the backup: `tar -xzf backups/vw-data_DATE.tar.gz`.
4. Run `docker compose up -d`.
