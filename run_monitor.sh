#!/usr/bin/env bash

# set -v

cd /home/monpi/co2_monitor

source ./venv/bin/activate

# -u = unbuffered stdout so appears in systemd logs
python -u co2.py
