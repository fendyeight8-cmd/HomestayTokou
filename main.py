"""
main.py
FastAPI application — server-rendered pages + JSON API endpoints.
"""

import os
from datetime import date, datetime, timedelta
from typing import Optional

from fastapi import FastAPI, Request, Form, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from backend.models import get_db, init_db, BookingStatus
from backend import crud
from backend.whatsapp import build_wa_url, build_enquiry_url

# ─── App Setup ────────────────────────────────────────────────────────────────

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TMPL_DIR   = os.path.join(BASE_DIR, "templates")
ADMIN_DIR  = os.path.join(BASE_DIR, "admin_templates")

app = FastAPI(title="Rumah Alam Homestay", version="1.0.0", docs_url="/api/docs")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates       = Jinja2Templates(directory=TMPL_DIR)
admin_templates = Jinja2Templates(directory=ADMIN_DIR)

# Jinja2 globals
def add_globals(t: Jinja2Templates):
    t.env.globals["now"]      = datetime.utcnow
    t.env.globals["WA_NUMBER"] = "+601110085626"

add_globals(templates)
add_globals(admin_templates)


@app.on_event("startup")
def startup():
    init_db()
    os.makedirs(STATIC_DIR, exist_ok=True)


# ─── HELPERS ─────────────────────────────────────────────────────────────────

def base_context(request: Request, db: Session) -> dict:
    settings = crud.get_all_settings(db)
    return {
        "request":    request,
        "settings":   settings,
        "wa_number":  settings.get("whatsapp_number", "+601110085626"),
        "prop_name":  settings.get("property_name", "Rumah Alam"),
        "wa_enquiry": build_enquiry_url(),
        "rooms":      crud.get_rooms(db),   # available in footer for all pages
    }


# ═══════════════════════════════════════════════════════════════════════════════
# PUBLIC PAGES
# ═══════════════════════════════════════════════════════════════════════════════

@app.exception_handler(404)
async def not_found(request: Request, exc):
    db = next(get_db())
    ctx = base_context(request, db)
    return templates.TemplateResponse("404.html", ctx, status_code=404)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    ctx = base_context(request, db)
    ctx["reviews"] = crud.get_reviews(db)
    return templates.TemplateResponse("index.html", ctx)


@app.get("/rooms", response_class=HTMLResponse)
async def rooms_page(request: Request, db: Session = Depends(get_db)):
    ctx = base_context(request, db)
    return templates.TemplateResponse("rooms.html", ctx)


@app.get("/rooms/{slug}", response_class=HTMLResponse)
async def room_detail(slug: str, request: Request, db: Session = Depends(get_db)):
    room = crud.get_room_by_slug(db, slug)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    ctx = base_context(request, db)
    ctx["room"]    = room
    ctx["reviews"] = crud.get_room_reviews(db, room.id)
    ctx["booked"]  = crud.get_booked_dates(db, room.id)
    return templates.TemplateResponse("room_detail.html", ctx)


@app.get("/booking", response_class=HTMLResponse)
async def booking_page(request: Request,
                        room_slug: str = Query(default=""),
                        db: Session = Depends(get_db)):
    ctx = base_context(request, db)
    ctx["rooms"]      = crud.get_rooms(db)
    ctx["preselected"] = room_slug
    return templates.TemplateResponse("booking.html", ctx)


@app.get("/booking/confirm/{reference}", response_class=HTMLResponse)
async def booking_confirm(reference: str, request: Request,
                           db: Session = Depends(get_db)):
    booking = crud.get_booking_by_ref(db, reference)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    ctx = base_context(request, db)
    ctx["booking"] = booking
    ctx["wa_url"]  = build_wa_url(booking)
    return templates.TemplateResponse("booking_confirm.html", ctx)


# ═══════════════════════════════════════════════════════════════════════════════
# API ENDPOINTS (JSON)
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/api/rooms", response_class=JSONResponse)
async def api_rooms(db: Session = Depends(get_db)):
    rooms = crud.get_rooms(db)
    return [{"id": r.id, "slug": r.slug, "name": r.name,
             "price_night": r.price_night, "max_guests": r.max_guests,
             "gradient_css": r.gradient_css, "emoji": r.emoji,
             "amenities": r.amenities} for r in rooms]


@app.get("/api/availability/{room_id}", response_class=JSONResponse)
async def api_availability(room_id: int, db: Session = Depends(get_db)):
    return {"room_id": room_id, "booked_dates": crud.get_booked_dates(db, room_id)}


@app.get("/api/availability", response_class=JSONResponse)
async def api_availability_range(
    check_in:  str = Query(...),
    check_out: str = Query(...),
    db: Session = Depends(get_db)
):
    try:
        ci = date.fromisoformat(check_in)
        co = date.fromisoformat(check_out)
    except ValueError:
        raise HTTPException(400, "Invalid date format. Use YYYY-MM-DD")
    available = crud.get_available_rooms(db, ci, co)
    return {"available_room_ids": [r.id for r in available]}


@app.post("/api/bookings", response_class=JSONResponse)
async def api_create_booking(
    room_id:          int  = Form(...),
    first_name:       str  = Form(...),
    last_name:        str  = Form(...),
    phone:            str  = Form(...),
    email:            str  = Form(""),
    check_in:         str  = Form(...),
    check_out:        str  = Form(...),
    adults:           int  = Form(2),
    children:         int  = Form(0),
    special_requests: str  = Form(""),
    db: Session = Depends(get_db)
):
    try:
        ci = date.fromisoformat(check_in)
        co = date.fromisoformat(check_out)
    except ValueError:
        return JSONResponse({"error": "Invalid date format"}, status_code=400)

    if ci >= co:
        return JSONResponse({"error": "Check-out must be after check-in"}, status_code=400)
    if ci < date.today():
        return JSONResponse({"error": "Check-in cannot be in the past"}, status_code=400)

    guest = crud.get_or_create_guest(db, first_name, last_name, phone, email)
    booking = crud.create_booking(
        db, room_id=room_id, guest_id=guest.id,
        check_in=ci, check_out=co,
        adults=adults, children=children,
        special_requests=special_requests,
    )

    if not booking:
        return JSONResponse({"error": "Room not available for selected dates"}, status_code=409)

    wa_url = build_wa_url(booking)
    return JSONResponse({
        "success":   True,
        "reference": booking.reference,
        "wa_url":    wa_url,
        "redirect":  f"/booking/confirm/{booking.reference}",
        "nights":    booking.nights,
        "total":     booking.total_price,
    })


@app.get("/api/bookings/{reference}", response_class=JSONResponse)
async def api_get_booking(reference: str, db: Session = Depends(get_db)):
    b = crud.get_booking_by_ref(db, reference)
    if not b:
        raise HTTPException(404, "Not found")
    return {
        "reference": b.reference, "status": b.status,
        "room": b.room.name, "check_in": str(b.check_in),
        "check_out": str(b.check_out), "nights": b.nights,
        "total": b.total_price, "guest": b.guest.full_name,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# ADMIN PANEL
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    stats    = crud.get_dashboard_stats(db)
    bookings = crud.get_all_bookings(db)[:10]   # latest 10
    ctx = {
        "request":  request,
        "stats":    stats,
        "bookings": bookings,
        "page":     "dashboard",
    }
    return admin_templates.TemplateResponse("admin_dashboard.html", ctx)


@app.get("/admin/bookings", response_class=HTMLResponse)
async def admin_bookings(request: Request,
                          status: str = "",
                          db: Session = Depends(get_db)):
    bookings = crud.get_all_bookings(db, status=status or None)
    ctx = {"request": request, "bookings": bookings,
           "filter_status": status, "page": "bookings",
           "statuses": [s.value for s in BookingStatus]}
    return admin_templates.TemplateResponse("admin_bookings.html", ctx)


@app.post("/admin/bookings/{booking_id}/status")
async def admin_update_status(booking_id: int,
                               status: str = Form(...),
                               notes: str  = Form(""),
                               db: Session = Depends(get_db)):
    crud.update_booking_status(db, booking_id, status, notes)
    return RedirectResponse("/admin/bookings", status_code=303)


@app.get("/admin/rooms", response_class=HTMLResponse)
async def admin_rooms(request: Request, db: Session = Depends(get_db)):
    rooms = crud.get_rooms(db, active_only=False)
    ctx = {"request": request, "rooms": rooms, "page": "rooms"}
    return admin_templates.TemplateResponse("admin_rooms.html", ctx)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
