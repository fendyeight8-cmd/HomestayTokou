#!/usr/bin/env python3
import os
import sys
import argparse
from app import init_db, HomestayHandler, ThreadingHTTPServer

def main():
    parser = argparse.ArgumentParser(description="Homestay Tokou Server")
    parser.add_argument("--host", default="0.0.0.0", help="Binding host")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", 8080)), help="Binding port")
    
    args = parser.parse_args()

    # Initialize database before starting
    init_db()

    print("\n" + "="*46)
    print("  Homestay Tokou - Production Server")
    print(f"  Running on http://{args.host}:{args.port}")
    print("="*46)
    
    server = ThreadingHTTPServer((args.host, args.port), HomestayHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    main()
