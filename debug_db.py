import sqlite3
import os

DB_PATH = 'homestay.db'
if os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("--- ROOMS ---")
    rooms = cursor.execute("SELECT id, name FROM rooms").fetchall()
    for r in rooms:
        print(f"ID: {r['id']} | Name: {r['name']}")
        
    print("\n--- BOOKINGS ---")
    bookings = cursor.execute("SELECT * FROM bookings").fetchall()
    for b in bookings:
        print(f"ID: {b['id']} | RoomID: {b['room_id']} | Guest: {b['guest_name']} | CheckIn: {b['check_in']} | CheckOut: {b['check_out']} | Status: {b['status']}")
    
    conn.close()
else:
    print("Database not found.")
