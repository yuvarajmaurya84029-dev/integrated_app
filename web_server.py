import http.server
import socketserver
import json
import sqlite3
import time

PORT = 8080

class VectorAPIHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/vectors":
            conn = sqlite3.connect("pipeline.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, v0, v1, v2, v3 FROM embeddings ORDER BY id DESC LIMIT 5")
            rows = cursor.fetchall()
            conn.close()
            
            data = [{"id": r[0], "vector": [r[1], r[2], r[3], r[4]]} for r in rows]
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))
        elif self.path == "/stream":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            
            last_id = -1
            try:
                while True:
                    conn = sqlite3.connect("pipeline.db")
                    cursor = conn.cursor()
                    cursor.execute("SELECT id, v0, v1, v2, v3 FROM embeddings ORDER BY id DESC LIMIT 1")
                    row = cursor.fetchone()
                    conn.close()
                    
                    if row and row[0] != last_id:
                        last_id = row[0]
                        payload = json.dumps({"id": row[0], "vector": [row[1], row[2], row[3], row[4]]})
                        self.wfile.write(f"data: {payload}\n\n".encode("utf-8"))
                        self.wfile.flush()
                    time.sleep(0.3)
            except Exception:
                pass
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            html = """<!DOCTYPE html>
<html>
<head><title>Live Vector Telemetry Stream</title></head>
<body style="font-family: monospace; background: #181825; color: #a6adc8; padding: 2rem;">
<h2 style="color: #89b4fa;">Real-Time Cross-Stack Telemetry Stream</h2>
<div style="margin-bottom: 1rem;">Status: <span id="status" style="color: #a6e3a1;">Connecting...</span></div>
<pre id="output" style="background: #1e1e2e; padding: 1rem; color: #f9e2af; border: 1px solid #45475a;"></pre>
<script>
const evtSource = new EventSource("/stream");
evtSource.onmessage = function(event) {
    document.getElementById("status").innerText = "Live (SSE Stream Active)";
    document.getElementById("output").innerText = event.data;
};
evtSource.onerror = function() {
    document.getElementById("status").innerText = "Disconnected";
};
</script>
</body>
</html>"""
            self.wfile.write(html.encode("utf-8"))

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), VectorAPIHandler) as httpd:
        print(f"[Live SSE Server] Running at http://localhost:{PORT}")
        httpd.serve_forever()
