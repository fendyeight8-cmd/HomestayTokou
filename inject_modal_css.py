import re

css_to_add = """
    /* ── BOOKING MODAL & WIDGETS ── */
    .stepper { display: flex; justify-content: center; gap: 2rem; margin-bottom: 2.5rem; border-bottom: 1px solid var(--border-light); padding-bottom: 1.5rem; }
    .step { display: flex; flex-direction: column; align-items: center; opacity: 0.4; transition: var(--transition-med); }
    .step.active { opacity: 1; }
    .step-num { width: 35px; height: 35px; border-radius: 50%; background: transparent; border: 1px solid var(--primary-dark); display: flex; align-items: center; justify-content: center; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem; transition: var(--transition-med); }
    .step.active .step-num { background: var(--gold); color: var(--primary-dark); border-color: var(--gold); }
    .step-label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; font-weight: 600; }

    .booking-summary { background: var(--bg-cream); padding: 1.5rem; border-radius: 4px; margin-bottom: 2rem; display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
    .summary-item label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 2px; color: var(--text-muted); display: block; margin-bottom: 0.3rem; }
    .summary-item p { font-family: 'Cormorant Garamond', serif; font-size: 1.2rem; color: var(--primary-dark); }
    .summary-total { grid-column: 1 / -1; border-top: 1px solid rgba(18,16,14,0.1); padding-top: 1rem; display: flex; justify-content: space-between; align-items: center; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
    .summary-total span:last-child { color: var(--gold-dark); font-size: 1.5rem; }

    #booking-form-view .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 1.5rem; }
    #booking-form-view .form-group { margin-bottom: 1.5rem; }
    #booking-form-view .form-group input, #booking-form-view .form-group select, #booking-form-view .form-group textarea { width: 100%; background: transparent; border: none; border-bottom: 1px solid var(--border-light); padding: 0.8rem 0; font-family: 'Cormorant Garamond', serif; font-size: 1.2rem; outline: none; transition: var(--transition-fast); }
    #booking-form-view .form-group input:focus, #booking-form-view .form-group textarea:focus { border-color: var(--gold); }
    
    .btn-block { width: 100%; text-align: center; margin-bottom: 1rem; }

    /* QR View */
    .qr-container { display: none; text-align: center; }
    .qr-container.show { display: block; animation: fadeInUp 0.4s var(--transition-med); }
    .qr-card { background: #fff; padding: 3rem; border: 1px solid var(--border-light); margin-bottom: 2rem; }
    .qr-image { width: 250px; height: 250px; object-fit: contain; margin: 0 auto 2rem; display: block; border: 1px solid var(--border-light); padding: 1rem; }
    .payment-instruction { font-size: 0.9rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 2rem; }

    /* Confirmation */
    .confirmation { text-align: center; padding: 2rem 0; }
    .confirm-icon { width: 80px; height: 80px; border-radius: 50%; background: var(--gold); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; margin: 0 auto 2rem; }
    .confirm-details { background: var(--bg-cream); padding: 2rem; text-align: left; margin: 2rem 0; line-height: 1.8; }
    
    /* Room Tags */
    .room-amenities { display: flex; flex-wrap: wrap; gap: 0.5rem; justify-content: center; margin-bottom: 1.5rem; }
    .amenity-tag { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted); border: 1px solid var(--border-light); padding: 0.3rem 0.8rem; border-radius: 40px; }
"""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('</style>', f'{css_to_add}\n  </style>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Modal CSS injected successfully.")
