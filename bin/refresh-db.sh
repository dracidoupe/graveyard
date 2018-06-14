#!/bin/bash

# Download production database to localhost for testing migration.
# 
# **************************************************************** 
# THIS WILL DROP YOUR LOCAL DATABASE AND THROW AWAY ANY CHANGES!!!
# ****************************************************************
# 
# This assumes:
#   * You have whole-disk encryption on localhost in order to protect user's data
#   * Requirements are set up correctly and you are authorized to read application password
#   * You have username/password in .my.cnf for current local user in order to be able to feed data into db locally

set -e

curdir=`pwd`
encryption_key=`makepasswd --chars=99`

host=${DEPLOYMENT_HOST:-"revy"}
user=${DEPLOYMENT_USERNAME:-"w-dracidoupe-cz"}

mysql_user="dracidoupe_cz"
mysql_db="dracidoupe_cz"
mysql_password_file="/var/www/dracidoupe.cz/dbconf/dbpasswd"
backup_file="/tmp/ddcz-bak.gpg"
backup_file_clear="/tmp/ddcz-bak"

machine="$user@$host"

ssh $machine bash -c "'
    if [ -f $backup_file ]; then rm $backup_file; fi && \
    mysqldump --single-transaction --add-drop-database -u $mysql_user --password=\$(cat $mysql_password_file) --databases $mysql_db | gpg -c --cipher-algo AES256 --passphrase=$encryption_key > $backup_file
'"

rsync -avz $machine:$backup_file $backup_file
ssh $machine rm $backup_file

echo $encryption_key | gpg -d --passphrase-fd=0 --batch --yes -o $backup_file_clear $backup_file 
rm $backup_file 

mysql $mysql_db < $backup_file_clear

rm $backup_file_clear

