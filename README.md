# Integrated Cross-Stack Vector Engine 🚀

A high-performance embedded vector embedding engine built with C23, Python, SQLite, and Server-Sent Events (SSE).

## 🛠 Tech Stack
* **Core Runtime:** C23 / Clang
* **Data Processing:** Python 3.11 / NumPy
* **Storage:** SQLite3
* **Telemetry Server:** Pure Python Standard Library HTTP/SSE
* **Containerization:** Docker & Docker Compose

## ⚡ Quick Start

```bash
# Start vector services
./app-control.sh start

# Run end-to-end integration tests
./test_app.sh
