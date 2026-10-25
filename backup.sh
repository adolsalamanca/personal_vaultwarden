#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR="$SCRIPT_DIR/backups"
DATE=$(date +%Y-%m-%d_%H%M%S)

mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/vw-data_$DATE.tar.gz" -C "$SCRIPT_DIR" vw-data
echo "Backup created: $BACKUP_DIR/vw-data_$DATE.tar.gz"

# Keep last 30 backups
find "$BACKUP_DIR" -name "vw-data_*.tar.gz" -type f | sort | head -n -30 | xargs -r rm --
