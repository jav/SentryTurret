#!/usr/bin/env bash
REMOTEUSER=pi
REMOTEHOST=192.168.0.26

#Assumes we have uploaded our ssh-pubkey.
# cat ~/.ssh/id_rsa.pub | ssh user@hostname 'cat >> .ssh/authorized_keys'

rsync -avz . $REMOTEUSER@$REMOTEHOST:$(basename $(pwd))

