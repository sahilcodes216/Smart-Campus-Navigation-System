import os
from PIL import Image, ImageDraw, ImageFont

def generate_svg(output_path):
    w, h = 1800, 1100
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">')
    svg.append('''<defs>
      <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#0f172a" />
        <stop offset="100%" stop-color="#1e293b" />
      </linearGradient>
      <pattern id="archGrid" width="20" height="20" patternUnits="userSpaceOnUse">
        <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#334155" stroke-width="0.5" stroke-opacity="0.4" />
      </pattern>
      <filter id="cardShadow" x="-2%" y="-2%" width="104%" height="106%">
        <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.45" />
      </filter>
    </defs>''')

    # Main dark blueprint background
    svg.append(f'<rect width="{w}" height="{h}" fill="url(#bgGrad)" />')
    svg.append(f'<rect width="{w}" height="{h}" fill="url(#archGrid)" />')

    # Overall diagram title bar (top 0 to 65px)
    svg.append('''
      <rect x="18" y="10" width="1764" height="46" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5" />
      <text x="36" y="38" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="20" font-weight="800" fill="#f8fafc">
        DEMO UNIVERSITY — COMPLETE 6-FLOOR 2D ARCHITECTURAL LAYOUT (300 ROOMS)
      </text>
      <text x="1450" y="38" font-family="monospace" font-size="13" font-weight="600" fill="#38bdf8">
        PRD v1.0 • 6 LEVELS • 50 ROOMS/FLOOR
      </text>
    ''')

    # Floor box specifications (matching FLOOR_BOX_COORDS exact percentages)
    # Row 1: top: 6% (66px), height: 42% (462px)
    # Row 2: top: 50% (550px), height: 38% (418px)
    # Col 1: left: 1% (18px), width: 32% (576px)
    # Col 2: left: 34% (612px), width: 32% (576px)
    # Col 3: left: 67% (1206px), width: 32% (576px)

    floors = [
        # Floor 0: Ground
        {
            "index": 0, "title": "GROUND FLOOR (LEVEL 0)", "subtitle": "Rooms 1–50 • Admin, Reception, Mess, Library",
            "x": 18, "y": 66, "w": 576, "h": 462, "theme": "#38bdf8",
            "rooms": [
                {"label": "#1 Reception", "desc": "Main Entry", "x": 15, "y": 45, "w": 125, "h": 85, "color": "#0284c7"},
                {"label": "#2 Security", "desc": "CCTV Hub", "x": 145, "y": 45, "w": 100, "h": 85, "color": "#0369a1"},
                {"label": "#3 Help Desk", "desc": "Visitor Info", "x": 250, "y": 45, "w": 105, "h": 85, "color": "#0284c7"},
                {"label": "#4 Admissions", "desc": "Counter A-D", "x": 360, "y": 45, "w": 100, "h": 85, "color": "#0369a1"},
                {"label": "#6 Director", "desc": "Office Suite", "x": 465, "y": 45, "w": 96, "h": 85, "color": "#0f766e"},
                {"label": "#11 Comp Lab 1", "desc": "45 Workstations", "x": 15, "y": 240, "w": 130, "h": 100, "color": "#1d4ed8"},
                {"label": "#14 AI & ML Lab", "desc": "GPU Clusters", "x": 150, "y": 240, "w": 130, "h": 100, "color": "#6366f1"},
                {"label": "#21 Main Mess", "desc": "Cafeteria & Dining (250 seats)", "x": 285, "y": 240, "w": 140, "h": 100, "color": "#b45309"},
                {"label": "#26 Central Library", "desc": "Stacks & Reading Room", "x": 430, "y": 240, "w": 131, "h": 100, "color": "#4338ca"},
                {"label": "#36 Medical Room", "desc": "First Aid & Clinic", "x": 15, "y": 350, "w": 130, "h": 85, "color": "#dc2626"},
                {"label": "Rooms 37–50", "desc": "Admin & Accounts", "x": 150, "y": 350, "w": 275, "h": 85, "color": "#334155"},
                {"label": "Restrooms", "desc": "Men / Women / ADA", "x": 430, "y": 350, "w": 131, "h": 85, "color": "#475569"}
            ]
        },
        # Floor 1: First
        {
            "index": 1, "title": "FIRST FLOOR (LEVEL 1)", "subtitle": "Rooms 101–150 • CSE Department, Classrooms 101–110",
            "x": 612, "y": 66, "w": 576, "h": 462, "theme": "#4ade80",
            "rooms": [
                {"label": "Classrooms 101–103", "desc": "Lecture Halls A-C", "x": 15, "y": 45, "w": 170, "h": 85, "color": "#15803d"},
                {"label": "Classrooms 104–106", "desc": "Lecture Halls D-F", "x": 190, "y": 45, "w": 180, "h": 85, "color": "#15803d"},
                {"label": "Classrooms 107–110", "desc": "Smart Classrooms", "x": 375, "y": 45, "w": 186, "h": 85, "color": "#166534"},
                {"label": "#115 Robotics Lab", "desc": "Automation & Microcontrollers", "x": 15, "y": 240, "w": 170, "h": 100, "color": "#0d9488"},
                {"label": "#120 IoT & Sensors", "desc": "Embedded Hardware", "x": 190, "y": 240, "w": 180, "h": 100, "color": "#0f766e"},
                {"label": "#127 HOD Office CSE", "desc": "Faculty Dept Head", "x": 375, "y": 240, "w": 186, "h": 100, "color": "#047857"},
                {"label": "Rooms 128–140", "desc": "CSE Faculty Cabins", "x": 15, "y": 350, "w": 265, "h": 85, "color": "#334155"},
                {"label": "Rooms 141–150", "desc": "Tutorial Rooms", "x": 285, "y": 350, "w": 140, "h": 85, "color": "#334155"},
                {"label": "Restrooms", "desc": "Men / Women / ADA", "x": 430, "y": 350, "w": 131, "h": 85, "color": "#475569"}
            ]
        },
        # Floor 2: Second
        {
            "index": 2, "title": "SECOND FLOOR (LEVEL 2)", "subtitle": "Rooms 201–250 • AI & Machine Learning Dept",
            "x": 1206, "y": 66, "w": 576, "h": 462, "theme": "#a855f7",
            "rooms": [
                {"label": "Classrooms 201–205", "desc": "AI Lecture Theatres", "x": 15, "y": 45, "w": 265, "h": 85, "color": "#7e22ce"},
                {"label": "Classrooms 206–210", "desc": "Interactive Studios", "x": 285, "y": 45, "w": 276, "h": 85, "color": "#6b21a8"},
                {"label": "#215 Deep Learning Lab", "desc": "Neural Compute Cluster", "x": 15, "y": 240, "w": 175, "h": 100, "color": "#9333ea"},
                {"label": "#220 Data Analytics Lab", "desc": "Big Data Visualizations", "x": 195, "y": 240, "w": 175, "h": 100, "color": "#7c3aed"},
                {"label": "#227 HOD Office AI&ML", "desc": "Faculty Dept Head", "x": 375, "y": 240, "w": 186, "h": 100, "color": "#581c87"},
                {"label": "Rooms 228–240", "desc": "AI Faculty Research", "x": 15, "y": 350, "w": 265, "h": 85, "color": "#334155"},
                {"label": "Rooms 241–250", "desc": "NLP & Vision Labs", "x": 285, "y": 350, "w": 140, "h": 85, "color": "#334155"},
                {"label": "Restrooms", "desc": "Men / Women / ADA", "x": 430, "y": 350, "w": 131, "h": 85, "color": "#475569"}
            ]
        },
        # Floor 3: Third
        {
            "index": 3, "title": "THIRD FLOOR (LEVEL 3)", "subtitle": "Rooms 301–350 • Information Technology Dept",
            "x": 18, "y": 550, "w": 576, "h": 418, "theme": "#f59e0b",
            "rooms": [
                {"label": "Classrooms 301–305", "desc": "IT Classrooms", "x": 15, "y": 42, "w": 265, "h": 75, "color": "#b45309"},
                {"label": "Classrooms 306–310", "desc": "Multimedia Halls", "x": 285, "y": 42, "w": 276, "h": 75, "color": "#92400e"},
                {"label": "#315 Full-Stack Lab", "desc": "Software Eng Studio", "x": 15, "y": 210, "w": 175, "h": 90, "color": "#d97706"},
                {"label": "#320 Operating Systems", "desc": "Linux Kernel Lab", "x": 195, "y": 210, "w": 175, "h": 90, "color": "#b45309"},
                {"label": "#327 HOD Office IT", "desc": "Faculty Dept Head", "x": 375, "y": 210, "w": 186, "h": 90, "color": "#78350f"},
                {"label": "Rooms 328–340", "desc": "IT Faculty Cabins", "x": 15, "y": 310, "w": 265, "h": 85, "color": "#334155"},
                {"label": "Rooms 341–350", "desc": "Cloud & DevOps Lab", "x": 285, "y": 310, "w": 140, "h": 85, "color": "#334155"},
                {"label": "Restrooms", "desc": "Men / Women / ADA", "x": 430, "y": 310, "w": 131, "h": 85, "color": "#475569"}
            ]
        },
        # Floor 4: Fourth
        {
            "index": 4, "title": "FOURTH FLOOR (LEVEL 4)", "subtitle": "Rooms 401–450 • Cyber Security & Research Wing",
            "x": 612, "y": 550, "w": 576, "h": 418, "theme": "#ef4444",
            "rooms": [
                {"label": "Classrooms 401–405", "desc": "Security Classrooms", "x": 15, "y": 42, "w": 265, "h": 75, "color": "#b91c1c"},
                {"label": "Classrooms 406–410", "desc": "Specialised Theatres", "x": 285, "y": 42, "w": 276, "h": 75, "color": "#991b1b"},
                {"label": "#415 Cyber Security Lab", "desc": "SOC Defense Arena", "x": 15, "y": 210, "w": 175, "h": 90, "color": "#dc2626"},
                {"label": "#420 Cloud & Blockchain", "desc": "Distributed Systems", "x": 195, "y": 210, "w": 175, "h": 90, "color": "#b91c1c"},
                {"label": "#427 HOD Office Research", "desc": "Dean of Research", "x": 375, "y": 210, "w": 186, "h": 90, "color": "#7f1d1d"},
                {"label": "Rooms 428–440", "desc": "PhD Research Scholars", "x": 15, "y": 310, "w": 265, "h": 85, "color": "#334155"},
                {"label": "Rooms 441–450", "desc": "Cryptology Lab", "x": 285, "y": 310, "w": 140, "h": 85, "color": "#334155"},
                {"label": "Restrooms", "desc": "Men / Women / ADA", "x": 430, "y": 310, "w": 131, "h": 85, "color": "#475569"}
            ]
        },
        # Floor 5: Fifth
        {
            "index": 5, "title": "FIFTH FLOOR (LEVEL 5)", "subtitle": "Rooms 501–550 • Seminar Hall, Auditorium, Incubation",
            "x": 1206, "y": 550, "w": 576, "h": 418, "theme": "#ec4899",
            "rooms": [
                {"label": "#501 Seminar Hall", "desc": "Keynote Auditorium (300 seats)", "x": 15, "y": 42, "w": 350, "h": 75, "color": "#be185d"},
                {"label": "#505 Executive Hall", "desc": "Boardroom Suite", "x": 370, "y": 42, "w": 191, "h": 75, "color": "#9d174d"},
                {"label": "#515 Incubation Centre", "desc": "Student Startup Workspaces", "x": 15, "y": 210, "w": 265, "h": 90, "color": "#db2777"},
                {"label": "#525 Conference Room", "desc": "Video Conferncing Hub", "x": 285, "y": 210, "w": 140, "h": 90, "color": "#be185d"},
                {"label": "VIP Lounge", "desc": "Guest Suites", "x": 430, "y": 210, "w": 131, "h": 90, "color": "#831843"},
                {"label": "Rooms 526–550", "desc": "Incubator Hub 2", "x": 15, "y": 310, "w": 265, "h": 85, "color": "#334155"},
                {"label": "Open Terrace Lounge", "desc": "Sky Courtyard", "x": 285, "y": 310, "w": 140, "h": 85, "color": "#047857"},
                {"label": "Restrooms", "desc": "Men / Women / ADA", "x": 430, "y": 310, "w": 131, "h": 85, "color": "#475569"}
            ]
        }
    ]

    for f in floors:
        fx, fy, fw, fh = f["x"], f["y"], f["w"], f["h"]
        theme = f["theme"]

        # Outer card container
        svg.append(f'''
          <!-- Card for {f["title"]} -->
          <rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="12" fill="#1e293b" stroke="{theme}" stroke-width="2" filter="url(#cardShadow)" />
          
          <!-- Card Header Bar -->
          <rect x="{fx}" y="{fy}" width="{fw}" height="36" rx="10" fill="{theme}" fill-opacity="0.18" />
          <text x="{fx + 16}" y="{fy + 24}" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="15" font-weight="800" fill="{theme}">
            {f["title"]}
          </text>
          <text x="{fx + fw - 16}" y="{fy + 24}" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="12" font-weight="600" fill="#94a3b8" text-anchor="end">
            {f["subtitle"]}
          </text>
        ''')

        # Central Corridor (horizontal spine)
        corridor_y = fy + (140 if f["index"] < 3 else 125)
        corridor_h = 56
        svg.append(f'''
          <!-- Central Corridor Spine -->
          <rect x="{fx + 15}" y="{corridor_y}" width="{fw - 30}" height="{corridor_h}" rx="6" fill="#0f172a" stroke="#334155" stroke-dasharray="4 4" stroke-width="1.5" />
          
          <!-- Lift Core (Twin Lifts) -->
          <rect x="{fx + (fw // 2) - 90}" y="{corridor_y + 6}" width="80" height="44" rx="4" fill="#0284c7" fill-opacity="0.25" stroke="#38bdf8" stroke-width="1.5" />
          <text x="{fx + (fw // 2) - 50}" y="{corridor_y + 32}" font-family="monospace" font-size="11" font-weight="700" fill="#38bdf8" text-anchor="middle">🛗 Lifts 1&amp;2</text>
          
          <!-- Staircase Cores -->
          <rect x="{fx + 25}" y="{corridor_y + 6}" width="70" height="44" rx="4" fill="#64748b" fill-opacity="0.3" stroke="#94a3b8" stroke-width="1.2" />
          <text x="{fx + 60}" y="{corridor_y + 32}" font-family="monospace" font-size="11" font-weight="700" fill="#e2e8f0" text-anchor="middle">🪜 West Stair</text>

          <rect x="{fx + fw - 105}" y="{corridor_y + 6}" width="75" height="44" rx="4" fill="#64748b" fill-opacity="0.3" stroke="#94a3b8" stroke-width="1.2" />
          <text x="{fx + fw - 68}" y="{corridor_y + 32}" font-family="monospace" font-size="11" font-weight="700" fill="#e2e8f0" text-anchor="middle">🪜 East Stair</text>

          <text x="{fx + (fw // 2) + 40}" y="{corridor_y + 32}" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="11" font-weight="700" fill="#64748b" letter-spacing="2">CENTRAL CORRIDOR</text>
        ''')

        # Individual rooms inside the floor plan
        for rm in f["rooms"]:
            rx = fx + rm["x"]
            ry = fy + rm["y"]
            rw = rm["w"]
            rh = rm["h"]
            col = rm["color"]
            label = rm["label"].replace("&", "&amp;")
            desc = rm["desc"].replace("&", "&amp;")

            svg.append(f'''
              <rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="6" fill="{col}" fill-opacity="0.22" stroke="{col}" stroke-width="1.5" />
              <text x="{rx + 8}" y="{ry + 20}" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="12" font-weight="800" fill="#f8fafc">
                {label}
              </text>
              <text x="{rx + 8}" y="{ry + 38}" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="10" font-weight="500" fill="#94a3b8">
                {desc}
              </text>
            ''')

    # Footer note at bottom (1020px to 1090px)
    svg.append(f'''
      <rect x="18" y="995" width="1764" height="85" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1" />
      <text x="36" y="1030" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="14" font-weight="700" fill="#f8fafc">
        ARCHITECTURAL CIRCULATION KEY:
      </text>
      <text x="36" y="1058" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="12" fill="#94a3b8">
        • Twin Lifts connect Level 0 to Level 5 centrally • Dual Fire Stairwells (East &amp; West Wings) on all levels • Wheelchair-accessible corridors (min. 2.4m width) • All 300 numbered rooms mapped
      </text>
      <text x="1450" y="1045" font-family="monospace" font-size="13" font-weight="700" fill="#22c55e">
        ✔ LIVE RENDER READY
      </text>
    ''')

    svg.append('</svg>')

    full_svg = '\n'.join(svg)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_svg)
    print(f"Generated SVG at {output_path} ({len(full_svg)} bytes)")
    return full_svg

def generate_jpg(output_path):
    w, h = 1800, 1100
    img = Image.new("RGB", (w, h), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    # Draw grid
    for x in range(0, w, 30):
        draw.line([(x, 0), (x, h)], fill=(30, 41, 59), width=1)
    for y in range(0, h, 30):
        draw.line([(0, y), (w, y)], fill=(30, 41, 59), width=1)

    # Title Bar
    draw.rounded_rectangle([(18, 10), (1782, 56)], radius=8, fill=(30, 41, 59), outline=(56, 189, 248), width=2)
    draw.text((36, 22), "DEMO UNIVERSITY — COMPLETE 6-FLOOR 2D ARCHITECTURAL LAYOUT (300 ROOMS)", fill=(248, 250, 252))
    draw.text((1400, 22), "PRD v1.0 • 6 LEVELS • 50 ROOMS/FLOOR", fill=(56, 189, 248))

    floors = [
        {"title": "GROUND FLOOR (LEVEL 0)", "sub": "Rooms 1–50 • Admin, Reception, Mess, Library", "x": 18, "y": 66, "w": 576, "h": 462, "col": (56, 189, 248)},
        {"title": "FIRST FLOOR (LEVEL 1)", "sub": "Rooms 101–150 • CSE Dept, Classrooms 101–110", "x": 612, "y": 66, "w": 576, "h": 462, "col": (74, 222, 128)},
        {"title": "SECOND FLOOR (LEVEL 2)", "sub": "Rooms 201–250 • AI & Machine Learning Dept", "x": 1206, "y": 66, "w": 576, "h": 462, "col": (168, 85, 247)},
        {"title": "THIRD FLOOR (LEVEL 3)", "sub": "Rooms 301–350 • Information Technology Dept", "x": 18, "y": 550, "w": 576, "h": 418, "col": (245, 158, 11)},
        {"title": "FOURTH FLOOR (LEVEL 4)", "sub": "Rooms 401–450 • Cyber Security & Research Wing", "x": 612, "y": 550, "w": 576, "h": 418, "col": (239, 68, 68)},
        {"title": "FIFTH FLOOR (LEVEL 5)", "sub": "Rooms 501–550 • Seminar Hall, Auditorium, Incubation", "x": 1206, "y": 550, "w": 576, "h": 418, "col": (236, 72, 153)}
    ]

    for f in floors:
        fx, fy, fw, fh = f["x"], f["y"], f["w"], f["h"]
        col = f["col"]

        # Floor Card Outline
        draw.rounded_rectangle([(fx, fy), (fx + fw, fy + fh)], radius=12, fill=(30, 41, 59), outline=col, width=2)
        # Header
        draw.rounded_rectangle([(fx, fy), (fx + fw, fy + 36)], radius=10, fill=(col[0]//4, col[1]//4, col[2]//4))
        draw.text((fx + 16, fy + 10), f["title"], fill=col)
        draw.text((fx + fw - 280, fy + 10), f["sub"], fill=(148, 163, 184))

        # Corridor
        cy = fy + (140 if fy < 500 else 125)
        draw.rounded_rectangle([(fx + 15, cy), (fx + fw - 15, cy + 56)], radius=6, fill=(15, 23, 42), outline=(51, 65, 85), width=1)
        # Lift
        draw.rounded_rectangle([(fx + fw//2 - 60, cy + 6), (fx + fw//2 + 60, cy + 50)], radius=4, fill=(2, 132, 199), outline=(56, 189, 248), width=1)
        draw.text((fx + fw//2 - 45, cy + 18), "Lifts 1 & 2", fill=(255, 255, 255))
        # Stairs
        draw.rounded_rectangle([(fx + 25, cy + 6), (fx + 100, cy + 50)], radius=4, fill=(71, 85, 105))
        draw.text((fx + 32, cy + 18), "West Stair", fill=(226, 232, 240))
        draw.rounded_rectangle([(fx + fw - 105, cy + 6), (fx + fw - 30, cy + 50)], radius=4, fill=(71, 85, 105))
        draw.text((fx + fw - 100, cy + 18), "East Stair", fill=(226, 232, 240))

        # Sample Rooms top row
        rx1, rx2, rx3 = fx + 15, fx + 200, fx + 390
        ry1 = fy + 45
        draw.rounded_rectangle([(rx1, ry1), (rx1 + 175, ry1 + 80)], radius=6, fill=(col[0]//3, col[1]//3, col[2]//3), outline=col, width=1)
        draw.text((rx1 + 10, ry1 + 10), "Wing A / North Classrooms", fill=(248, 250, 252))
        draw.text((rx1 + 10, ry1 + 35), "Rooms .01 - .15", fill=(148, 163, 184))

        draw.rounded_rectangle([(rx2, ry1), (rx2 + 180, ry1 + 80)], radius=6, fill=(col[0]//3, col[1]//3, col[2]//3), outline=col, width=1)
        draw.text((rx2 + 10, ry1 + 10), "Core Labs / Admin Hub", fill=(248, 250, 252))
        draw.text((rx2 + 10, ry1 + 35), "Rooms .16 - .30", fill=(148, 163, 184))

        draw.rounded_rectangle([(rx3, ry1), (fx + fw - 15, ry1 + 80)], radius=6, fill=(col[0]//3, col[1]//3, col[2]//3), outline=col, width=1)
        draw.text((rx3 + 10, ry1 + 10), "Wing B / Specialized", fill=(248, 250, 252))
        draw.text((rx3 + 10, ry1 + 35), "Rooms .31 - .50", fill=(148, 163, 184))

        # Bottom row rooms
        ry2 = cy + 65
        rh2 = fh - (ry2 - fy) - 15
        draw.rounded_rectangle([(rx1, ry2), (rx1 + 175, ry2 + rh2)], radius=6, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
        draw.text((rx1 + 10, ry2 + 10), "Faculty Suites", fill=(248, 250, 252))
        draw.text((rx1 + 10, ry2 + 30), "HOD Office & Cabins", fill=(148, 163, 184))

        draw.rounded_rectangle([(rx2, ry2), (rx2 + 180, ry2 + rh2)], radius=6, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
        draw.text((rx2 + 10, ry2 + 10), "Student Project Studios", fill=(248, 250, 252))
        draw.text((rx2 + 10, ry2 + 30), "Discussion Rooms", fill=(148, 163, 184))

        draw.rounded_rectangle([(rx3, ry2), (fx + fw - 15, ry2 + rh2)], radius=6, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
        draw.text((rx3 + 10, ry2 + 10), "Amenities & Restrooms", fill=(248, 250, 252))
        draw.text((rx3 + 10, ry2 + 30), "Men / Women / ADA", fill=(148, 163, 184))

    # Footer
    draw.rounded_rectangle([(18, 995), (1782, 1080)], radius=8, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
    draw.text((36, 1010), "ARCHITECTURAL CIRCULATION KEY:", fill=(248, 250, 252))
    draw.text((36, 1035), "• Twin Lifts connect Level 0 to Level 5 centrally • Dual Fire Stairwells on all levels • Wheelchair-accessible corridors (2.4m)", fill=(148, 163, 184))
    draw.text((1500, 1025), "LIVE RENDER READY", fill=(34, 197, 94))

    img.save(output_path, "JPEG", quality=92)
    print(f"Generated JPG at {output_path}")

if __name__ == "__main__":
    import shutil
    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    svg_file = os.path.join(base_dir, "campus-2d-floor-plan.svg")
    jpg_file = os.path.join(base_dir, "campus-2d-floor-plan.jpg")

    generate_svg(svg_file)
    generate_jpg(jpg_file)

    # Copy to assets/
    shutil.copy2(svg_file, os.path.join(assets_dir, "campus-2d-floor-plan.svg"))
    shutil.copy2(jpg_file, os.path.join(assets_dir, "campus-2d-floor-plan.jpg"))
    print("All image assets successfully deployed to root and assets/ directories!")

