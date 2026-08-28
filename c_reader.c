#include <stdio.h>
#include <stdlib.h>
#include <sqlite3.h>

int main(void) {
    sqlite3 *db;
    sqlite3_stmt *res;
    
    if (sqlite3_open("pipeline.db", &db) != SQLITE_OK) {
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
        return 1;
    }
    
    const char *sql = "SELECT id, v0, v1, v2, v3 FROM embeddings ORDER BY id DESC LIMIT 1;";
    if (sqlite3_prepare_v2(db, sql, -1, &res, 0) == SQLITE_OK) {
        if (sqlite3_step(res) == SQLITE_ROW) {
            printf("[C23 Native Engine] Verified Cache -> ID: %d | Vector: [%.4f, %.4f, %.4f, %.4f]\n",
                sqlite3_column_int(res, 0),
                sqlite3_column_double(res, 1),
                sqlite3_column_double(res, 2),
                sqlite3_column_double(res, 3),
                sqlite3_column_double(res, 4));
        }
    }
    sqlite3_finalize(res);
    sqlite3_close(db);
    return 0;
}
