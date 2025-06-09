import os
import pandas as pd
import sqlite3
from sqlalchemy import text
from langchain_community.utilities import SQLDatabase

# Constants
CSV_PATH = "../data/retail_transactions_dataset.csv"
DB_FILE_PATH = "../data/retail_transactions_data.db"
DB_URI = f"sqlite:///{DB_FILE_PATH}"
TABLE_NAME = "retail_transactions"

# Check if DB already exists
if not os.path.exists(DB_FILE_PATH):
    print("⚠️ DB not found. Creating SQLite DB from CSV...")

    # Load data
    df = pd.read_csv(CSV_PATH)

    # Create SQLite DB
    conn = sqlite3.connect(DB_FILE_PATH)
    df.to_sql(TABLE_NAME, conn, index=False, if_exists="replace")

    # # Sample query to verify
    # cursor = conn.cursor()
    # cursor.execute(f"SELECT * FROM {TABLE_NAME} LIMIT 5")
    # rows = cursor.fetchall()
    # print("Sample rows:", rows)

    conn.close()
    print(f"✅ SQLite DB created at '{DB_FILE_PATH}'")

else:
    print("✅ SQLite DB already exists. Connecting...")

# Connect using LangChain's SQLDatabase
db = SQLDatabase.from_uri(DB_URI)

# List all tables
print("Tables:", db.get_usable_table_names())

# Run sample query
with db._engine.connect() as conn:
    result = conn.execute(text(f"SELECT * FROM {TABLE_NAME} LIMIT 5"))
    for row in result:
        print(row)
