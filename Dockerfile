FROM python:3.11-slim
WORKDIR /app

# Install native C compiler toolchain and SQLite headers
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    sqlite3 \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Compile C23 binary inside container runtime
RUN gcc -O3 c_reader.c -lsqlite3 -o c_reader

EXPOSE 8080
CMD ["python3", "web_server.py"]
