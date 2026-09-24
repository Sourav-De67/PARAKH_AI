import sqlite3
import os
from datetime import datetime

# ==========================================================
# DATABASE PATH
# ==========================================================

DB_NAME = os.path.join(os.path.dirname(__file__), "parakh_ai.db")


# ==========================================================
# CREATE DATABASE & TABLE
# ==========================================================

def init_db():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            image_name TEXT NOT NULL,

            status TEXT NOT NULL,

            percentage INTEGER NOT NULL,

            manufacturer INTEGER,

            generic_name INTEGER,

            net_quantity INTEGER,

            mrp INTEGER,

            unit_sale_price INTEGER,

            consumer_care INTEGER,

            date_declaration INTEGER,

            scan_time TEXT NOT NULL

        )
    """)

    conn.commit()
    conn.close()


# ==========================================================
# SAVE SCAN
# ==========================================================

def save_scan(image_name, status, percentage, results):

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO scan_history (
                image_name,
                status,
                percentage,
                manufacturer,
                generic_name,
                net_quantity,
                mrp,
                unit_sale_price,
                consumer_care,
                date_declaration,
                scan_time
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            image_name,
            status,
            percentage,
            int(results.get("Manufacturer / Packer / Importer", False)),
            int(results.get("Common / Generic Name", False)),
            int(results.get("Net Quantity", False)),
            int(results.get("MRP", False)),
            int(results.get("Unit Sale Price", False)),
            int(results.get("Consumer Care Details", False)),
            int(results.get("Relevant Date Declaration", False)),
            datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        ))

        conn.commit()
        print(f"✅ Saved to SQLite: {image_name} | {status} | {percentage}%", flush=True)

    except Exception as e:
        print("❌ SQLite Error:", e, flush=True)

    finally:
        if 'conn' in locals():
            conn.close()

# ==========================================================
# GET ALL SCANS
# ==========================================================

def get_all_scans():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM scan_history
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data