import sqlite3
import json
import os
import re
import logging
from datetime import datetime, date
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Tuple, Dict, Any, List

# ─── Configuration & Logging ──────────────────────────────────────────────────

DB_PATH = os.path.join(os.path.dirname(__file__), 'homestay.db')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# ─── Database Management ──────────────────────────────────────────────────────

class Database:
    """Context manager for SQLite database connections."""
    def __init__(self, path: str):
        self.path = path

    def __enter__(self):
        self.conn = sqlite3.connect(self.path, timeout=10)
        self.conn.row_factory = sqlite3.Row
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

def init_db():
    """Initialise the database with tables and seed data if necessary."""
    with Database(DB_PATH) as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
        cur = conn.cursor()
        cur.executescript("""
            CREATE TABLE IF NOT EXISTS rooms (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL,
                type        TEXT NOT NULL,
                price       REAL NOT NULL,
                capacity    INTEGER NOT NULL,
                description TEXT,
                amenities   TEXT,
                image_url   TEXT
            );



            CREATE TABLE IF NOT EXISTS reviews (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_id  INTEGER,
                guest_name  TEXT NOT NULL,
                rating      INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
                comment     TEXT,
                created_at  TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS bookings (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id     INTEGER NOT NULL,
                guest_name  TEXT NOT NULL,
                check_in    TEXT NOT NULL,
                check_out   TEXT NOT NULL,
                total_price REAL NOT NULL,
                status      TEXT DEFAULT 'confirmed',
                created_at  TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (room_id) REFERENCES rooms (id)
            );

            CREATE TABLE IF NOT EXISTS settings (
                key         TEXT PRIMARY KEY,
                value       TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS users (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                username    TEXT UNIQUE NOT NULL,
                password    TEXT NOT NULL
            );
        """)

        # Seed data
        cur.execute("SELECT COUNT(*) FROM rooms")
        if cur.fetchone()[0] == 0:
            rooms = [
                ("Room 1", "Twin Sharing", 88.00, 2,
                 "These elegantly designed rooms blend modern luxury with comfort, featuring marble-inspired walls with gold accents, plush bedding, warm ambient lighting, air conditioning, and thoughtful amenities to create a stylish and tranquil homestay experience.",
                 "Smart TV,Double Single Bed,Private Balcony,Air Conditioning,Hot Shower,WiFi,Mini Fridge",
                 "bilik-no-1.jpg"),
                ("Room 3", "Twin Sharing", 108.00, 6,
                 "These sophisticated rooms offer a seamless mix of modern elegance and comfort, highlighted by marble-textured walls with gold detailing, cozy bedding, soft lighting, and essential amenities for a relaxing homestay stay.",
                 "Smart TV,Double Single Bed,Living Area,Air Conditioning,Hot Shower,WiFi,Mini Fridge,Bathtub",
                 "bilik-no-3.jpg"),
                ("Room 6", "Queen Deluxe", 108.00, 2,
                 "With their refined marble finishes, subtle gold accents, and minimalist furnishings, these rooms provide a cozy yet stylish retreat complete with all the comforts needed for a pleasant stay.",
                 "Smart TV,Queen Bed,Air Conditioning,Hot Shower,WiFi",
                 "bilik-no-6.jpg"),
                ("Room 8", "Queen Deluxe", 118.00, 4,
                 "Blending contemporary design with everyday comfort, the rooms showcase elegant marble-style walls, soft ambient lighting, and well-appointed amenities, offering a peaceful and welcoming homestay environment.",
                 "Smart TV,Queen Bed,Sofa Bed,Private Pool,Outdoor Deck,Air Conditioning,Bathtub,Hot Shower,WiFi,Mini Bar,Nespresso Machine",
                 "bilik-no-8.jpg"),
            ]
            cur.executemany("""
                INSERT INTO rooms (name, type, price, capacity, description, amenities, image_url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, rooms)

            reviews = [
                (None, "Ahmad Faizal", 5, "Tempat yang sangat cantik! Pemandangan sawah pagi hari memang luar biasa. Akan datang lagi!"),
                (None, "Sarah Lim", 5, "Amazing experience! The hosts were so warm and welcoming. Breakfast was delicious."),
                (None, "Rajan Kumar", 4, "Great place to relax and unwind. Clean rooms, friendly staff. Highly recommended!"),
                (None, "Nurul Ain", 5, "Sangat sesuai untuk balik kampung experience. Suite dengan private pool - terbaik!"),
            ]
            cur.executemany("""
                INSERT INTO reviews (booking_id, guest_name, rating, comment)
                VALUES (?, ?, ?, ?)
            """, reviews)

            # Seed Bookings for Sales Dashboard
            bookings = [
                (1, "Ahmad Faiz", "2026-04-24", "2026-04-26", 176.00, "confirmed"),
                (3, "Sarah Wilson", "2026-04-25", "2026-04-28", 324.00, "confirmed"),
                (6, "Chin Wei", "2026-05-01", "2026-05-03", 216.00, "confirmed")
            ]
            cur.executemany("""
                INSERT INTO bookings (room_id, guest_name, check_in, check_out, total_price, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, bookings)
            logger.info("Database seeded with initial data.")

        # Seed Admin & Settings
        cur.execute("SELECT COUNT(*) FROM users")
        if cur.fetchone()[0] == 0:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin123"))
            cur.execute("INSERT INTO settings (key, value) VALUES (?, ?)", ("whatsapp", "+601110085626"))
            cur.execute("INSERT INTO settings (key, value) VALUES (?, ?)", ("qr_code", "payment-qr.jpg"))
            logger.info("Admin and Settings seeded.")

    logger.info(f"Database initialised at {DB_PATH}")

# ─── Helpers ──────────────────────────────────────────────────────────────────



def json_response(data: Any, status: int = 200) -> Tuple[int, bytes]:
    """Format a JSON response."""
    body = json.dumps(data, default=str).encode()
    return status, body

def rows_to_list(rows: List[sqlite3.Row]) -> List[Dict[str, Any]]:
    """Convert SQLite rows to a list of dictionaries."""
    return [dict(r) for r in rows]

# ─── API Handlers ─────────────────────────────────────────────────────────────

def handle_get_rooms(params: Dict[str, List[str]]) -> Tuple[int, bytes]:
    try:
        min_guests = int(params.get('guests', ['0'])[0] or 0)
    except (ValueError, TypeError):
        min_guests = 0

    check_in = params.get('check_in', [None])[0]
    check_out = params.get('check_out', [None])[0]

    with Database(DB_PATH) as conn:
        query = "SELECT * FROM rooms WHERE capacity >= ? ORDER BY id ASC"
        rooms = rows_to_list(conn.execute(query, (min_guests,)).fetchall())
        
        for r in rooms:
            if check_in and check_out:
                # Check for conflicting bookings
                # Overlap if: (existing_check_in < requested_check_out) AND (existing_check_out > requested_check_in)
                conflicts = conn.execute("""
                    SELECT COUNT(*) FROM bookings 
                    WHERE room_id = ? 
                    AND status != 'cancelled'
                    AND (check_in < ? AND check_out > ?)
                """, (r['id'], check_out, check_in)).fetchone()[0]
                r['available'] = (conflicts == 0)
            else:
                r['available'] = True
            r['amenities'] = r['amenities'].split(',') if r['amenities'] else []

    return json_response(rooms)

def handle_get_room(room_id: int) -> Tuple[int, bytes]:
    with Database(DB_PATH) as conn:
        row = conn.execute("SELECT * FROM rooms WHERE id=?", (room_id,)).fetchone()
        if not row:
            return json_response({"error": "Room not found"}, 404)
        room = dict(row)
        room['amenities'] = room['amenities'].split(',') if room['amenities'] else []
        return json_response(room)



def handle_get_reviews() -> Tuple[int, bytes]:
    with Database(DB_PATH) as conn:
        reviews = rows_to_list(conn.execute("SELECT * FROM reviews ORDER BY created_at DESC LIMIT 20").fetchall())
        avg = conn.execute("SELECT AVG(rating) FROM reviews").fetchone()[0]
        return json_response({"reviews": reviews, "average_rating": round(avg or 0, 1)})

def handle_dashboard() -> Tuple[int, bytes]:
    with Database(DB_PATH) as conn:
        stats = {
            "total_bookings": conn.execute("SELECT COUNT(*) FROM bookings").fetchone()[0],
            "total_revenue":  round(conn.execute("SELECT SUM(total_price) FROM bookings").fetchone()[0] or 0, 2),
            "total_rooms":    conn.execute("SELECT COUNT(*) FROM rooms").fetchone()[0],
            "avg_rating":     round(conn.execute("SELECT AVG(rating) FROM reviews").fetchone()[0] or 0, 1),
            "recent_bookings": rows_to_list(conn.execute("""
                SELECT b.*, r.name as room_name 
                FROM bookings b 
                JOIN rooms r ON b.room_id = r.id 
                ORDER BY b.created_at DESC LIMIT 5
            """).fetchall()),
        }
        return json_response(stats)

def handle_login(data: Dict[str, Any]) -> Tuple[int, bytes]:
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    logger.info(f"[LOGIN ATTEMPT] User: {username}")
    with Database(DB_PATH) as conn:
        user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
        if user:
            return json_response({"success": True, "token": "admin_session_active"})
        return json_response({"success": False, "error": "Invalid credentials"}, 401)

def handle_update_room(rid: int, data: Dict[str, Any]) -> Tuple[int, bytes]:
    with Database(DB_PATH) as conn:
        conn.execute("UPDATE rooms SET price=?, name=?, type=?, capacity=? WHERE id=?", 
                    (data['price'], data['name'], data['type'], data['capacity'], rid))
        return json_response({"success": True})

def handle_add_room(data: Dict[str, Any]) -> Tuple[int, bytes]:
    with Database(DB_PATH) as conn:
        conn.execute("INSERT INTO rooms (name, type, price, capacity, description, amenities, image_url) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (data['name'], data['type'], data['price'], data['capacity'], data['description'], data['amenities'], data['image_url']))
        return json_response({"success": True})

def handle_get_settings() -> Tuple[int, bytes]:
    with Database(DB_PATH) as conn:
        settings = rows_to_list(conn.execute("SELECT * FROM settings").fetchall())
        return json_response({s['key']: s['value'] for s in settings})

def handle_update_setting(data: Dict[str, Any]) -> Tuple[int, bytes]:
    key = data.get('key')
    val = data.get('value')
    with Database(DB_PATH) as conn:
        conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, val))
        return json_response({"success": True})

# ─── HTTP Server ──────────────────────────────────────────────────────────────

MIME_TYPES = {
    '.html': 'text/html', '.css': 'text/css', '.js': 'application/javascript',
    '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.svg': 'image/svg+xml',
}

class HomestayHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        logger.info(fmt % args)

    def send_json(self, status, body):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, filename):
        # Security: Normalize path and prevent directory traversal
        clean_filename = os.path.normpath(filename).lstrip(os.sep + (os.altsep or ''))
        filepath = os.path.join(os.path.dirname(__file__), clean_filename)
        
        # Security: Only serve files from within the project directory
        # and prevent access to sensitive files
        if not filepath.startswith(os.path.dirname(__file__)) or \
           clean_filename.endswith(('.py', '.db', '.env', '.sh')) or \
           clean_filename.startswith(('.git', '__pycache__')):
            return self.send_json(*json_response({"error": "Access denied"}, 403))

        # Auto-create uploads if requested
        if clean_filename.startswith('uploads') or clean_filename.startswith('images'):
            os.makedirs(os.path.join(os.path.dirname(__file__), 'uploads'), exist_ok=True)
            os.makedirs(os.path.join(os.path.dirname(__file__), 'images'), exist_ok=True)

        if not os.path.isfile(filepath):
            return self.send_json(*json_response({"error": "File not found"}, 404))
        
        ext = os.path.splitext(filepath)[1]
        mime = MIME_TYPES.get(ext, 'application/octet-stream')
        
        try:
            with open(filepath, 'rb') as f:
                self.send_response(200)
                self.send_header('Content-Type', mime)
                self.send_header('Content-Length', str(os.path.getsize(filepath)))
                self.send_header('Cache-Control', 'public, max-age=86400')
                self.end_headers()
                
                # Stream file in chunks for better memory performance
                while True:
                    chunk = f.read(65536)
                    if not chunk: break
                    self.wfile.write(chunk)
        except Exception as e:
            logger.error(f"Error reading file {filepath}: {e}")
            self.send_json(*json_response({"error": "Error reading file"}, 500))

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/') or '/'
        params = parse_qs(parsed.query)

        try:
            if path == '/': return self.send_file('index.html')
            if path == '/admin': return self.send_file('admin.html')
            
            # API Routes
            if path == '/api/rooms': return self.send_json(*handle_get_rooms(params))
            if path.startswith('/api/rooms/'):
                try:
                    rid = int(path.split('/')[-1])
                    return self.send_json(*handle_get_room(rid))
                except (ValueError, IndexError):
                    return self.send_json(*json_response({"error": "Invalid Room ID"}, 400))
            if path == '/api/reviews': return self.send_json(*handle_get_reviews())
            if path == '/api/dashboard': return self.send_json(*handle_dashboard())
            if path == '/api/settings': return self.send_json(*handle_get_settings())

            # Static assets
            return self.send_file(path.lstrip('/'))
        except Exception as e:
            logger.error(f"Error handling GET {path}: {e}")
            self.send_json(*json_response({"error": "Internal server error"}, 500))

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        try:
            data = json.loads(post_data) if post_data else {}
        except:
            data = {}

        path = urlparse(self.path).path
        logger.info(f"[POST TRACE] Request Path: {path}")
        
        try:
            if path.rstrip('/') == '/api/login': return self.send_json(*handle_login(data))
            if path.rstrip('/') == '/api/rooms': return self.send_json(*handle_add_room(data))
            if path.startswith('/api/rooms/update/'):
                rid = int(path.split('/')[-1])
                return self.send_json(*handle_update_room(rid, data))
            if path.rstrip('/') == '/api/settings/update': return self.send_json(*handle_update_setting(data))
            
            if path == '/api/upload':
                return self.handle_upload()

            self.send_json(*json_response({"error": "Not found"}, 404))
        except Exception as e:
            logger.error(f"Error handling POST {path}: {e}")
            self.send_json(*json_response({"error": "Internal server error"}, 500))

    def handle_upload(self):
        try:
            content_type = self.headers.get('Content-Type')
            if not content_type or 'multipart/form-data' not in content_type:
                return self.send_json(*json_response({"error": "Invalid Content-Type"}, 400))
            
            boundary = content_type.split("boundary=")[1].encode()
            content_length = int(self.headers.get('Content-Length'))
            body = self.rfile.read(content_length)
            
            # More robust multipart parsing
            parts = body.split(b'--' + boundary)
            for part in parts:
                if b'filename="' in part:
                    # Extract filename and content
                    header_part, content = part.split(b'\r\n\r\n', 1)
                    filename = re.findall(r'filename="([^"]+)"', header_part.decode())[0]
                    # Remove trailing \r\n
                    content = content.rstrip(b'\r\n')
                    # Remove trailing --
                    if content.endswith(b'--'): content = content[:-2]
                    
                    upload_dir = os.path.join(os.path.dirname(__file__), 'uploads')
                    os.makedirs(upload_dir, exist_ok=True)
                    
                    # Sanitize filename
                    filename = "".join([c for c in filename if c.isalnum() or c in '._-']).strip()
                    save_path = os.path.join(upload_dir, filename)
                    
                    with open(save_path, 'wb') as f:
                        f.write(content)
                    
                    logger.info(f"File uploaded successfully: {filename}")
                    return self.send_json(*json_response({"success": True, "path": f"uploads/{filename}"}))
            
            return self.send_json(*json_response({"error": "No file found in multipart data"}, 400))
        except Exception as e:
            logger.error(f"Upload error: {e}")
            return self.send_json(*json_response({"error": str(e)}, 500))

    def do_DELETE(self):
        path = urlparse(self.path).path.rstrip('/')
        try:
            self.send_json(*json_response({"error": "Not found"}, 404))
        except Exception as e:
            logger.error(f"Error handling DELETE {path}: {e}")
            self.send_json(*json_response({"error": "Internal server error"}, 500))

if __name__ == '__main__':
    init_db()
    PORT = int(os.environ.get("PORT", 8080))
    server = ThreadingHTTPServer(('0.0.0.0', PORT), HomestayHandler)
    logger.info(f"Homestay Tokou running at http://0.0.0.0:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server stopping...")
        server.server_close()

