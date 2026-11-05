
#!/bin/bash

# Database information
CONTAINER="mysql_db"
DB="mysql_db"

# Backup directory
BACKUP_DIR="$HOME/student_lab/mysql_backups"

# Date and time
DATE=$(date +"%Y-%m-%d_%H-%M-%S")

# Backup file
BACKUP_FILE="$BACKUP_DIR/${DB}_${DATE}.sql"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Check container
if ! docker inspect -f '{{.State.Running}}' "$CONTAINER" 2>/dev/null | grep -q true; then
    echo "ERROR: MySQL container is not running!"
    exit 1
fi

# Backup database
if docker exec "$CONTAINER" sh -c \
  'exec mysqldump -u root -p"$MYSQL_ROOT_PASSWORD" --single-transaction "$1"' \
  sh "$DB" > "$BACKUP_FILE" && [ -s "$BACKUP_FILE" ]; then

    echo "Backup successfully completed!"
    ls -lh "$BACKUP_FILE"

else
    echo "Backup failed!"
    rm -f "$BACKUP_FILE"
    exit 1
fi
