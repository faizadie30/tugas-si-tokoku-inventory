import sqlite3

def get_connection():
    return sqlite3.connect("tokoku.db")

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS barang (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        stok INTEGER,
        harga INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transaksi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_barang TEXT,
        jumlah INTEGER
    )
    """)

    conn.commit()
    conn.close()
