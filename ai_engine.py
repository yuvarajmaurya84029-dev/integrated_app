import sqlite3
import numpy as np

def generate_embeddings():
    np.random.seed(42)
    # Cast numpy float32 values to standard Python floats
    raw_vector = np.random.rand(4)
    vector = [float(x) for x in raw_vector]
    
    conn = sqlite3.connect("pipeline.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            v0 REAL, v1 REAL, v2 REAL, v3 REAL
        )
    """)
    cursor.execute("INSERT INTO embeddings (v0, v1, v2, v3) VALUES (?, ?, ?, ?)", tuple(vector))
    conn.commit()
    conn.close()
    print(f"[Python AI Engine] Generated & Cached Vector: {[round(x, 4) for x in vector]}")

if __name__ == "__main__":
    generate_embeddings()
