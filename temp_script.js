
            /**
             * Homestay Tokou - Main Application Script
             * A professional, modular implementation for a high-conversion booking platform.
             */

            const CONFIG = {
              API_BASE: '',
              CURRENCY: 'RM',
              DATE_LOCALE: 'en-MY',
              TOAST_DURATION: 3500
            };

            // â”€â”€â”€ API Service â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
            const ApiService = {
              async fetchRooms(params = {}) {
                const query = new URLSearchParams(params).toString();
                const response = await fetch(`${CONFIG.API_BASE}/api/rooms${query ? '?' + query : ''}`);
                if (!response.ok) throw new Error('Failed to fetch rooms');
                return await response.json();
              },

              async fetchReviews() {
                const response = await fetch(`${CONFIG.API_BASE}/api/reviews`);
                if (!response.ok) throw new Error('Failed to fetch reviews');
                return await response.json();
              }
            };

            // â”€â”€â”€ Language & Translation â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
            const LangService = {
              current: 'en',

              translations: {
                en: {
                  flag: 'EN', label: 'EN',
                  nav_rooms: "Rooms", nav_about: "About", nav_reviews: "Reviews", nav_booking: "My Booking", nav_book_now: "Book Now",
                  hero_badge: "Authentic Sabahan Retreat", hero_title: "Homestay<br><em>Tokou</em>", hero_p: "Immerse yourself in the raw beauty of North Borneo, where traditional Sabahan hospitality meets the tranquil outskirts of Beluran's lush wilderness.",
                  hero_btn_rooms: "Explore Rooms", hero_btn_about: "Our Story", hero_scroll: "Scroll",
                  search_checkin: "Check In", search_checkout: "Check Out", search_guests: "Guests", search_btn: "Check Availability",
                  section_rooms_label: "Accommodation", section_rooms_title: "Our Rooms & Suites", section_rooms_sub: "Thoughtfully designed spaces blending local heritage with modern comfort.",
                  section_about_label: "Why Choose Us", section_about_title: "A Home Away From Home", section_about_sub: "Nestled in the heart of Sapi-Nangoh, Sabah, our homestay offers more than just a place to stay itâ€™s an invitation to slow down and truly experience rural life. Surrounded by lush landscapes and the rhythms of nature, we blend authentic local living with thoughtful comfort. Whether youâ€™re here to unwind, explore, or connect with the community, every stay is designed to be simple, warm, and meaningful.",
                  feature_authentic_title: "Authentic Experience", feature_authentic_p: "Live like a local with traditional Malay architecture and genuine warm hospitality.",
                  feature_meals_title: "Home-Cooked Meals", feature_meals_p: "Wake up to a delicious Malaysian breakfast prepared with fresh local ingredients.",
                  feature_nature_title: "Nature Surroundings", feature_nature_p: "Surrounded by lush greenery and paddy fields â€” perfect for relaxation.",
                  feature_service_title: "Personalised Service", feature_service_p: "As a family-run homestay, every guest receives dedicated attention.",
                  lookup_title: "Find Your Reservation", lookup_sub: "Enter your booking reference to manage your reservation.", lookup_ref: "Booking Reference", lookup_btn: "Find Booking",
                  footer_desc: "A family-run homestay offering authentic Malaysian kampung experience with warm hospitality.",
                  reviews_label: "Guest Reviews", reviews_title: "What Our Guests Say",
                  room_night: "/ night", btn_book_now: "Book Now", btn_unavailable: "Unavailable", badge_available: "âœ“ Available", badge_booked: "âœ— Booked"
                },
                ms: {
                  flag: 'MY', label: 'MS',
                  nav_rooms: "Bilik", nav_about: "Tentang", nav_reviews: "Ulasan", nav_booking: "Tempahan", nav_book_now: "Tempah",
                  hero_badge: "Percutian Autentik Sabah", hero_title: "Inap Desa<br><em>Tokou</em>", hero_p: "Alami keindahan asli Borneo Utara, di mana kemesraan hospitaliti tradisi Sabah bertemu dengan ketenangan alam semula jadi di pinggir Beluran.",
                  hero_btn_rooms: "Lihat Bilik", hero_btn_about: "Kisah Kami", hero_scroll: "Skrol",
                  search_checkin: "Tarikh Masuk", search_checkout: "Tarikh Keluar", search_guests: "Tetamu", search_btn: "Semak Kekosongan",
                  section_rooms_label: "Penginapan", section_rooms_title: "Bilik & Suit Kami", section_rooms_sub: "Ruang yang direka khas menggabungkan warisan tempatan dengan keselesaan moden.",
                  section_about_label: "Kenapa Pilih Kami", section_about_title: "Rumah Di Luar Rumah", section_about_sub: "Homestay Tokou menawarkan pengalaman Malaysia yang tulen â€” dari sarapan kampung hingga budaya tempatan.",
                  feature_authentic_title: "Pengalaman Autentik", feature_authentic_p: "Alami kehidupan kampung dengan seni bina tradisional dan keramahan sebenar.",
                  feature_meals_title: "Makanan Tradisional", feature_meals_p: "Nikmati sarapan Malaysia yang lazat yang disediakan dengan bahan tempatan segar.",
                  feature_nature_title: "Suasana Alam", feature_nature_p: "Dikelilingi oleh kehijauan dan sawah padi â€” sesuai untuk berehat.",
                  feature_service_title: "Servis Peribadi", feature_service_p: "Sebagai homestay keluarga, setiap tetamu menerima perhatian khusus.",
                  lookup_title: "Cari Tempahan Anda", lookup_sub: "Masukkan rujukan tempahan untuk menguruskan tempahan anda.", lookup_ref: "Rujukan Tempahan", lookup_btn: "Cari Tempahan",
                  footer_desc: "Inap desa keluarga yang menawarkan pengalaman kampung Malaysia yang tulen dengan layanan mesra.",
                  reviews_label: "Ulasan Tetamu", reviews_title: "Apa Kata Tetamu Kami",
                  room_night: "/ malam", btn_book_now: "Tempah Sekarang", btn_unavailable: "Penuh", badge_available: "âœ“ Tersedia", badge_booked: "âœ— Habis"
                },
                zh: {
                  flag: 'CN', label: 'ZH',
                  nav_rooms: "å®¢æˆ¿", nav_about: "å…³äºŽ", nav_reviews: "è¯„ä»·", nav_booking: "æˆ‘çš„é¢„è®¢", nav_book_now: "ç«‹å³é¢„è®¢",
                  hero_badge: "æ­£å®—é©¬æ¥è¥¿äºšåº¦å‡èƒœåœ°", hero_title: "Tokou<br><em>æ°‘å®¿</em>", hero_p: "åœ¨è‡ªç„¶ä¸­å¿ƒä½“éªŒä¼ ç»Ÿé©¬æ¥è¥¿äºšæ¬¾å¾…çš„çƒ­æƒ…ã€‚",
                  hero_btn_rooms: "æŽ¢ç´¢å®¢æˆ¿", hero_btn_about: "æˆ‘ä»¬çš„æ•…äº‹", hero_scroll: "æ»šåŠ¨",
                  search_checkin: "å…¥ä½æ—¥æœŸ", search_checkout: "é€€æˆ¿æ—¥æœŸ", search_guests: "äººæ•°", search_btn: "æ£€æŸ¥ç©ºæˆ¿",
                  section_rooms_label: "ä½å®¿", section_rooms_title: "å®¢æˆ¿ä¸Žå¥—æˆ¿", section_rooms_sub: "ç²¾å¿ƒè®¾è®¡çš„ç©ºé—´ï¼Œèžåˆäº†å½“åœ°é—äº§ä¸ŽçŽ°ä»£èˆ’é€‚ã€‚",
                  section_about_label: "ä¸ºä»€ä¹ˆé€‰æ‹©æˆ‘ä»¬", section_about_title: "å®¾è‡³å¦‚å½’", section_about_sub: "Homestay Tokou æä¾›æ­£å®—çš„é©¬æ¥è¥¿äºšä½“éªŒ â€” ä»Žå®¶å¸¸æ—©é¤åˆ°æ‘åº„æ¼«æ­¥ã€‚",
                  feature_authentic_title: "åœ°é“ä½“éªŒ", feature_authentic_p: "ä½“éªŒä¼ ç»Ÿé©¬æ¥å»ºç­‘é£Žæ ¼çš„ä¹¡æ‘ç”Ÿæ´»å’ŒçœŸè¯šçš„æ¬¾å¾…ã€‚",
                  feature_meals_title: "å®¶å¸¸ç¾Žé£Ÿ", feature_meals_p: "äº«ç”¨ç”±æ–°é²œå½“åœ°é£Ÿæäº²æ‰‹åˆ¶ä½œçš„ç¾Žå‘³é©¬æ¥è¥¿äºšæ—©é¤ã€‚",
                  feature_nature_title: "è‡ªç„¶çŽ¯æŠ±", feature_nature_p: "çŽ¯ç»•åœ¨éƒéƒè‘±è‘±çš„ç»¿æ„å’Œç¨»ç”°ä¹‹ä¸­ â€” æ”¾æ¾èº«å¿ƒçš„ç†æƒ³åœºæ‰€ã€‚",
                  feature_service_title: "ä¸ªæ€§åŒ–æœåŠ¡", feature_service_p: "ä½œä¸ºå®¶åº­ç»è¥çš„æ°‘å®¿ï¼Œæ¯ä½å®¢äººéƒ½å°†èŽ·å¾—ç»†è‡´å…¥å¾®çš„ç…§é¡¾ã€‚",
                  lookup_title: "æŸ¥æ‰¾æ‚¨çš„é¢„è®¢", lookup_sub: "è¾“å…¥æ‚¨çš„é¢„è®¢ç¼–å·ä»¥ç®¡ç†æ‚¨çš„é¢„è®¢ã€‚", lookup_ref: "é¢„è®¢ç¼–å·", lookup_btn: "æŸ¥æ‰¾é¢„è®¢",
                  footer_desc: "å®¶åº­ç»è¥çš„æ°‘å®¿ï¼Œæä¾›æ­£å®—çš„é©¬æ¥è¥¿äºšä¹¡æ‘ä½“éªŒå’Œçƒ­æƒ…çš„æ¬¾å¾…ã€‚",
                  reviews_label: "å®¢è¯„", reviews_title: "æˆ¿å®¢çš„è¯„ä»·",
                  room_night: "/ æ¯æ™š", btn_book_now: "ç«‹å³é¢„è®¢", btn_unavailable: "å·²æ»¡", badge_available: "âœ“ æœ‰æˆ¿", badge_booked: "âœ— å·²æ»¡"
                },
                in: {
                  flag: 'IN', label: 'IN',
                  nav_rooms: "à®…à®±à¯ˆà®•à®³à¯", nav_about: "à®ªà®±à¯à®±à®¿", nav_reviews: "à®®à®¤à®¿à®ªà¯à®ªà¯à®°à¯ˆà®•à®³à¯", nav_booking: "à®Žà®©à®¤à¯ à®®à¯à®©à¯à®ªà®¤à®¿à®µà¯", nav_book_now: "à®®à¯à®©à¯à®ªà®¤à®¿à®µà¯",
                  hero_badge: "à®…à®šà®²à¯ à®®à®²à¯‡à®šà®¿à®¯ à®¤à®™à¯à®•à¯à®®à®¿à®Ÿà®®à¯", hero_title: "à®¤à®™à¯à®•à¯à®®à®¿à®Ÿà®®à¯<br><em>Tokou</em>", hero_p: "à®‡à®¯à®±à¯à®•à¯ˆà®¯à®¿à®©à¯ à®‡à®¤à®¯à®¤à¯à®¤à®¿à®²à¯ à®®à®²à¯‡à®šà®¿à®¯ à®µà®¿à®°à¯à®¨à¯à®¤à¯‹à®®à¯à®ªà®²à®¿à®©à¯ à®µà¯†à®ªà¯à®ªà®¤à¯à®¤à¯ˆ à®…à®©à¯à®ªà®µà®¿à®•à¯à®•à®µà¯à®®à¯.",
                  hero_btn_rooms: "à®…à®±à¯ˆà®•à®³à¯ˆ à®†à®°à®¾à®¯à¯à®™à¯à®•à®³à¯", hero_btn_about: "à®Žà®™à¯à®•à®³à¯ à®•à®¤à¯ˆ", hero_scroll: "à®‰à®°à¯à®Ÿà¯à®Ÿà®µà¯à®®à¯",
                  search_checkin: "à®µà®°à¯à®•à¯ˆ", search_checkout: "à®µà¯†à®³à®¿à®¯à¯‡à®±à®²à¯", search_guests: "à®µà®¿à®°à¯à®¨à¯à®¤à®¿à®©à®°à¯à®•à®³à¯", search_btn: "à®•à®¿à®Ÿà¯ˆà®•à¯à®•à®¿à®±à®¤à®¾ à®Žà®© à®šà®°à®¿à®ªà®¾à®°à¯à®•à¯à®•à®µà¯à®®à¯",
                  section_rooms_label: "à®¤à®™à¯à®•à¯à®®à®¿à®Ÿà®®à¯", section_rooms_title: "à®Žà®™à¯à®•à®³à¯ à®…à®±à¯ˆà®•à®³à¯", section_rooms_sub: "à®‰à®³à¯à®³à¯‚à®°à¯ à®ªà®¾à®°à®®à¯à®ªà®°à®¿à®¯à®¤à¯à®¤à¯ˆ à®¨à®µà¯€à®© à®µà®šà®¤à®¿à®¯à¯à®Ÿà®©à¯ à®‡à®£à¯ˆà®•à¯à®•à¯à®®à¯ à®µà®Ÿà®¿à®µà®®à¯ˆà®•à¯à®•à®ªà¯à®ªà®Ÿà¯à®Ÿ à®‡à®Ÿà®™à¯à®•à®³à¯.",
                  section_about_label: "à®à®©à¯ à®Žà®™à¯à®•à®³à¯ˆ à®¤à¯‡à®°à¯à®µà¯ à®šà¯†à®¯à¯à®¯ à®µà¯‡à®£à¯à®Ÿà¯à®®à¯", section_about_title: "à®µà¯€à®Ÿà¯à®Ÿà®¿à®±à¯à®•à¯ à®µà¯†à®³à®¿à®¯à¯‡ à®’à®°à¯ à®µà¯€à®Ÿà¯", section_about_sub: "Homestay Tokou à®…à®šà®²à¯ à®®à®²à¯‡à®šà®¿à®¯ à®…à®©à¯à®ªà®µà®¤à¯à®¤à¯ˆ à®µà®´à®™à¯à®•à¯à®•à®¿à®±à®¤à¯.",
                  feature_authentic_title: "à®…à®šà®²à¯ à®…à®©à¯à®ªà®µà®®à¯", feature_authentic_p: "à®ªà®¾à®°à®®à¯à®ªà®°à®¿à®¯ à®•à®Ÿà¯à®Ÿà®¿à®Ÿà®•à¯à®•à®²à¯ˆ à®®à®±à¯à®±à¯à®®à¯ à®‰à®£à¯à®®à¯ˆà®¯à®¾à®© à®µà®¿à®°à¯à®¨à¯à®¤à¯‹à®®à¯à®ªà®²à¯à®Ÿà®©à¯ à®•à®¿à®°à®¾à®®à®¤à¯à®¤à¯ à®µà®¾à®´à¯à®•à¯à®•à¯ˆà®¯à¯ˆ à®…à®©à¯à®ªà®µà®¿à®•à¯à®•à®µà¯à®®à¯.",
                  feature_meals_title: "à®µà¯€à®Ÿà¯à®Ÿà¯ à®‰à®£à®µà¯", feature_meals_p: "à®‰à®³à¯à®³à¯‚à®°à¯ à®ªà¯Šà®°à¯à®Ÿà¯à®•à®³à®¾à®²à¯ à®¤à®¯à®¾à®°à®¿à®•à¯à®•à®ªà¯à®ªà®Ÿà¯à®Ÿ à®šà¯à®µà¯ˆà®¯à®¾à®© à®®à®²à¯‡à®šà®¿à®¯ à®•à®¾à®²à¯ˆ à®‰à®£à®µà¯ˆ à®…à®©à¯à®ªà®µà®¿à®•à¯à®•à®µà¯à®®à¯.",
                  feature_nature_title: "à®‡à®¯à®±à¯à®•à¯ˆ à®šà¯‚à®´à®²à¯", feature_nature_p: "à®ªà®šà¯à®®à¯ˆ à®®à®±à¯à®±à¯à®®à¯ à®¨à¯†à®²à¯ à®µà®¯à®²à¯à®•à®³à®¾à®²à¯ à®šà¯‚à®´à®ªà¯à®ªà®Ÿà¯à®Ÿà¯à®³à¯à®³à®¤à¯ â€” à®“à®¯à¯à®µà¯†à®Ÿà¯à®•à¯à®• à®šà®¿à®±à®¨à¯à®¤à®¤à¯.",
                  feature_service_title: "à®¤à®©à®¿à®ªà¯à®ªà®¯à®©à®¾à®•à¯à®•à®ªà¯à®ªà®Ÿà¯à®Ÿ à®šà¯‡à®µà¯ˆ", feature_service_p: "à®’à®µà¯à®µà¯Šà®°à¯ à®µà®¿à®°à¯à®¨à¯à®¤à®¿à®©à®°à¯à®®à¯ à®ªà®¿à®°à®¤à¯à®¯à¯‡à®• à®•à®µà®©à®¤à¯à®¤à¯ˆà®ªà¯ à®ªà¯†à®±à¯à®•à®¿à®±à®¾à®°à¯à®•à®³à¯.",
                  lookup_title: "à®‰à®™à¯à®•à®³à¯ à®®à¯à®©à¯à®ªà®¤à®¿à®µà¯ˆà®•à¯ à®•à®£à¯à®Ÿà®±à®¿à®¯à®µà¯à®®à¯", lookup_sub: "à®‰à®™à¯à®•à®³à¯ à®®à¯à®©à¯à®ªà®¤à®¿à®µà¯ˆ à®¨à®¿à®°à¯à®µà®•à®¿à®•à¯à®• à®‰à®™à¯à®•à®³à¯ à®®à¯à®©à¯à®ªà®¤à®¿à®µà¯ à®Žà®£à¯à®£à¯ˆ à®‰à®³à¯à®³à®¿à®Ÿà®µà¯à®®à¯.", lookup_ref: "à®®à¯à®©à¯à®ªà®¤à®¿à®µà¯ à®Žà®£à¯", lookup_btn: "à®®à¯à®©à¯à®ªà®¤à®¿à®µà¯ˆà®•à¯ à®•à®£à¯à®Ÿà¯à®ªà®¿à®Ÿà®¿",
                  footer_desc: "à®•à¯à®Ÿà¯à®®à¯à®ªà®¤à¯à®¤à®¿à®©à®¾à®²à¯ à®¨à®Ÿà®¤à¯à®¤à®ªà¯à®ªà®Ÿà¯à®®à¯ à®¤à®™à¯à®•à¯à®®à®¿à®Ÿà®®à¯, à®‰à®£à¯à®®à¯ˆà®¯à®¾à®© à®®à®²à¯‡à®šà®¿à®¯ à®…à®©à¯à®ªà®µà®¤à¯à®¤à¯ˆà®¯à¯à®®à¯ à®µà®¿à®°à¯à®¨à¯à®¤à¯‹à®®à¯à®ªà®²à¯ˆà®¯à¯à®®à¯ à®µà®´à®™à¯à®•à¯à®•à®¿à®±à®¤à¯.",
                  reviews_label: "à®µà®¿à®°à¯à®¨à¯à®¤à®¿à®©à®°à¯ à®®à®¤à®¿à®ªà¯à®ªà¯à®°à¯ˆà®•à®³à¯", reviews_title: "à®Žà®™à¯à®•à®³à¯ à®µà®¿à®°à¯à®¨à¯à®¤à®¿à®©à®°à¯à®•à®³à¯ à®Žà®©à¯à®© à®šà¯Šà®²à¯à®•à®¿à®±à®¾à®°à¯à®•à®³à¯",
                  room_night: "/ à®‡à®°à®µà¯", btn_book_now: "à®‡à®ªà¯à®ªà¯‹à®¤à¯ à®ªà®¤à®¿à®µà¯ à®šà¯†à®¯à¯à®¯à¯à®™à¯à®•à®³à¯", btn_unavailable: "à®‡à®²à¯à®²à¯ˆ", badge_available: "âœ“ à®‰à®³à¯à®³à®¤à¯", badge_booked: "âœ— à®‡à®²à¯à®²à¯ˆ"
                },
                ko: {
                  flag: 'KR', label: 'KO',
                  nav_rooms: "ê°ì‹¤", nav_about: "ì†Œê°œ", nav_reviews: "í›„ê¸°", nav_booking: "ì˜ˆì•½ í™•ì¸", nav_book_now: "ì§€ê¸ˆ ì˜ˆì•½",
                  hero_badge: "ì§„ì •í•œ ë§ë ˆì´ì‹œì•„ íœ´ì–‘ì§€", hero_title: "í™ˆìŠ¤í…Œì´<br><em>Tokou</em>", hero_p: "ìžì—°ì˜ í’ˆ ì•ˆì—ì„œ ì „í†µ ë§ë ˆì´ì‹œì•„ í™˜ëŒ€ì˜ ë”°ëœ»í•¨ì„ ê²½í—˜í•´ ë³´ì„¸ìš”.",
                  hero_btn_rooms: "ê°ì‹¤ ë‘˜ëŸ¬ë³´ê¸°", hero_btn_about: "ìš°ë¦¬ì˜ ì´ì•¼ê¸°", hero_scroll: "ìŠ¤í¬ë¡¤",
                  search_checkin: "ì²´í¬ì¸", search_checkout: "ì²´í¬ì•„ì›ƒ", search_guests: "ì¸ì›", search_btn: "ì˜ˆì•½ ê°€ëŠ¥ ì—¬ë¶€ í™•ì¸",
                  section_rooms_label: "ìˆ™ë°• ì‹œì„¤", section_rooms_title: "ê°ì‹¤ ë° ìŠ¤ìœ„íŠ¸", section_rooms_sub: "í˜„ì§€ ìœ ì‚°ê³¼ í˜„ëŒ€ì ì¸ íŽ¸ì•ˆí•¨ì´ ì–´ìš°ëŸ¬ì§„ ì„¸ì‹¬í•˜ê²Œ ì„¤ê³„ëœ ê³µê°„.",
                  section_about_label: "ì„ íƒ ì´ìœ ", section_about_title: "ì§‘ì²˜ëŸ¼ íŽ¸ì•ˆí•œ ê³³", section_about_sub: "Tokou í™ˆìŠ¤í…Œì´ëŠ” ì •í†µ ë§ë ˆì´ì‹œì•„ ê²½í—˜ì„ ì œê³µí•©ë‹ˆë‹¤.",
                  feature_authentic_title: "ì •í†µ ì²´í—˜", feature_authentic_p: "ì „í†µ ê±´ì¶•ë¬¼ê³¼ ì§„ì •í•œ í™˜ëŒ€ë¡œ í˜„ì§€ì¸ì²˜ëŸ¼ ìƒí™œí•´ ë³´ì„¸ìš”.",
                  feature_meals_title: "ê°€ì •ì‹ ì‹ì‚¬", feature_meals_p: "ì‹ ì„ í•œ ìž¬ë£Œë¡œ ì •ì„±ê» ì¤€ë¹„í•œ ë§›ìžˆëŠ” ë§ë ˆì´ì‹œì•„ì‹ ì¡°ì‹ì„ ì¦ê²¨ë³´ì„¸ìš”.",
                  feature_nature_title: "ìžì—° í™˜ê²½", feature_nature_p: "ë¬´ì„±í•œ ë…¹ìŒê³¼ ë…¼ìœ¼ë¡œ ë‘˜ëŸ¬ì‹¸ì—¬ íœ´ì‹ì— ì™„ë²½í•œ ìž¥ì†Œìž…ë‹ˆë‹¤.",
                  feature_service_title: "ê°œì¸í™”ëœ ì„œë¹„ìŠ¤", feature_service_p: "ëª¨ë“  íˆ¬ìˆ™ê°ì—ê²Œ ì„¸ì‹¬í•œ ë°°ë ¤ì™€ ì„œë¹„ìŠ¤ë¥¼ ì œê³µí•©ë‹ˆë‹¤.",
                  lookup_title: "ì˜ˆì•½ ì°¾ê¸°", lookup_sub: "ì˜ˆì•½ì„ ê´€ë¦¬í•˜ë ¤ë©´ ì˜ˆì•½ ë²ˆí˜¸ë¥¼ ìž…ë ¥í•˜ì„¸ìš”.", lookup_ref: "ì˜ˆì•½ ë²ˆí˜¸", lookup_btn: "ì˜ˆì•½ ì°¾ê¸°",
                  footer_desc: "ì •í†µ ë§ë ˆì´ì‹œì•„ ìº„í’ ì²´í—˜ê³¼ ë”°ëœ»í•œ í™˜ëŒ€ë¥¼ ì œê³µí•˜ëŠ” ê°€ì¡± ê²½ì˜ í™ˆìŠ¤í…Œì´ìž…ë‹ˆë‹¤.",
                  reviews_label: "íˆ¬ìˆ™ê° í›„ê¸°", reviews_title: "íˆ¬ìˆ™ê°ë“¤ì˜ ì´ì•¼ê¸°",
                  room_night: "/ 1ë°•", btn_book_now: "ì§€ê¸ˆ ì˜ˆì•½", btn_unavailable: "ì˜ˆì•½ ë¶ˆê°€", badge_available: "âœ“ ì˜ˆì•½ ê°€ëŠ¥", badge_booked: "âœ— ì˜ˆì•½ ì™„ë£Œ"
                },
                fr: {
                  flag: 'FR', label: 'FR',
                  nav_rooms: "Chambres", nav_about: "Ã€ Propos", nav_reviews: "Avis", nav_booking: "Mes RÃ©servations", nav_book_now: "RÃ©server",
                  hero_badge: "Retraite Malaise Authentique", hero_title: "Homestay<br><em>Tokou</em>", hero_p: "DÃ©couvrez la chaleur de l'hospitalitÃ© malaise traditionnelle au cÅ“ur de la nature.",
                  hero_btn_rooms: "Explorer", hero_btn_about: "Notre Histoire", hero_scroll: "DÃ©filer",
                  search_checkin: "ArrivÃ©e", search_checkout: "DÃ©part", search_guests: "InvitÃ©s", search_btn: "DisponibilitÃ©",
                  section_rooms_label: "HÃ©bergement", section_rooms_title: "Nos Chambres", section_rooms_sub: "Des espaces conÃ§us alliant patrimoine local et confort moderne.",
                  section_about_label: "Pourquoi Nous", section_about_title: "Comme Ã  la Maison", section_about_sub: "Homestay Tokou offre une expÃ©rience malaise authentique.",
                  feature_authentic_title: "ExpÃ©rience Authentique", feature_authentic_p: "Vivez comme un local avec l'architecture traditionnelle et l'accueil chaleureux.",
                  feature_meals_title: "Repas Maison", feature_meals_p: "Savourez un dÃ©licieux petit-dÃ©jeuner malais prÃ©parÃ© avec des ingrÃ©dients frais.",
                  feature_nature_title: "Nature", feature_nature_p: "EntourÃ© de verdure et de riziÃ¨res â€” parfait pour la relaxation.",
                  feature_service_title: "Service PersonnalisÃ©", feature_service_p: "Chaque invitÃ© reÃ§oit une attention dÃ©diÃ©e.",
                  lookup_title: "Trouver Votre RÃ©servation", lookup_sub: "Entrez votre rÃ©fÃ©rence pour gÃ©rer votre rÃ©servation.", lookup_ref: "RÃ©fÃ©rence de RÃ©servation", lookup_btn: "Trouver",
                  footer_desc: "Un homestay familial offrant une expÃ©rience authentique malaise avec un accueil chaleureux.",
                  reviews_label: "Avis Clients", reviews_title: "Ce que Disent Nos Clients",
                  room_night: "/ nuit", btn_book_now: "RÃ©server", btn_unavailable: "Indisponible", badge_available: "âœ“ Disponible", badge_booked: "âœ— Complet"
                }
              },

              init() {
                const saved = localStorage.getItem('preferred_lang') || 'en';
                this.set(saved);
              },

              set(lang) {
                if (!this.translations[lang]) return;
                this.current = lang;
                const t = this.translations[lang];

                // Update UI Flags
                const flagEl = document.getElementById('current-lang-flag');
                const labelEl = document.getElementById('current-lang-label');
                if (flagEl) flagEl.textContent = t.flag;
                if (labelEl) labelEl.textContent = t.label;

                // Apply translations
                document.querySelectorAll('[data-t]').forEach(el => {
                  const key = el.getAttribute('data-t');
                  if (t[key]) {
                    if (key.includes('title') && t[key].includes('<br>')) {
                      el.innerHTML = t[key];
                    } else {
                      el.textContent = t[key];
                    }
                  }
                });

                // Active dropdown state
                document.querySelectorAll('.lang-option').forEach(opt => {
                  opt.classList.toggle('active', opt.getAttribute('onclick').includes(lang));
                });

                localStorage.setItem('preferred_lang', lang);
                if (window.App && App.allRooms.length) {
                  App.renderRooms(App.allRooms);
                } else {
                  // If no rooms yet, still attach observer for static elements
                  this.attachRevealObserver();
                }
              },

              attachRevealObserver() {
                const obs = new IntersectionObserver((entries) => {
                  entries.forEach(entry => {
                    if (entry.isIntersecting) entry.target.classList.add('active');
                  });
                }, { threshold: 0.1 });
                document.querySelectorAll('.reveal').forEach(el => obs.observe(el));
              }
            };

            // â”€â”€â”€ UI Controller â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
            const UI = {
              elements: {
                navbar: document.getElementById('navbar'),
                roomsGrid: document.getElementById('rooms-grid'),
                reviewsGrid: document.getElementById('reviews-grid'),
                toast: document.getElementById('toast'),
                modalOverlay: document.getElementById('modal-overlay'),
                modalBody: document.getElementById('modal-body'),
                lookupResult: document.getElementById('lookup-result')
              },

              showToast(msg, type = '') {
                const t = this.elements.toast;
                t.textContent = msg;
                t.className = `toast show ${type}`;
                setTimeout(() => t.className = 'toast', CONFIG.TOAST_DURATION);
              },

              toggleModal(show) {
                this.elements.modalOverlay.classList.toggle('open', show);
              },

              formatDate(dateStr) {
                return new Date(dateStr + 'T00:00:00').toLocaleDateString(CONFIG.DATE_LOCALE, {
                  day: 'numeric', month: 'short', year: 'numeric'
                });
              },

              setLoading(el, message = 'Loadingâ€¦') {
                el.innerHTML = `
      <div style="grid-column:1/-1;text-align:center;padding:3rem 0">
        <div class="spinner"></div>
        <p style="color:var(--mid-brown);margin-top:.5rem">${message}</p>
      </div>`;
              }
            };

            // â”€â”€â”€ Application Logic â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
            const App = {
              allRooms: [],
              selectedRoom: null,
              search: { check_in: null, check_out: null, guests: 2 },

              async init() {
                LangService.init();
                this.setupEventListeners();
                this.initDateDefaults();
                await this.loadSettings();
                await this.loadInitialData();
              },

              async loadSettings() {
                try {
                  const res = await fetch('/api/settings');
                  const settings = await res.json();
                  if (settings.whatsapp) {
                    const wa = settings.whatsapp;
                    const display = document.getElementById('display-whatsapp');
                    if (display) display.textContent = wa;
                  }
                  if (settings.qr_code) {
                    const qr = document.getElementById('qr-image');
                    if (qr) qr.src = settings.qr_code;
                  }
                  App.globalSettings = settings;
                } catch (e) {}
              },

              setupEventListeners() {
                window.addEventListener('scroll', () => {
                  UI.elements.navbar.classList.toggle('scrolled', window.scrollY > 50);
                });

                window.addEventListener('click', (e) => {
                  if (e.target === UI.elements.modalOverlay) App.closeBooking();
                  if (!e.target.closest('.lang-selector')) {
                    document.getElementById('lang-dropdown')?.classList.remove('show');
                  }
                });

                // 3D Tilt Logic
                document.addEventListener('mousemove', (e) => {
                  const cards = document.querySelectorAll('.room-card, .feature-card');
                  cards.forEach(card => {
                    const rect = card.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;

                    if (x > 0 && x < rect.width && y > 0 && y < rect.height) {
                      const centerX = rect.width / 2;
                      const centerY = rect.height / 2;
                      const rotateX = ((y - centerY) / centerY) * -10;
                      const rotateY = ((x - centerX) / centerX) * 10;

                      card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
                    } else {
                      card.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;
                    }
                  });
                });

                // Reveal on scroll
                const observer = new IntersectionObserver((entries) => {
                  entries.forEach(entry => {
                    if (entry.isIntersecting) {
                      entry.target.classList.add('active');
                      if (entry.target.classList.contains('rooms-grid')) {
                        this.staggerRoomReveal();
                      }
                    }
                  });
                }, { threshold: 0.1 });

                document.querySelectorAll('.reveal, section').forEach(el => observer.observe(el));
              },

              staggerRoomReveal() {
                document.querySelectorAll('.room-card').forEach((card, i) => {
                  setTimeout(() => card.classList.add('active'), i * 150);
                });
              },

              initDateDefaults() {
                const today = new Date();
                const tom = new Date(today); tom.setDate(tom.getDate() + 1);
                const fmt = d => d.toISOString().split('T')[0];

                const ciInput = document.getElementById('s-checkin');
                const coInput = document.getElementById('s-checkout');
                if (ciInput && coInput) {
                  ciInput.min = fmt(today);
                  coInput.min = fmt(tom);
                  ciInput.value = fmt(today);
                  coInput.value = fmt(tom);
                  
                  App.search.check_in = ciInput.value;
                  App.search.check_out = coInput.value;
                }
              },

              async loadInitialData() {
                await Promise.all([this.loadRooms(), this.loadReviews()]);
              },

              async loadRooms() {
                UI.setLoading(UI.elements.roomsGrid, 'Exploring availabilityâ€¦');
                try {
                  const params = {};
                  if (App.search.check_in) params.check_in = App.search.check_in;
                  if (App.search.check_out) params.check_out = App.search.check_out;
                  if (App.search.guests) params.guests = App.search.guests;
 
                  App.allRooms = await ApiService.fetchRooms(params);
                  App.renderRooms(App.allRooms);
                } catch (e) {
                  UI.elements.roomsGrid.innerHTML = `<p class="text-error" style="grid-column:1/-1;text-align:center">Unable to load rooms. Please refresh the page.</p>`;
                }
              },

              renderRooms(rooms) {
                if (!rooms.length) {
                  UI.elements.roomsGrid.innerHTML = `<p style="grid-column:1/-1;text-align:center;color:var(--mid-brown)">No rooms available for these criteria.</p>`;
                  return;
                }

                const t = LangService.translations[LangService.current];
                UI.elements.roomsGrid.innerHTML = rooms.map(r => App.generateRoomCard(r, t)).join('');

                App.attachRevealObserver();
              },

              attachRevealObserver() {
                const observer = new IntersectionObserver((entries) => {
                  entries.forEach(entry => {
                    if (entry.isIntersecting) {
                      entry.target.classList.add('active');
                      if (entry.target.id === 'rooms-grid') {
                        this.staggerRoomReveal();
                      }
                    }
                  });
                }, { threshold: 0.1 });

                document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
              },

              generateRoomCard(r, t) {
                const isBooked = !r.available && App.search.check_in;
                const amenities = (r.amenities || []).filter(a => !['Private Balcony', 'Living Area', 'Private Pool'].includes(a)).slice(0, 4).map(a => `<span class="amenity-tag">${a}</span>`).join('');
                const badge = (App.search.check_in && App.search.check_out)
                  ? `<span class="room-avail ${r.available ? 'avail-yes' : 'avail-no'}">${r.available ? t.badge_available : t.badge_booked}</span>` : '';

                let imageSource = null;
                if (r.image_url) {
                  if (r.image_url.startsWith('uploads/') || r.image_url.startsWith('http')) {
                    imageSource = r.image_url;
                  } else {
                    imageSource = `/images/${r.image_url}`;
                  }
                }

                return `
      <div class="room-card reveal" id="room-${r.id}">
        <div class="room-img">
          ${imageSource ? `<img src="${imageSource}" alt="${r.name}" class="room-img-file">` : `<div class="room-img-inner img-standard"></div>`}
          ${badge}
        </div>
        <div class="room-body">
          <p class="room-type">${r.type}</p>
          <h3 class="room-name">${r.name}</h3>
          <p class="room-desc">${r.description}</p>
          <div class="room-amenities">${amenities}${r.amenities.length > 4 ? `<span class="amenity-tag">+${r.amenities.length - 4}</span>` : ''}</div>
          <div class="room-footer">
            <div class="room-price">${CONFIG.CURRENCY} ${r.price.toFixed(2)} <span>${t.room_night}</span></div>
            <button class="btn-primary" onclick='App.openBooking(${JSON.stringify(r)})' ${isBooked ? 'disabled style="opacity:.5"' : ''} aria-label="Book ${r.name}">
              ${isBooked ? t.btn_unavailable : t.btn_book_now}
            </button>
          </div>
        </div>
      </div>`;
              },

              async loadReviews() {
                try {
                  const data = await ApiService.fetchReviews();
                  document.getElementById('avg-rating').textContent = data.average_rating;
                  document.getElementById('avg-stars').textContent = 'â˜…'.repeat(Math.round(data.average_rating));
                  document.getElementById('review-count').textContent = `Based on ${data.reviews.length} reviews`;

                  UI.elements.reviewsGrid.innerHTML = data.reviews.map(r => `
        <div class="review-card">
          <div class="review-stars">${'â˜…'.repeat(r.rating)}${'â˜†'.repeat(5 - r.rating)}</div>
          <p class="review-text">"${r.comment}"</p>
          <p class="review-author">${r.guest_name}</p>
          <p class="review-date">${new Date(r.created_at).toLocaleDateString(CONFIG.DATE_LOCALE, { year: 'numeric', month: 'long' })}</p>
        </div>`).join('');
                } catch (e) {
                  UI.elements.reviewsGrid.innerHTML = `<p style="color:var(--mid-brown)">Reviews currently unavailable.</p>`;
                }
              },

              // â”€â”€ Action Handlers â”€â”€
              searchRooms() {
                const ci = document.getElementById('s-checkin').value;
                const co = document.getElementById('s-checkout').value;
                const g = document.getElementById('s-guests').value;

                if (!ci || !co) { UI.showToast('Select your dates first.', 'error'); return; }
                if (ci >= co) { UI.showToast('Check-out must be after check-in.', 'error'); return; }

                App.search = { check_in: ci, check_out: co, guests: g };
                
                // Open modal with professional loading state instead of scrolling
                document.getElementById('modal-room-name').textContent = "Quick Booking";
                document.getElementById('modal-room-type').textContent = `${UI.formatDate(ci)} â†’ ${UI.formatDate(co)}`;
                UI.setLoading(UI.elements.modalBody, 'Analyzing room availability...');
                UI.toggleModal(true);

                // Fetch rooms and trigger the selection view
                const params = { check_in: ci, check_out: co, guests: g };
                ApiService.fetchRooms(params).then(rooms => {
                  App.allRooms = rooms;
                  App.showQuickBookingView(rooms);
                }).catch(e => {
                  UI.elements.modalBody.innerHTML = `<p style="text-align:center; padding:2rem;">Connection issue. Please try again.</p>`;
                });

                const nights = Math.round((new Date(co) - new Date(ci)) / 86400000);
                document.getElementById('rooms-subtitle').textContent =
                  `${nights} night${nights > 1 ? 's' : ''} Â· ${g} guests Â· ${UI.formatDate(ci)} â†’ ${UI.formatDate(co)}`;
              },

              showQuickBookingView(rooms) {
                const { check_in, check_out } = App.search;
                const nights = Math.round((new Date(check_out) - new Date(check_in)) / 86400000);
                const t = LangService.translations[LangService.current];

                if (!rooms.length) {
                  UI.elements.modalBody.innerHTML = `
                    <div style="text-align:center; padding:2rem;">
                      <p style="margin-bottom:1.5rem; color:var(--mid-brown);">No rooms match your criteria for these dates.</p>
                      <button class="btn-primary" onclick="App.closeBooking()">Try Other Dates</button>
                    </div>`;
                  return;
                }

                const roomListHtml = rooms.map(r => `
                  <div class="qb-room-item" onclick='App.openBooking(${JSON.stringify(r)})'>
                    <div class="qb-info">
                      <h4>${r.name}</h4>
                      <p>${r.type} Â· Max ${r.capacity} Guests</p>
                    </div>
                    <div class="qb-pricing">
                      <span class="qb-rate">${CONFIG.CURRENCY} ${r.price.toFixed(2)} / night</span>
                      <span class="qb-total">${CONFIG.CURRENCY} ${(r.price * nights).toFixed(2)}</span>
                    </div>
                  </div>
                `).join('');

                UI.elements.modalBody.innerHTML = `
                  <div style="margin-bottom:1.5rem;">
                    <p style="font-size:0.9rem; color:var(--mid-brown);">${nights} night stay selected. Choose your room:</p>
                  </div>
                  <div class="quick-book-list">
                    ${roomListHtml}
                  </div>
                  <p style="font-size:0.75rem; text-align:center; margin-top:1.5rem; color:var(--mid-brown); opacity:0.7;">Prices inclusive of all standard service charges.</p>
                `;
              },

              openBooking(room) {
                App.selectedRoom = room;
                const { check_in, check_out } = App.search;
                const nights = (check_in && check_out) ? Math.round((new Date(check_out) - new Date(check_in)) / 86400000) : 1;
                const total = nights * room.price;

                document.getElementById('modal-room-name').textContent = room.name;
                document.getElementById('modal-room-type').textContent = room.type;

                const ci = check_in || new Date().toISOString().split('T')[0];
                const co = check_out || new Date(Date.now() + 86400000).toISOString().split('T')[0];

                UI.elements.modalBody.innerHTML = `
      <div class="stepper">
        <div class="step active" id="step-1">
          <div class="step-num">1</div>
          <div class="step-label">Your Stay</div>
        </div>
        <div class="step" id="step-2">
          <div class="step-num">2</div>
          <div class="step-label">Payment</div>
        </div>
      </div>

      <div id="booking-form-view">
        <div class="booking-summary">
          <div class="summary-item"><label>Check In</label><p>${UI.formatDate(ci)}</p></div>
          <div class="summary-item"><label>Check Out</label><p id="summary-co">${UI.formatDate(co)}</p></div>
          <div class="summary-item"><label>Duration</label><p><span id="summary-nights">${nights}</span> Nights</p></div>
          <div class="summary-total"><span>Total Payable</span><span id="summary-total">${CONFIG.CURRENCY} ${total.toFixed(2)}</span></div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label>Nights</label>
            <select id="b-duration" onchange="App.updateBookingDates()">
              ${[1, 2, 3, 4, 5, 6, 7, 10, 14].map(n => `<option value="${n}" ${n === nights ? 'selected' : ''}>${n} ${n > 1 ? 'Nights' : 'Night'}</option>`).join('')}
            </select>
          </div>
          <div class="form-group">
            <label>Guests</label>
            <select id="b-guests">
              ${Array.from({ length: room.capacity }, (_, i) => `<option value="${i + 1}" ${App.search.guests == i + 1 ? 'selected' : ''}>${i + 1}</option>`).join('')}
            </select>
          </div>
        </div>

        <div class="form-group">
          <label>Full Name *</label>
          <input type="text" id="b-name" placeholder="E.g. Ahmad Faiz">
        </div>

        <div class="form-group">
          <label>Special Requests</label>
          <textarea id="b-special" rows="2" placeholder="Dietary needs, arrival time, etc."></textarea>
        </div>
        
        <button class="btn-primary btn-block" onclick="App.showQRView()">Proceed to Payment</button>
        <button class="btn-outline btn-block" onclick="App.submitBooking('whatsapp')" style="border:none; color:var(--sage); background:transparent;">Or inquire via WhatsApp</button>
      </div>

      <div id="qr-payment-view" class="qr-container">
        <div class="qr-card">
          <h3 style="font-family:'Cormorant Garamond', serif; font-size:1.4rem; margin-bottom:1rem;">Scan & Pay Securely</h3>
          <img src="${App.globalSettings?.qr_code || '/images/QR.png'}" alt="Payment QR" class="qr-image" onerror="this.src='https://placehold.co/220x220?text=Scan+to+Pay'">
          <div class="summary-total" style="border:none; padding:0; justify-content:center; gap:0.5rem;">
            <span style="font-size:0.9rem; font-weight:400;">Amount:</span>
            <span id="qr-total-display">${CONFIG.CURRENCY} ${total.toFixed(2)}</span>
          </div>
        </div>
        <p class="payment-instruction">1. Scan the QR above to pay RM <span id="qr-amount-confirm">${total.toFixed(2)}</span><br>2. Save your transaction receipt<br>3. Click below to confirm stay</p>
        <button class="btn-primary btn-block" onclick="App.submitBooking('qr_paid')">I've Completed Payment</button>
        <button class="btn-outline btn-block" onclick="App.showFormView()" style="border:none; font-size:0.8rem;">Go back to details</button>
      </div>

      <div id="booking-success-view" class="confirmation" style="display:none;">
        <div class="confirm-icon">âœ“</div>
        <h3 style="font-family:'Cormorant Garamond', serif; font-size:1.8rem; margin-bottom:1rem;">Inquiry Sent!</h3>
        <p style="font-size:0.95rem; line-height:1.6; color:var(--mid-brown); margin-bottom:1.5rem;">Your booking request has been sent via WhatsApp. The owner will verify your details and confirm your stay shortly.</p>
        <div class="confirm-details">
          <p><strong>Next Steps:</strong></p>
          <ul style="padding-left:1.2rem; margin-top:0.5rem; display:flex; flex-direction:column; gap:0.4rem;">
            <li>Stay tuned to WhatsApp for host confirmation</li>
            <li>Keep your payment receipt (if applicable)</li>
            <li>Enjoy your stay at Homestay Tokou!</li>
          </ul>
        </div>
        <button class="btn-primary btn-block" onclick="App.closeBooking()">Close & Return Home</button>
      </div>
    `;

                UI.toggleModal(true);
              },

              updateBookingDates() {
                const ciVal = this.search.check_in || new Date().toISOString().split('T')[0];
                const nights = parseInt(document.getElementById('b-duration').value);
                const ciDate = new Date(ciVal + 'T00:00:00');
                const coDate = new Date(ciDate);
                coDate.setDate(ciDate.getDate() + nights);
                const coVal = coDate.toISOString().split('T')[0];
                const total = nights * this.selectedRoom.price;

                document.getElementById('summary-co').textContent = UI.formatDate(coVal);
                document.getElementById('summary-nights').textContent = nights;
                document.getElementById('summary-total').textContent = `${CONFIG.CURRENCY} ${total.toFixed(2)}`;

                const qrTotal = document.getElementById('qr-total-display');
                if (qrTotal) qrTotal.textContent = `${CONFIG.CURRENCY} ${total.toFixed(2)}`;
                
                const qrConfirm = document.getElementById('qr-amount-confirm');
                if (qrConfirm) qrConfirm.textContent = total.toFixed(2);
              },

              showQRView() {
                const name = document.getElementById('b-name').value.trim();
                if (!name) {
                  UI.showToast('Please enter your name.', 'error');
                  return;
                }
                document.getElementById('booking-form-view').style.display = 'none';
                document.getElementById('qr-payment-view').classList.add('show');
                document.getElementById('step-1').classList.remove('active');
                document.getElementById('step-2').classList.add('active');
              },

              showFormView() {
                document.getElementById('booking-form-view').style.display = 'block';
                document.getElementById('qr-payment-view').classList.remove('show');
                document.getElementById('booking-success-view').style.display = 'none';
                document.getElementById('step-2').classList.remove('active');
                document.getElementById('step-1').classList.add('active');
              },

              showSuccessView() {
                document.getElementById('booking-form-view').style.display = 'none';
                document.getElementById('qr-payment-view').classList.remove('show');
                document.getElementById('booking-success-view').style.display = 'block';
                document.querySelector('.stepper').style.display = 'none';
              },

              closeBooking() { UI.toggleModal(false); },

              submitBooking(method) {
                const ciVal = this.search.check_in || new Date().toISOString().split('T')[0];
                const nights = parseInt(document.getElementById('b-duration').value);
                const guests = document.getElementById('b-guests').value;
                const guest_name = document.getElementById('b-name').value.trim();
                const special = document.getElementById('b-special').value.trim();

                if (!guest_name) {
                  UI.showToast('Please enter your name.', 'error');
                  return;
                }

                const ciDate = new Date(ciVal + 'T00:00:00');
                const coDate = new Date(ciDate);
                coDate.setDate(ciDate.getDate() + nights);
                const coVal = coDate.toISOString().split('T')[0];

                let msg = ``;
                if (method === 'qr_paid') {
                  msg = `*NEW BOOKING PAYMENT*\n\n`;
                  msg += `I have completed the payment for my stay. Here are the details:\n\n`;
                } else {
                  msg = `*BOOKING INQUIRY*\n\n`;
                  msg += `Hello, I would like to check availability for the following:\n\n`;
                }

                msg += `â€¢ Room: ${this.selectedRoom.name}\n`;
                msg += `â€¢ Check-in: ${UI.formatDate(ciVal)}\n`;
                msg += `â€¢ Check-out: ${UI.formatDate(coVal)}\n`;
                msg += `â€¢ Nights: ${nights}\n`;
                msg += `â€¢ Guests: ${guests}\n`;
                msg += `â€¢ Name: ${guest_name}\n`;

                if (method === 'qr_paid') {
                  const total = nights * this.selectedRoom.price;
                  msg += `â€¢ Total Paid: RM ${total.toFixed(2)}\n`;
                  msg += `\n(I will send my payment receipt below)`;
                }

                if (special) msg += `\n\nâ€¢ Special Request: ${special}`;

                const encodedMsg = encodeURIComponent(msg);
                const waNumber = (this.globalSettings?.whatsapp || '601110085626').replace(/\+/g, '');
                const whatsappUrl = `https://wa.me/${waNumber}?text=${encodedMsg}`;

                window.open(whatsappUrl, '_blank');
                this.closeBooking();
              },

              shareBooking() {
                const ciVal = this.search.check_in || new Date().toISOString().split('T')[0];
                const nights = parseInt(document.getElementById('b-duration').value);
                const guests = document.getElementById('b-guests').value;
                const ciDate = new Date(ciVal + 'T00:00:00');
                const coDate = new Date(ciDate);
                coDate.setDate(ciDate.getDate() + nights);
                const coVal = coDate.toISOString().split('T')[0];

                const shareUrl = `${window.location.origin}${window.location.pathname}?room=${encodeURIComponent(this.selectedRoom.name)}&checkin=${ciVal}&checkout=${coVal}&guests=${guests}`;
                if (navigator.share) {
                  navigator.share({
                    title: 'HomeStay Baru â€“ Booking',
                    text: `Check out this room: ${this.selectedRoom.name}`,
                    url: shareUrl,
                  }).catch(console.error);
                } else {
                  navigator.clipboard.writeText(shareUrl).then(() => {
                    UI.showToast('Share link copied to clipboard!', 'success');
                  });
                }
              }
            };

            // Start the application
            document.addEventListener('DOMContentLoaded', () => App.init());

            // Global access for onclick handlers
            window.App = App;
            window.setLanguage = (l) => LangService.set(l);
            window.toggleLangDropdown = () => document.getElementById('lang-dropdown').classList.toggle('show');
          
