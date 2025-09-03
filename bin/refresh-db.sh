#!/bin/bash

# Script to download Heroku PostgreSQL backup and restore to local database
# Usage: ./restore_heroku_backup.sh [--nokeep]
#   --nokeep: Keep the backup file after restore (don't delete from /tmp)

set -e  # Exit on any error

# Parse command line arguments
KEEP_FILE=true
while [[ $# -gt 0 ]]; do
    case $1 in
        --nokeep)
            KEEP_FILE=false
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [--nokeep]"
            echo "  --nokeep    Keep the backup file after restore (don't delete)"
            echo "  -h, --help  Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

# Configuration
APP_NAME="${HEROKU_APP_NAME:-dracidoupe}"
LOCAL_DB_NAME="${LOCAL_DB_NAME:-dracidoupe_cz}"
LOCAL_DB_USER="${LOCAL_DB_USER:-ddcz}"
POSTGRES_USER="${POSTGRES_USER:-postgres}"

# Generate date-based filename
DATE_SUFFIX=$(date +%Y%m%d)
BACKUP_FILE="/tmp/ddcz_backup_${DATE_SUFFIX}.dump"

echo "Starting Heroku PostgreSQL backup download and restore process..."
echo "📋 Configuration:"
echo "   App: $APP_NAME"
echo "   Local DB: $LOCAL_DB_NAME"
echo "   Local User: $LOCAL_DB_USER"
echo "   Backup file: $BACKUP_FILE"
echo "   Keep file: $KEEP_FILE"
echo ""

# Step 1: Check if today's backup already exists
if [[ -f "$BACKUP_FILE" ]]; then
    echo "📁 Found existing backup file for today: $BACKUP_FILE"
    echo "   File size: $(du -h "$BACKUP_FILE" | cut -f1)"
    echo "   Skipping download..."
else
    # Step 2: Download the latest backup
    echo "⬇️  Downloading backup from Heroku..."
    heroku pg:backups:download -a $APP_NAME -o $BACKUP_FILE
    echo "   Downloaded: $(du -h "$BACKUP_FILE" | cut -f1)"
fi

# Step 3: Drop existing local database (if it exists)
echo "🗑️  Dropping existing local database '$LOCAL_DB_NAME'..."
dropdb --if-exists $LOCAL_DB_NAME

# Step 4: Create new local database
echo "🆕 Creating new local database '$LOCAL_DB_NAME'..."
createdb $LOCAL_DB_NAME

# Step 5: Restore backup to local database
echo "🔄 Restoring backup to local database..."
pg_restore --verbose --no-acl --no-owner -h localhost -d $LOCAL_DB_NAME $BACKUP_FILE

# Step 6: Grant permissions to local user
echo "🔐 Granting permissions to user '$LOCAL_DB_USER'..."
psql -U $POSTGRES_USER -d $LOCAL_DB_NAME -c "
-- Grant usage permission on the schema
GRANT USAGE ON SCHEMA $LOCAL_DB_NAME TO $LOCAL_DB_USER;

-- Grant permissions on all existing tables in the schema
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA $LOCAL_DB_NAME TO $LOCAL_DB_USER;

-- Grant permissions on all sequences (for auto-increment fields)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA $LOCAL_DB_NAME TO $LOCAL_DB_USER;

-- Grant permissions on future tables and sequences
ALTER DEFAULT PRIVILEGES IN SCHEMA $LOCAL_DB_NAME GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO $LOCAL_DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA $LOCAL_DB_NAME GRANT USAGE, SELECT ON SEQUENCES TO $LOCAL_DB_USER;
"

# Step 7: Conditional cleanup of backup file
if [[ "$KEEP_FILE" == "true" ]]; then
    echo "💾 Keeping backup file as requested: $BACKUP_FILE"
else
    echo "🧹 Cleaning up backup file..."
    rm -f $BACKUP_FILE
fi

echo ""
echo "✅ Restore completed successfully!"
echo "Local database '$LOCAL_DB_NAME' has been updated with data from Heroku app '$APP_NAME'"
echo "User '$LOCAL_DB_USER' has been granted appropriate permissions"

if [[ "$KEEP_FILE" == "true" ]]; then
    echo "📁 Backup file preserved at: $BACKUP_FILE"
fi
