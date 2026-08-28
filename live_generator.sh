#!/usr/bin/bash
echo "[Live Vector Ingestion Service Started]"
while true; do
    python3 ai_engine.py > /dev/null
    sleep 2
done
