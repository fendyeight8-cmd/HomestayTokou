#!/usr/bin/env python3
"""
Market Tokou — Quick launcher.
Usage:  python run.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
# Import the server components directly from app
from app import init_db, HomestayHandler, ThreadingHTTPServer

if __name__ == "__main__":
    init_db()
    PORT = int(os.environ.get("PORT", 8080))
    server = ThreadingHTTPServer(("0.0.0.0", PORT), HomestayHandler)
    print("\n" + "="*46)
    print("  Market Tokou Store Management System")
    print(f"  http://0.0.0.0:{PORT}")
    print("="*46)
    print("  Press CTRL+C to stop\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
