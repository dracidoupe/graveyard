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

host=${DEPLOYMENT_HOST:-"revy"}
user=${DEPLOYMENT_USERNAME:-"w-dracidoupe-cz"}

remote_root=${DEPLOYMENT_ROOT:-"/var/www/dracidoupe.cz/www_root/api/application/src"}
remote_venv=${DEPLOYMENT_VENV:-"/var/www/dracidoupe.cz/www_root/api/application/ddcz-api-venv"}
remote_requirements=${DEPLOYMENT_TMP_REQUIREMENTS_PATH:-"/tmp/ddcz-api-deploy-requirements.txt"}

machine="$user@$host"

# Step 1: move requirements to remote machine
scp requirements.txt $machine:$remote_requirements

# Step 2: Prepare and create clean venv on remote server, then remove the old venv with it
# Unfortunately move to backup needs to occur first since python3 venv doesn't support --relocatable
ssh $machine bash -c "'
    if [ -d $remote_venv.bak ]; then rm -rf $remote_venv.bak; fi && \
    if [ -d $remote_venv ]; then mv $remote_venv $remote_venv.bak; fi && \
    mkdir $remote_venv && \
    python3 -m venv $remote_venv && \
    $remote_venv/bin/pip3 install -r $remote_requirements && \
    rm $remote_requirements
'"

# Step 3: Sync source code to remote
rsync -avzt --delete -m --exclude="*.pyc" --exclude="*.pyo" --exclude="__pycache__" ./src/ $machine:$remote_root/

# Restart process on remote, in a non-graceful way because traffic
# Before you ask...yes, sudo is whitelisted to this single command on remote
ssh $machine sudo /usr/bin/svc -k /etc/service/api.dracidoupe.cz/
