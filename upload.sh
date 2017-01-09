#!/usr/bin/env bash
REMOTEUSER=pi
REMOTEHOST=192.168.0.26
REMOTECONN=${1:-$REMOTEUSER@$REMOTEHOST}

EXCLUDE="dlib*/build/ tools/python/build/"
EXCLUDEMERGEDARGS=$(for PATH in $EXCLUDE; do echo "--exclude $PATH"; done)

#Assumes we have uploaded our ssh-pubkey.
# cat ~/.ssh/id_rsa.pub | ssh user@hostname 'cat >> .ssh/authorized_keys'

rsync -avz $EXCLUDEMERGEDARGS . $REMOTECONN:$(basename $(pwd))

