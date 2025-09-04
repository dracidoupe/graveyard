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
# Determine schema name: prefer 'dracidoupe_cz' if present in dump, otherwise fallback to 'public'.
# Allow override via SCHEMA_NAME env var.
if [[ -z "${SCHEMA_NAME}" ]]; then
  # Detect schema by checking if 'dracidoupe_cz' exists after restore
  if psql -U $POSTGRES_USER -d $LOCAL_DB_NAME -tAc "SELECT 1 FROM pg_namespace WHERE nspname='dracidoupe_cz'" | grep -q 1; then
    SCHEMA_NAME=dracidoupe_cz
  else
    SCHEMA_NAME=public
  fi
fi

echo "🔐 Granting permissions on schema '$SCHEMA_NAME' to user '$LOCAL_DB_USER'..."
psql -U $POSTGRES_USER -d $LOCAL_DB_NAME -v ON_ERROR_STOP=1 -c "
-- Grant usage and create on the schema for application user
GRANT USAGE, CREATE ON SCHEMA \"$SCHEMA_NAME\" TO \"$LOCAL_DB_USER\";

-- Grant permissions on all existing tables in the schema
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA \"$SCHEMA_NAME\" TO \"$LOCAL_DB_USER\";

-- Grant permissions on all sequences (for auto-increment fields)
GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA \"$SCHEMA_NAME\" TO \"$LOCAL_DB_USER\";

-- Grant permissions on future tables and sequences
ALTER DEFAULT PRIVILEGES IN SCHEMA \"$SCHEMA_NAME\" GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO \"$LOCAL_DB_USER\";
ALTER DEFAULT PRIVILEGES IN SCHEMA \"$SCHEMA_NAME\" GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO \"$LOCAL_DB_USER\";
"

# Ensure the role executing migrations also has necessary privileges
echo "🔑 Adding additional permissions for CURRENT_USER on schema '$SCHEMA_NAME'..."
psql -U $POSTGRES_USER -d $LOCAL_DB_NAME -v ON_ERROR_STOP=1 -c "
-- Grant schema permissions to current role
GRANT USAGE, CREATE ON SCHEMA \"$SCHEMA_NAME\" TO CURRENT_USER;

-- Grant privileges on all existing sequences in the schema to current role
GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA \"$SCHEMA_NAME\" TO CURRENT_USER;

-- Grant permissions for future sequences
ALTER DEFAULT PRIVILEGES IN SCHEMA \"$SCHEMA_NAME\" GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO CURRENT_USER;
"

# Optional: Change ownership of objects in the schema to LOCAL_DB_USER so migrations can ALTER OWNERSHIP/OWNED BY
# This avoids errors like 'must be able to SET ROLE "<owner>"'
echo "🧰 Reassigning ownership of objects in schema '$SCHEMA_NAME' to '$LOCAL_DB_USER' (best-effort)..."
psql -U $POSTGRES_USER -d $LOCAL_DB_NAME -v ON_ERROR_STOP=0 <<'SQL'
DO $$
DECLARE
    obj RECORD;
BEGIN
    -- Tables
    FOR obj IN
        SELECT c.relname AS name
        FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE n.nspname = current_schema() AND c.relkind = 'r'
    LOOP
        EXECUTE format('ALTER TABLE IF EXISTS %I.%I OWNER TO %I', '$SCHEMA_NAME', obj.name, '$LOCAL_DB_USER');
    END LOOP;

    -- Sequences
    FOR obj IN
        SELECT c.relname AS name
        FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE n.nspname = current_schema() AND c.relkind = 'S'
    LOOP
        EXECUTE format('ALTER SEQUENCE IF EXISTS %I.%I OWNER TO %I', '$SCHEMA_NAME', obj.name, '$LOCAL_DB_USER');
    END LOOP;
END$$;
SQL

# Set search_path for role and database so Django sees the restored schema first
if [[ "$SCHEMA_NAME" != "public" ]]; then
  echo "🧭 Setting search_path to '$SCHEMA_NAME,public' for role '$LOCAL_DB_USER' and database '$LOCAL_DB_NAME'..."
  psql -U $POSTGRES_USER -d $LOCAL_DB_NAME -v ON_ERROR_STOP=1 -c "ALTER ROLE \"$LOCAL_DB_USER\" IN DATABASE \"$LOCAL_DB_NAME\" SET search_path TO '$SCHEMA_NAME,public';" || true
  psql -U $POSTGRES_USER -d $LOCAL_DB_NAME -v ON_ERROR_STOP=1 -c "ALTER DATABASE \"$LOCAL_DB_NAME\" SET search_path TO '$SCHEMA_NAME,public';" || true
fi

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
