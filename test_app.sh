#!/usr/bin/bash
set -e

echo "=========================================="
echo "    INTEGRATED APP SYSTEM VALIDATION      "
echo "=========================================="

echo "[1/4] Testing Python AI Engine Ingestion..."
python3 ai_engine.py > /dev/null

echo "[2/4] Compiling & Verifying C23 Native Reader..."
clang -std=c23 -O3 c_reader.c -lsqlite3 -o c_reader
./c_reader > /dev/null

echo "[3/4] Validating Docker Manifest Files..."
test -f Dockerfile && test -f docker-compose.yml

echo "[4/4] Testing HTTP API Vector Endpoint..."
python3 web_server.py > /dev/null 2>&1 &
SERVER_PID=$!
sleep 1
curl -s http://localhost:8080/api/vectors | grep -q "vector"
kill $SERVER_PID 2>/dev/null || true

echo "=========================================="
echo "   ALL STACK INTEGRATION TESTS PASSED     "
echo "=========================================="
