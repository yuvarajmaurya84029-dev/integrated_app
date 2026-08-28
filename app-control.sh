#!/usr/bin/bash
PID_DIR="run"
mkdir -p "$PID_DIR"

case "$1" in
    start)
        echo "[System Control] Initializing Integrated Services..."
        python3 ai_engine.py > /dev/null
        python3 web_server.py > log_web.log 2>&1 &
        echo $! > "$PID_DIR/web.pid"
        ./live_generator.sh > log_gen.log 2>&1 &
        echo $! > "$PID_DIR/gen.pid"
        echo "[System Control] Services Active. Stream visualizer live at http://localhost:8080"
        ;;
    stop)
        echo "[System Control] Shutting Down Services..."
        if [ -f "$PID_DIR/web.pid" ]; then kill $(cat "$PID_DIR/web.pid") 2>/dev/null; rm "$PID_DIR/web.pid"; fi
        if [ -f "$PID_DIR/gen.pid" ]; then kill $(cat "$PID_DIR/gen.pid") 2>/dev/null; rm "$PID_DIR/gen.pid"; fi
        pkill -f live_generator.sh 2>/dev/null
        pkill -f web_server.py 2>/dev/null
        echo "[System Control] All processes terminated."
        ;;
    status)
        echo "=========================================="
        echo "      SERVICE STATUS DASHBOARD            "
        echo "=========================================="
        if pgrep -f "web_server.py" > /dev/null; then
            echo "Web Server      : RUNNING (http://localhost:8080)"
        else
            echo "Web Server      : STOPPED"
        fi
        if pgrep -f "live_generator.sh" > /dev/null; then
            echo "Vector Engine   : RUNNING (SSE Ingestion Active)"
        else
            echo "Vector Engine   : STOPPED"
        fi
        echo "=========================================="
        ;;
    logs)
        echo "=== Web Telemetry Logs ==="
        tail -n 15 log_web.log 2>/dev/null || echo "No logs found."
        ;;
    *)
        echo "Usage: ./app-control.sh {start|stop|status|logs}"
        ;;
esac
