CC = clang
CFLAGS = -std=c23 -O3
LIBS = -lsqlite3

all: build run

build:
$(CC) $(CFLAGS) c_reader.c $(LIBS) -o c_reader

run: build
python3 ai_engine.py
./c_reader

benchmark: build
@python3 -c "import time, subprocess; t0=time.time(); [subprocess.run(['python3', 'ai_engine.py'], stdout=subprocess.DEVNULL) for _ in range(50)]; print(f'[Benchmark] 50 Python AI Writes: {time.time()-t0:.3f}s')"
@python3 -c "import time, subprocess; t0=time.time(); [subprocess.run(['./c_reader'], stdout=subprocess.DEVNULL) for _ in range(50)]; print(f'[Benchmark] 50 C23 Native Reads: {time.time()-t0:.3f}s')"

clean:
rm -f c_reader pipeline.db

serve: build
python3 ai_engine.py
python3 web_server.py

docker-build:
docker build -t vector-engine:latest .

docker-up:
docker-compose up -d
