#!/usr/bin/env python3
"""
manage.py — Database management CLI for Rumah Alam Homestay

Usage:
    python manage.py init          # Create tables & seed data
    python manage.py reset         # Drop all tables & reseed (DESTRUCTIVE)
    python manage.py stats         # Print database statistics
    python manage.py rooms         # List all rooms
    python manage.py bookings      # List recent bookings
    python manage.py block         # Block a date for a room
    python manage.py export        # Export bookings to CSV
"""

import sys
import os

# Ensure project root in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.models import (
    init_db, Base, engine, SessionLocal,
    Room, Guest, Booking, BlockedDate, SiteSetting
)
from backend import crud
from datetime import date, timedelta
import csv


def cmd_init():
    print("Initialising database…")
    init_db()
    db = SessionLocal()
    rooms    = db.query(Room).count()
    settings = db.query(SiteSetting).count()
    db.close()
    print(f"✅ Done. {rooms} rooms, {settings} settings loaded.")


def cmd_reset():
    confirm = input("⚠️  This will DELETE all data. Type 'yes' to confirm: ")
    if confirm.strip().lower() != "yes":
        print("Aborted.")
        return
    print("Dropping all tables…")
    Base.metadata.drop_all(bind=engine)
    print("Recreating and seeding…")
    init_db()
    print("✅ Reset complete.")


def cmd_stats():
    db = SessionLocal()
    stats = crud.get_dashboard_stats(db)
    print("\n─── Rumah Alam Database Statistics ───")
    print(f"  Total Bookings : {stats['total_bookings']}")
    print(f"  Pending        : {stats['pending']}")
    print(f"  Confirmed      : {stats['confirmed']}")
    print(f"  Total Revenue  : RM {stats['revenue']:,.0f}")
    print(f"  Total Guests   : {stats['total_guests']}")
    print(f"  Check-ins Today: {stats['checkins_today']}")
    print("────────────────────────────────────\n")
    db.close()


def cmd_rooms():
    db = SessionLocal()
    rooms = crud.get_rooms(db, active_only=False)
    print(f"\n{'ID':<5}{'Slug':<22}{'Name':<26}{'Type':<12}{'Price':>8}{'Status':>10}")
    print("─" * 85)
    for r in rooms:
        print(f"{r.id:<5}{r.slug:<22}{r.name:<26}{r.room_type:<12}RM {r.price_night:>5.0f}{r.status:>10}")
    print()
    db.close()


def cmd_bookings():
    db = SessionLocal()
    bookings = crud.get_all_bookings(db)[:20]
    print(f"\n{'Ref':<14}{'Guest':<22}{'Room':<22}{'Check-in':<13}{'Nights':>7}{'Total':>10}{'Status':>12}")
    print("─" * 105)
    for b in bookings:
        print(
            f"{b.reference:<14}"
            f"{b.guest.full_name[:20]:<22}"
            f"{b.room.name[:20]:<22}"
            f"{str(b.check_in):<13}"
            f"{b.nights:>7}"
            f"RM {b.total_price:>7.0f}"
            f"{b.status:>12}"
        )
    if not bookings:
        print("  No bookings found.")
    print()
    db.close()


def cmd_block():
    db = SessionLocal()
    rooms = crud.get_rooms(db, active_only=True)
    print("\nAvailable rooms:")
    for r in rooms:
        print(f"  {r.id} — {r.name}")
    room_id = int(input("\nEnter room ID to block: ").strip())
    date_str = input("Enter date to block (YYYY-MM-DD): ").strip()
    reason   = input("Reason (optional): ").strip() or "Blocked by admin"
    try:
        d = date.fromisoformat(date_str)
        bd = BlockedDate(room_id=room_id, blocked_on=d, reason=reason)
        db.add(bd)
        db.commit()
        print(f"✅ Blocked {date_str} for room {room_id}.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()


def cmd_export():
    db = SessionLocal()
    bookings = crud.get_all_bookings(db)
    filename = f"bookings_export_{date.today().isoformat()}.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Reference", "Status", "Room", "Guest Name", "Phone", "Email",
            "Check-in", "Check-out", "Nights", "Adults", "Children",
            "Price/Night", "Total", "Special Requests", "Booked At"
        ])
        for b in bookings:
            writer.writerow([
                b.reference, b.status, b.room.name,
                b.guest.full_name, b.guest.phone, b.guest.email or "",
                b.check_in, b.check_out, b.nights,
                b.adults, b.children,
                b.price_per_night, b.total_price,
                (b.special_requests or "").replace("\n", " "),
                b.created_at.strftime("%Y-%m-%d %H:%M"),
            ])
    print(f"✅ Exported {len(bookings)} bookings to {filename}")
    db.close()


COMMANDS = {
    "init":     cmd_init,
    "reset":    cmd_reset,
    "stats":    cmd_stats,
    "rooms":    cmd_rooms,
    "bookings": cmd_bookings,
    "block":    cmd_block,
    "export":   cmd_export,
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(1)
    COMMANDS[sys.argv[1]]()
