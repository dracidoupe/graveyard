#!/bin/bash

# Declarative terraform/Puppet/whatever nicities may happen once we are on
# a system from this decade
# Until then, shell rulez. '60s still roll!

# This assumes:
# * You have reasonably set up ssh-agent and you are in authorized_keys2
# * You are running this from repo root
# * Deployment server is configured in a magical way that works
# * Incremental deploys are fragile given current setup and will not be used...so...no deploys over GPRS from your phone, sorry. 
# * bash & rsync installed
set -e

curdir=`pwd`

host=${DEPLOYMENT_HOST:-"revy"}
user=${DEPLOYMENT_USERNAME:-"w-dracidoupe-cz"}

remote_root=${DEPLOYMENT_ROOT:-"/var/www/dracidoupe.cz/www_root/nove/application"}
remote_venv=${DEPLOYMENT_VENV:-"/var/www/dracidoupe.cz/www_root/nove/application/ddcz-venv"}
remote_requirements=${DEPLOYMENT_TMP_REQUIREMENTS_PATH:-"/var/www/dracidoupe.cz/www_root/nove/application-requirements"}

machine="$user@$host"

# Step 1: move requirements to remote machine and no, we can't do that remotely because TLS
reqdir=`mktemp -d`
cd $reqdir
pip download -r $curdir/requirements.txt --no-binary=:all:
cp $curdir/requirements.txt ./
rsync -avzd -m --delete $reqdir/ $machine:$remote_requirements/
cd $curdir
rm -rf $reqdir

# Step 2: Prepare and create clean venv on remote server, then remove the old venv with it
# Unfortunately move to backup needs to occur first since python3 venv doesn't support --relocatable
ssh $machine bash -c "'
    if [ -d $remote_root.bak ]; then rm -rf $remote_root.bak; fi && \
    if [ -d $remote_root ]; then mv $remote_root $remote_root.bak; fi && \
    mkdir $remote_root && \
    python3 -m venv $remote_venv && \
    $remote_venv/bin/pip3 install -r $remote_requirements/requirements.txt --no-index --find-links file://$remote_requirements
'"

# Step 3: Sync source code to remote
# --delete is not used because of how production.py works. This is to be solved
# in the future using proper redirects
rsync -avzt -m --exclude="*.pyc" --exclude="*.pyo" --exclude="__pycache__" $curdir/ddcz $curdir/graveyard $curdir/dragon $curdir/manage.py $curdir/static $machine:$remote_root/

# Migrate database and collect static files
ssh $machine bash -c "'
    cp $remote_root/../production.py $remote_root/graveyard/settings/ && \
    $remote_venv/bin/python3 $remote_root/manage.py check --deploy && \
    $remote_venv/bin/python3 $remote_root/manage.py migrate && \
    $remote_venv/bin/python3 $remote_root/manage.py loaddata pages && \
    $remote_venv/bin/python3 $remote_root/manage.py collectstatic --no-input
'"

# Restart process on remote, in a non-graceful way because traffic
# Before you ask...yes, sudo is whitelisted to this single command on remote

ssh $machine sudo /usr/bin/svc -k /etc/service/nove.dracidoupe.cz/
