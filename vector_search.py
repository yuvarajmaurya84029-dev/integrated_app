import sqlite3
import numpy as np

def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

conn = sqlite3.connect("pipeline.db")
cursor = conn.cursor()

# Retrieve stored vector embeddings
cursor.execute("SELECT id, vector_data FROM vectors LIMIT 2")
rows = cursor.fetchall()

if len(rows) == 2:
    v1 = np.frombuffer(rows[0][1], dtype=np.float32)
    v2 = np.frombuffer(rows[1][1], dtype=np.float32)
    score = cosine_similarity(v1, v2)
    print(f"[SEARCH ENGINE] Vector #{rows[0][0]} <-> Vector #{rows[1][0]}")
    print(f"[COSINE SCORE ] {score:.6f}")
else:
    print("[INFO] Generate vectors first using: python3 ai_engine.py")

conn.close()
