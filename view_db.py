import sqlite3

conn = sqlite3.connect("parakh_ai.db")
cursor = conn.cursor()

print("\n===== PARAKH AI DATABASE =====\n")

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("Tables:", cursor.fetchall())

cursor.execute("SELECT id, image_name, status, percentage, scan_time FROM scan_history ORDER BY id DESC")

rows = cursor.fetchall()

if not rows:
    print("\nNo scan records found.")
else:
    print("\nStored Scan Records:\n")
    for row in rows:
        print(f"ID: {row[0]}")
        print(f"Image: {row[1]}")
        print(f"Status: {row[2]}")
        print(f"Score: {row[3]}%")
        print(f"Time: {row[4]}")
        print("-" * 40)

conn.close()