#!/usr/bin/env bash

while true; do
    sleep 30

    echo "=== Running commands at $(date) ==="

    ./delta-to-map.sh
    python3.11 timing-test.py

    echo "=== Done, sleeping again ==="
done
