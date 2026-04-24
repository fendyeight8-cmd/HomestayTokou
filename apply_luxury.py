import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

luxury_css = """
    :root {
      /* Premium Luxury Palette */
      --primary-dark: #12100E;    /* Deep espresso/charcoal */
      --secondary-dark: #2A2522;  /* Rich walnut */
      --gold: #D4AF37;            /* Champagne Gold */
      --gold-light: #F3E5AB;      /* Light gold */
      --gold-dark: #AA8C2C;       /* Dark gold */
      --bg-light: #FBFBF9;        /* Warm Ivory */
      --bg-cream: #F4EFEA;        /* Cream */
      --accent-green: #2E4730;    /* Forest Green */
      --text-main: #2A2522;
      --text-muted: #6B6058;
      --border-light: rgba(42, 37, 34, 0.1);
      --border-dark: rgba(212, 175, 55, 0.3);
      --glass-bg: rgba(251, 251, 249, 0.85);
      
      --transition-slow: 0.8s cubic-bezier(0.25, 1, 0.5, 1);
      --transition-med: 0.4s cubic-bezier(0.25, 1, 0.5, 1);
      --transition-fast: 0.2s ease-out;
    }

    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    :focus-visible {
      outline: 1px solid var(--gold);
      outline-offset: 4px;
    }

    html {
      scroll-behavior: smooth;
      scroll-padding-top: 100px;
      font-size: 16px;
    }

    body {
      font-family: 'Inter', sans-serif;
      background: var(--bg-light);
      color: var(--text-main);
      overflow-x: hidden;
      -webkit-font-smoothing: antialiased;
    }

    /* ── TYPOGRAPHY ── */
    h1, h2, h3, h4, h5, .serif {
      font-family: 'Cormorant Garamond', serif;
      font-weight: 400;
      line-height: 1.2;
    }

    .section-label {
      font-family: 'Inter', sans-serif;
      font-size: 0.75rem;
      letter-spacing: 4px;
      text-transform: uppercase;
      color: var(--gold-dark);
      font-weight: 600;
      margin-bottom: 1.5rem;
      display: block;
    }

    .section-title {
      font-size: clamp(2.5rem, 5vw, 4rem);
      color: var(--primary-dark);
      margin-bottom: 1.5rem;
    }

    .section-sub {
      font-size: 1.1rem;
      color: var(--text-muted);
      max-width: 600px;
      line-height: 1.8;
      font-weight: 300;
    }

    /* ── NAV ── */
    nav {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      width: 100%;
      z-index: 1000;
      padding: 1.5rem 4rem;
      display: flex;
      align-items: center;
      background: transparent;
      transition: var(--transition-med);
      border-bottom: 1px solid transparent;
    }

    nav.scrolled {
      padding: 1rem 4rem;
      background: rgba(18, 16, 14, 0.95);
      backdrop-filter: blur(10px);
      border-bottom: 1px solid rgba(255,255,255,0.05);
    }

    .nav-logo {
      font-family: 'Cormorant Garamond', serif;
      font-size: 1.8rem;
      color: #fff;
      text-decoration: none;
      letter-spacing: 1px;
    }

    .nav-logo span {
      color: var(--gold);
    }

    .nav-links {
      display: flex;
      gap: 3rem;
      align-items: center;
      margin-left: auto;
      list-style: none;
    }

    .nav-links a {
      color: #fff;
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 2px;
      text-decoration: none;
      font-weight: 400;
      opacity: 0.8;
      transition: var(--transition-fast);
      position: relative;
    }

    .nav-links a:hover {
      opacity: 1;
      color: var(--gold);
    }

    .nav-links a::after {
      content: '';
      position: absolute;
      bottom: -4px;
      left: 0;
      width: 0;
      height: 1px;
      background: var(--gold);
      transition: var(--transition-med);
    }

    .nav-links a:hover::after {
      width: 100%;
    }

    .nav-cta {
      border: 1px solid var(--gold);
      padding: 0.75rem 2rem;
      border-radius: 0;
      color: var(--gold) !important;
    }
    
    .nav-cta::after { display: none !important; }

    .nav-cta:hover {
      background: var(--gold);
      color: var(--primary-dark) !important;
    }

    .menu-toggle { display: none; }

    /* ── HERO ── */
    .hero {
      position: relative;
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
      color: #fff;
      overflow: hidden;
    }

    .hero-bg-wrapper {
      position: absolute;
      inset: 0;
      z-index: -1;
    }

    .hero-bg {
      width: 100%;
      height: 110%;
      background: url('/images/hero-bg.jpg') center/cover no-repeat;
      transform: translateY(0);
      animation: slowZoom 20s ease-out forwards;
    }

    @keyframes slowZoom {
      0% { transform: scale(1); }
      100% { transform: scale(1.1); }
    }

    .hero-overlay {
      position: absolute;
      inset: 0;
      background: linear-gradient(to bottom, rgba(18,16,14,0.4) 0%, rgba(18,16,14,0.7) 100%);
      z-index: 0;
    }

    .hero-content {
      position: relative;
      z-index: 1;
      max-width: 900px;
      padding: 0 2rem;
      animation: fadeInUp 1.2s var(--transition-slow);
    }

    .hero-badge {
      font-size: 0.8rem;
      letter-spacing: 4px;
      text-transform: uppercase;
      color: var(--gold);
      margin-bottom: 2rem;
      display: inline-block;
      border-bottom: 1px solid var(--gold);
      padding-bottom: 0.5rem;
    }

    .hero h1 {
      font-size: clamp(3rem, 8vw, 6.5rem);
      line-height: 1.05;
      margin-bottom: 1.5rem;
      font-weight: 300;
    }

    .hero h1 em {
      font-style: italic;
      color: var(--gold);
      font-weight: 400;
    }

    .hero-btns {
      display: flex;
      gap: 1.5rem;
      justify-content: center;
      margin-top: 3rem;
    }

    /* ── BUTTONS ── */
    .btn-primary {
      background: var(--primary-dark);
      color: #fff;
      border: 1px solid var(--primary-dark);
      padding: 1rem 2.5rem;
      font-size: 0.85rem;
      text-transform: uppercase;
      letter-spacing: 2px;
      cursor: pointer;
      transition: var(--transition-med);
      text-decoration: none;
      display: inline-block;
    }

    .btn-primary:hover {
      background: var(--gold);
      border-color: var(--gold);
      color: var(--primary-dark);
    }

    .btn-outline {
      background: transparent;
      color: #fff;
      border: 1px solid rgba(255,255,255,0.4);
      padding: 1rem 2.5rem;
      font-size: 0.85rem;
      text-transform: uppercase;
      letter-spacing: 2px;
      cursor: pointer;
      transition: var(--transition-med);
      text-decoration: none;
      display: inline-block;
    }

    .btn-outline:hover {
      background: #fff;
      color: var(--primary-dark);
    }

    /* ── QUICK SEARCH ── */
    .quick-search {
      position: relative;
      margin-top: -80px;
      z-index: 10;
      padding: 0 5%;
    }

    .search-card {
      background: #fff;
      padding: 2.5rem 4rem;
      display: grid;
      grid-template-columns: 1fr 1fr 1fr auto;
      gap: 2.5rem;
      align-items: center;
      box-shadow: 0 30px 60px rgba(18, 16, 14, 0.08);
      max-width: 1200px;
      margin: 0 auto;
    }

    .form-group { display: flex; flex-direction: column; }
    .form-group label {
      font-size: 0.7rem;
      text-transform: uppercase;
      letter-spacing: 2px;
      color: var(--text-muted);
      margin-bottom: 0.8rem;
      font-weight: 600;
    }

    .form-group input, .form-group select {
      background: transparent;
      border: none;
      border-bottom: 1px solid var(--border-light);
      padding: 0.5rem 0;
      font-size: 1.1rem;
      font-family: 'Cormorant Garamond', serif;
      color: var(--primary-dark);
      cursor: pointer;
      transition: var(--transition-fast);
      appearance: none;
    }

    .form-group input:focus, .form-group select:focus {
      outline: none;
      border-bottom-color: var(--gold);
    }

    /* ── SECTIONS ── */
    section { padding: 8rem 5%; position: relative; }
    
    .section-header {
      text-align: center;
      margin-bottom: 5rem;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    /* ── ROOMS GRID ── */
    #rooms { background: var(--bg-light); }
    
    .rooms-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
      gap: 3rem;
      max-width: 1400px;
      margin: 0 auto;
    }

    .room-card {
      background: #fff;
      position: relative;
      overflow: hidden;
      transition: var(--transition-med);
      cursor: pointer;
    }

    .room-card:hover {
      box-shadow: 0 40px 80px rgba(18, 16, 14, 0.08);
      transform: translateY(-5px);
    }

    .room-img {
      position: relative;
      height: 450px;
      overflow: hidden;
    }

    .room-img img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 1.2s cubic-bezier(0.25, 1, 0.5, 1);
    }

    .room-card:hover .room-img img {
      transform: scale(1.08);
    }

    .room-avail {
      position: absolute;
      top: 1.5rem;
      right: 1.5rem;
      background: var(--glass-bg);
      backdrop-filter: blur(10px);
      padding: 0.5rem 1rem;
      font-size: 0.7rem;
      text-transform: uppercase;
      letter-spacing: 2px;
      font-weight: 600;
    }
    .room-avail.booked { background: rgba(18, 16, 14, 0.8); color: #fff; }

    .room-body {
      padding: 2.5rem 2rem;
      text-align: center;
    }

    .room-body .cat {
      font-size: 0.7rem;
      text-transform: uppercase;
      letter-spacing: 2px;
      color: var(--text-muted);
      margin-bottom: 0.5rem;
    }

    .room-body h3 {
      font-size: 2rem;
      color: var(--primary-dark);
      margin-bottom: 1rem;
    }

    .room-body .price {
      font-family: 'Inter', sans-serif;
      font-size: 1.2rem;
      color: var(--gold-dark);
    }

    /* ── ABOUT / FEATURES ── */
    #about { background: var(--bg-cream); }

    .features-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 4rem;
      margin-top: 5rem;
      max-width: 1400px;
      margin-inline: auto;
    }

    .feature-card {
      text-align: left;
    }

    .feature-image {
      height: 350px;
      margin-bottom: 2rem;
      overflow: hidden;
    }

    .feature-image img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: var(--transition-slow);
    }

    .feature-card:hover .feature-image img {
      transform: scale(1.05);
    }

    .feature-card h3 {
      font-size: 1.8rem;
      margin-bottom: 1rem;
      color: var(--primary-dark);
    }

    .feature-card p {
      color: var(--text-muted);
      line-height: 1.8;
      font-size: 0.95rem;
    }

    /* ── REVIEWS ── */
    #reviews { background: #fff; }

    .rating-overall {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-bottom: 4rem;
    }

    .rating-num {
      font-family: 'Cormorant Garamond', serif;
      font-size: 5rem;
      color: var(--primary-dark);
      line-height: 1;
    }

    .stars { color: var(--gold); font-size: 1.5rem; letter-spacing: 5px; margin: 1rem 0; }

    .reviews-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
      gap: 3rem;
      max-width: 1400px;
      margin: 0 auto;
    }

    .review-card {
      background: var(--bg-light);
      padding: 3rem;
      text-align: center;
      border: 1px solid var(--border-light);
    }

    .review-card p {
      font-family: 'Cormorant Garamond', serif;
      font-size: 1.4rem;
      font-style: italic;
      line-height: 1.6;
      color: var(--primary-dark);
      margin-bottom: 2rem;
    }

    .review-author {
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 2px;
      color: var(--text-muted);
      font-weight: 600;
    }

    /* ── FOOTER ── */
    footer {
      background: var(--primary-dark);
      color: #fff;
      padding: 6rem 5% 2rem;
    }

    .footer-grid {
      display: grid;
      grid-template-columns: 2fr 1fr 1fr;
      gap: 5rem;
      max-width: 1400px;
      margin: 0 auto 5rem;
    }

    .footer-brand .nav-logo { font-size: 2.5rem; }
    
    .footer-brand p {
      margin-top: 1.5rem;
      color: rgba(255,255,255,0.5);
      line-height: 1.8;
      max-width: 400px;
    }

    footer h4 {
      font-family: 'Inter', sans-serif;
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 2px;
      color: var(--gold);
      margin-bottom: 2rem;
    }

    footer ul { list-style: none; }
    footer ul li { margin-bottom: 1rem; }
    footer ul a, .contact-item {
      color: rgba(255,255,255,0.7);
      text-decoration: none;
      font-size: 0.95rem;
      transition: var(--transition-fast);
      display: block;
    }
    
    .contact-item { margin-bottom: 1rem; display: flex; align-items: center; gap: 1rem; }
    
    footer ul a:hover { color: #fff; transform: translateX(5px); }

    .footer-bottom {
      border-top: 1px solid rgba(255,255,255,0.1);
      padding-top: 2rem;
      display: flex;
      justify-content: space-between;
      color: rgba(255,255,255,0.4);
      font-size: 0.8rem;
      max-width: 1400px;
      margin: 0 auto;
    }

    /* ── ANIMATIONS ── */
    .luxury-reveal {
      opacity: 0;
      transform: translateY(40px);
      transition: opacity 1s ease-out, transform 1s cubic-bezier(0.25, 1, 0.5, 1);
    }
    
    .luxury-reveal.visible {
      opacity: 1;
      transform: translateY(0);
    }

    @keyframes fadeInUp {
      from { opacity: 0; transform: translateY(30px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* ── RESPONSIVE ── */
    @media (max-width: 1024px) {
      .search-card { grid-template-columns: 1fr 1fr; padding: 2rem; }
      .search-card .btn-primary { grid-column: 1 / -1; }
      .footer-grid { grid-template-columns: 1fr; gap: 3rem; }
    }
    @media (max-width: 768px) {
      nav { padding: 1rem 2rem; }
      .nav-links { display: none; }
      .menu-toggle { display: block; background: transparent; border: none; color: #fff; font-size: 1.5rem; cursor: pointer; }
      .hero h1 { font-size: 3rem; }
      .search-card { grid-template-columns: 1fr; padding: 1.5rem; }
      section { padding: 5rem 5%; }
    }
    
    /* MODAL AND OTHERS KEPT WORKING BUT RESTYLED */
    .modal-overlay {
      position: fixed; inset: 0; background: rgba(18,16,14,0.8); z-index: 2000;
      display: none; place-items: center; padding: 1rem; backdrop-filter: blur(5px);
    }
    .modal-overlay.open { display: grid; }
    .modal {
      background: var(--bg-light); width: 100%; max-width: 600px;
      max-height: 90vh; overflow-y: auto;
      box-shadow: 0 40px 100px rgba(0,0,0,0.5);
    }
    .modal-header {
      background: var(--primary-dark); color: #fff; padding: 2rem;
      display: flex; justify-content: space-between; align-items: center;
    }
    .modal-header h2 { color: #fff; font-size: 2rem; }
    .modal-close { background: transparent; border: none; color: #fff; font-size: 1.5rem; cursor: pointer; }
    .modal-body { padding: 2.5rem; }
    
    /* Toast */
    .toast {
      position: fixed; bottom: 2rem; right: 2rem; background: var(--primary-dark);
      color: #fff; padding: 1rem 2rem; z-index: 9999; transform: translateY(100px);
      opacity: 0; transition: var(--transition-med); border-left: 3px solid var(--gold);
    }
    .toast.show { transform: translateY(0); opacity: 1; }

    /* Lang dropdown */
    .lang-selector { position: relative; margin-left: 2rem; }
    .lang-btn { background: transparent; color: #fff; border: 1px solid rgba(255,255,255,0.3); padding: 0.5rem 1rem; cursor: pointer; }
    .lang-btn:hover { border-color: var(--gold); }
    .lang-dropdown { display: none; position: absolute; top: 100%; right: 0; background: #fff; color: var(--primary-dark); width: 150px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-top: 0.5rem; }
    .lang-dropdown.show { display: block; }
    .lang-option { padding: 0.8rem 1rem; cursor: pointer; font-size: 0.8rem; }
    .lang-option:hover { background: var(--bg-cream); color: var(--gold); }
    
    .spinner { border: 2px solid var(--border-light); border-top-color: var(--gold); width: 30px; height: 30px; border-radius: 50%; animation: spin 1s linear infinite; margin: 2rem auto; }
    @keyframes spin { to { transform: rotate(360deg); } }
"""

# Replace the style block
html = re.sub(r'<style>.*?</style>', f'<style>\n{luxury_css}\n  </style>', html, flags=re.DOTALL)

# Add hero overlay
html = html.replace('<div class="hero-bg-wrapper">', '<div class="hero-overlay"></div>\n    <div class="hero-bg-wrapper">')

# Modify nav buttons
html = html.replace('class="menu-toggle"', 'class="menu-toggle" style="color:white;"')

# Adjust feature image classes (remove the small border-radius)
html = html.replace('class="feature-image"', 'class="feature-image luxury-reveal"')

# Make sure review cards use luxury-reveal
html = html.replace('class="review-card"', 'class="review-card luxury-reveal"')

# Modify Rooms header layout
html = html.replace('<div class="rooms-header">', '<div class="section-header luxury-reveal">')
html = html.replace('<h2 class="section-title" data-t="section_rooms_title">Our Rooms & Suites</h2>', '<h2 class="section-title" data-t="section_rooms_title">Our Rooms & Suites</h2>')
html = html.replace('<div style="max-width:900px; margin: 0 auto; text-align: center;">', '<div class="section-header luxury-reveal">')

html = html.replace('<div class="reviews-header">', '<div class="section-header luxury-reveal">')

# Save changes
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html CSS successfully.")
