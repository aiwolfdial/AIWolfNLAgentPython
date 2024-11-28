#!/bin/bash
source ./../.venv/bin/activate

while true; do
    python3 main.py
    echo "Restarting in 15 seconds..."
    sleep 15
done