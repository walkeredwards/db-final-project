import sqlite3


def setup_database() -> None:
    conn = sqlite3.connect("fitness.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Exercise()
                   """)