#!/usr/bin/env bash

cd /home/monpi/co2_monitor

source ./venv/bin/activate

python co2.py >co2.log 2>&1
