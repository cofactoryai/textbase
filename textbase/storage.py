from fastapi import HTTPException
import sqlite3

# Create and connect to the SQLite database
conn = sqlite3.connect("data_store.db")
cursor = conn.cursor()


def create_data_store_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data_store (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    conn.commit()

create_data_store_table()

# function to set data
async def set_data(key,value):
    try:
        cursor.execute("INSERT OR REPLACE INTO data_store (key, value) VALUES (?, ?)", (key, value))
        conn.commit()
        print ("message", "Data set successfully")
        # cursor.execute("SELECT value FROM data_store WHERE key = ?", (key,))
        # row = cursor.fetchone()
        # print("row",row)
    except sqlite3.Error as e:
        return HTTPException(status_code=500, detail="Database error")

# function to get data
async def get_data(key):
    try:
        cursor.execute("SELECT value FROM data_store WHERE key = ?", (key,))
        row = cursor.fetchone()
        print("row",row)
        if row is not None:
            print("row",row)
            return row[0]
        else:
            return None
    except sqlite3.Error as e:
        return HTTPException(status_code=500, detail="Database error")
