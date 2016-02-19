#!/bin/bash
set -euo pipefail

mkdir -p /var/log
mkdir -p /var/uploads
# Wipe /var/run, since pidfiles and socket files from previous launches should go away
# TODO someday: I'd prefer a tmpfs for these.
rm -rf /var/run
mkdir -p /var/run

set +o nounset
source /opt/app/env/bin/activate
set -o nounset
python /opt/app/main.py
