#!/bin/sh

SOURCE_FILE="/opt/postgres/pg_hba.conf"
#TARGET_FILE="/var/postgresql/data/pg_hba.conf"
TARGET_FILE="/var/lib/postgresql/data/pg_hba.conf"

ls "/opt/postgres"
cat "$SOURCE_FILE"
# Check if the symlink already exists
if [ -L "$TARGET_FILE" ]; then
  echo "Symlink already exists, no action needed."
else
  # Check if the target file already exists
  if [ -e "$TARGET_FILE" ]; then
    # Delete the existing file
    rm "$TARGET_FILE"
    echo "Existing file pg_hba.conf deleted."
  fi

  # Create the symlink
  cp "$SOURCE_FILE" "$TARGET_FILE"
  echo "Symlink for pg_hba.conf created."
fi