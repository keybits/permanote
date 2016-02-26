#!/bin/bash
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y sqlite3 build-essential python3-dev python3-virtualenv
