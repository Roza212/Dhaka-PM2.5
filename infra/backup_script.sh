#!/bin/bash
# Automated Backup Script for PostgreSQL Database & STGCN Models
# Execute via CRON: 0 2 * * * /path/to/backup_script.sh

set -e

BACKUP_DIR="/tmp/db_backups"
DATE=$(date +"%Y%m%d_%H%M%S")
DB_NAME="dhaka_pm25"
S3_BUCKET="s3://dhaka-pm25-secure-backups/"

mkdir -p $BACKUP_DIR

echo "Starting Database Dump..."
# pg_dump requires PGPASSWORD to be set in environment securely
pg_dump -U admin -F c $DB_NAME > $BACKUP_DIR/db_backup_$DATE.dump

echo "Encrypting Backup with AES-256..."
# Database Encryption Strategy: AES-256-CBC at rest before moving to cloud
openssl enc -aes-256-cbc -salt -in $BACKUP_DIR/db_backup_$DATE.dump -out $BACKUP_DIR/db_backup_$DATE.dump.enc -pass pass:$BACKUP_ENCRYPTION_KEY

echo "Syncing to Secure S3 Bucket..."
aws s3 cp $BACKUP_DIR/db_backup_$DATE.dump.enc $S3_BUCKET

echo "Cleaning up local unencrypted dump..."
rm $BACKUP_DIR/db_backup_$DATE.dump

echo "Backup complete at $DATE"
