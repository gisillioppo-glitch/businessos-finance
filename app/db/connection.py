DB_PATH = "finance.db"


def create_connection():
    import sqlite3

    return sqlite3.connect(DB_PATH)
