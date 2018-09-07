#!/bin/bash
set -e

git archive HEAD -o deploy/noisebot.tar.gz
pushd deploy
ansible-playbook deploy.yml
popd
