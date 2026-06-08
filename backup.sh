#!/bin/bash

# Backup script for Django LMS
set -e

BACKUP_DIR="/home/ubuntu/backups"
DATE=$(date +"%Y%m%d_%H%M%S")
PROJECT_DIR="/home/ubuntu/online-learning-system"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Load environment variables
source $PROJECT_DIR/.env

echo "Starting backup at $DATE"

# Backup MySQL database
if [ "$DB_ENGINE" = "django.db.backends.mysql" ]; then
    echo "Backing up MySQL database..."
    mysqldump -u $DB_USER -p$DB_PASSWORD -h $DB_HOST -P $DB_PORT $DB_NAME | gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz
fi

# Backup PostgreSQL database
if [ "$DB_ENGINE" = "django.db.backends.postgresql" ]; then
    echo "Backing up PostgreSQL database..."
    pg_dump -U $DB_USER -h $DB_HOST -p $DB_PORT $DB_NAME | gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz
fi

# Backup media files
echo "Backing up media files..."
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz -C $PROJECT_DIR/backend media

# Backup static files (optional)
echo "Backing up static files..."
tar -czf $BACKUP_DIR/static_backup_$DATE.tar.gz -C $PROJECT_DIR staticfiles

# Clean up old backups (keep last 7 days)
echo "Cleaning up old backups..."
find $BACKUP_DIR -type f -name "*.gz" -mtime +7 -delete

echo "Backup completed successfully!"
