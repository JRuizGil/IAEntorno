from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image
import os, io

# ── CONFIG ────────────────────────────────────────────────────────────────────
W, H = landscape(A4)  # 841.89 x 595.28 pts

NAVY      = HexColor("#0D1B3E")
NAVY_DARK = HexColor("#080E1E")
NAVY_MID  = HexColor("#152852")
ORANGE    = HexColor("#FF6B23")
WHITE_C   = HexColor("#FFFFFF")
LGRAY     = HexColor("#CCCCCC")
DGRAY     = HexColor("#2A3A6A")
BLACK_C   = HexColor("#000000")

IMGS = {
    "017": "/root/.claude/uploads/e9b5fa60-5927-438b-86d5-288a719c4134/e027f003-1000149017.jpg",
    "018": "/root/.claude/uploads/e9b5fa60-5927-438b-86d5-288a719c4134/e6b79f4a-1000149018.jpg",
    "019": "/root/.claude/uploads/e9b5fa60-5927-438b-86d5-288a719c4134/8008f10a-1000149019.jpg",
    "020": "/root/.claude/uploads/e9b5fa60-5927-438b-86d5-288a719c4134/8ad82bc8-1000149020.jpg",
    "021": "/root/.claude/uploads/e9b5fa60-5927-438b-86d5-288a719c4134/01f972cd-1000149021.jpg",
    "022": "/root/.claude/uploads/e9b5fa60-5927-438b-86d5-288a719c4134/54b6f34c-1000149022.jpg",
}

OUT = "/home/user/IAEntorno/NO_SALIR_DE_DIA_presentacion.pdf"

# ── HELPERS ───────────────────────────────────────────────────────────────────
def bg(c, color=NAVY):
    c.setFillColor(color)
    c.rect(0, 0, W, H, fill=1, stroke=0)

def top_bar(c, color=ORANGE, h=5):
    c.setFillColor(color)
    c.rect(0, H - h, W, h, fill=1, stroke=0)

def rect_fill(c, x, y, w, h, fill, stroke_color=None, stroke_w=0.5):
    if stroke_color:
        c.setStrokeColor(stroke_color)
        c.setLineWidth(stroke_w)
    else:
        c.setStrokeColor(fill)
    c.setFillColor(fill)
    c.rect(x, y, w, h, fill=1, stroke=1 if stroke_color else 0)

def label(c, text, x, y, size=9, color=ORANGE, bold=False):
    c.setFillColor(color)
    c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
    c.drawString(x, y, text)

def mlabel(c, text, x, y, size, color, bold=False, line_h=None, max_w=None):
    """Multi-line label. Splits on \n."""
    if line_h is None:
        line_h = size * 1.35
    fn = "Helvetica-Bold" if bold else "Helvetica"
    c.setFont(fn, size)
    c.setFillColor(color)
    for i, line in enumerate(text.split("\n")):
        c.drawString(x, y - i * line_h, line)

def draw_img(c, key, x, y, w, h):
    path = IMGS.get(key)
    if path and os.path.exists(path):
        try:
            # Maintain aspect ratio, crop to fit
            img = Image.open(path)
            iw, ih = img.size
            # scale to fill the box
            scale = max(w / iw, h / ih)
            nw, nh = int(iw * scale), int(ih * scale)
            img = img.resize((nw, nh), Image.LANCZOS)
            # crop center
            ox = (nw - int(w)) // 2
            oy = (nh - int(h)) // 2
            img = img.crop((ox, oy, ox + int(w), oy + int(h)))
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=88)
            buf.seek(0)
            c.drawImage(ImageReader(buf), x, y, w, h)
        except Exception as e:
            print(f"  img {key}: {e}")

def slide_header(c, sublabel, title, label_y=None, title_y=None):
    top_bar(c)
    if label_y is None: label_y = H - 18
    if title_y is None: title_y = H - 38
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(ORANGE)
    c.drawString(22, label_y, sublabel)
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(WHITE_C)
    c.drawString(22, title_y, title)
    # orange divider line
    c.setFillColor(ORANGE)
    c.rect(22, H - 52, 80, 2.5, fill=1, stroke=0)

def divider_card(c, x, y, w, h):
    rect_fill(c, x, y, w, h, NAVY_MID, ORANGE, 0.6)

# ── SLIDES ────────────────────────────────────────────────────────────────────
c = canvas.Canvas(OUT, pagesize=landscape(A4))
c.setTitle("No salir de día — Trabajo Final Iluminación y Render")

# ════════════════════════════════════════════
# SLIDE 1 — PORTADA
# ════════════════════════════════════════════
bg(c)
# right accent bar
c.setFillColor(ORANGE)
c.rect(W - 30, 0, 18, H, fill=1, stroke=0)
c.setFillColor(NAVY_MID)
c.rect(W - 48, 0, 16, H, fill=1, stroke=0)

c.setFont("Helvetica-Bold", 8)
c.setFillColor(ORANGE)
c.drawString(26, H - 28, "TRABAJO FINAL — ILUMINACIÓN Y RENDER")

c.setFont("Helvetica-Bold", 56)
c.setFillColor(WHITE_C)
c.drawString(26, H - 100, "NO SALIR")
c.drawString(26, H - 160, "DE DÍA")

c.setFont("Helvetica", 14)
c.setFillColor(LGRAY)
c.drawString(26, H - 195, "Escenario de iluminación cinematográfica  ·  Unreal Engine 5")
c.setFont("Helvetica", 11)
c.setFillColor(ORANGE)
c.drawString(26, H - 212, "Modalidad A — Opción Cinematográfica  ·  4 secuencias")

c.setFillColor(LGRAY)
c.rect(26, H - 230, 200, 1.5, fill=1, stroke=0)

c.setFont("Helvetica", 10)
c.setFillColor(LGRAY)
c.drawString(26, H - 248, "EUNEIZ  ·  Grado en Arte para Videojuegos  ·  Curso 2025–26")
c.showPage()

# ════════════════════════════════════════════
# SLIDE 2 — CONCEPTO Y NARRATIVA
# ════════════════════════════════════════════
bg(c)
slide_header(c, "CONCEPTO Y NARRATIVA", '"En combate, la luz del día es el enemigo"')

concept = (
    "Cuatro secuencias cinematográficas narran la espera en una trinchera de la Primera\n"
    "Guerra Mundial. Salir durante el día significa muerte segura: la luz, normalmente\n"
    "asociada a la vida, se convierte aquí en amenaza. La oscuridad del atardecer es el\n"
    "único momento de acción posible."
)
y0 = H - 75
c.setFont("Helvetica", 10)
c.setFillColor(LGRAY)
for line in concept.split("\n"):
    c.drawString(22, y0, line)
    y0 -= 14

seqs = [
    ("SEC. 1", "ESTABLISHING",  "Plano general.", "Contextualiza el espacio."),
    ("SEC. 2", "ARSENAL",       "Close-up DoF.", "Implica presencia humana."),
    ("SEC. 3", "TRAVELLING",    "Dolly + cartel.", '"Keep to the trench."'),
    ("SEC. 4", "SUNSET",        "Exterior. Sol en horizonte.", "La noche llega."),
]
cw, ch = 185, 145
cx0 = 22
cy0 = 30
for i, (num, title, d1, d2) in enumerate(seqs):
    x = cx0 + i * (cw + 8)
    y = cy0
    divider_card(c, x, y, cw, ch)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(ORANGE)
    c.drawString(x + 8, y + ch - 16, num)
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(WHITE_C)
    c.drawString(x + 8, y + ch - 34, title)
    c.setFillColor(ORANGE)
    c.rect(x + 8, y + ch - 42, cw - 16, 1.5, fill=1, stroke=0)
    c.setFont("Helvetica", 9)
    c.setFillColor(LGRAY)
    c.drawString(x + 8, y + ch - 56, d1)
    c.drawString(x + 8, y + ch - 70, d2)

c.showPage()

# ════════════════════════════════════════════
# SLIDE 3 — SETUP TÉCNICO
# ════════════════════════════════════════════
bg(c)
slide_header(c, "SETUP TÉCNICO", "Motor  ·  Luces  ·  Render")

left = [
    ("MOTOR",              "Unreal Engine 5"),
    ("ILUMINACIÓN GLOBAL", "Lumen — Dynamic GI + Reflections"),
    ("SOMBRAS",            "Virtual Shadow Maps"),
    ("PIPELINE DE RENDER", "Movie Render Queue (offline)"),
    ("FRAME RATE",         "24 fps — look cinematográfico"),
    ("ANTI-ALIASING",      "TSR — Temporal Super Resolution"),
    ("ASSET BASE",         "FAB Trench — luces / cámaras reconstruidos"),
]
right = [
    ("KEY LIGHT",          "Directional Light — Movable"),
    ("FILL LIGHT",         "Sky Light — Real Time Capture"),
    ("COLOR TEMPERATURE",  "3.500 K  (ámbar cálido)"),
    ("VOLUMETRIC FOG",     "Exponential Height Fog  ·  Density 0.02"),
    ("LENTES",             "35 mm  ·  50 mm  (Cine Camera Actor)"),
    ("APERTURA",           "f/2  →  f/8  según secuencia"),
    ("RESOLUCIÓN",         "1920 × 1080 — 24 fps"),
]

y0 = H - 68
for lbl, val in left:
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(ORANGE)
    c.drawString(22, y0, lbl)
    c.setFont("Helvetica", 10)
    c.setFillColor(WHITE_C)
    c.drawString(22, y0 - 12, val)
    y0 -= 32

y0 = H - 68
for lbl, val in right:
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(ORANGE)
    c.drawString(W // 2 + 10, y0, lbl)
    c.setFont("Helvetica", 10)
    c.setFillColor(WHITE_C)
    c.drawString(W // 2 + 10, y0 - 12, val)
    y0 -= 32

# vertical divider
c.setFillColor(DGRAY)
c.rect(W // 2, H - 60, 1.5, H - 90, fill=1, stroke=0)
c.showPage()

# ════════════════════════════════════════════
# SLIDE 4 — ILUMINACIÓN
# ════════════════════════════════════════════
bg(c)
slide_header(c, "ILUMINACIÓN", "Key  ·  Fill  ·  Atmósfera volumétrica")

cols = [
    ("KEY LIGHT", "Directional Light",
     ["Mobility: Movable", "Intensity: 8–10 lux", "Color Temp: 3.500 K",
      "Source Angle: 1.5", "Atmosphere Sun Light: ON",
      "Cast Volumetric Shadow: ON", "Vol. Scattering Int.: 2.0"]),
    ("FILL / SKY", "Sky Light",
     ["Source: Real Time Capture", "Intensity Scale: 0.4",
      "Sky Atmosphere vinculada", "No compite con la key",
      "Evita negros absolutos", "Lower Hemisphere: Color"]),
    ("ATMÓSFERA", "Volumetric Fog + Lumen",
     ["Fog Density: 0.02", "Scattering Dist.: 0.6",
      "Inscattering: ámbar oscuro", "Lumen GI Quality: 2",
      "God rays vía Cast Vol. Shadow", "Niebla en zonas de haces"]),
]
cw2 = 250
for i, (title, sub, items) in enumerate(cols):
    x = 22 + i * (cw2 + 10)
    y_top = H - 60
    ch2 = H - 60 - 22
    divider_card(c, x, 22, cw2, ch2)
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(ORANGE)
    c.drawString(x + 8, y_top - 16, title)
    c.setFont("Helvetica", 9)
    c.setFillColor(WHITE_C)
    c.drawString(x + 8, y_top - 30, sub)
    c.setFillColor(ORANGE)
    c.rect(x + 8, y_top - 36, cw2 - 16, 1.5, fill=1, stroke=0)
    c.setFont("Helvetica", 9)
    c.setFillColor(LGRAY)
    for j, item in enumerate(items):
        c.drawString(x + 12, y_top - 50 - j * 20, "· " + item)
c.showPage()

# ════════════════════════════════════════════
# SLIDE 5 — SEC 1 ESTABLISHING
# ════════════════════════════════════════════
bg(c, NAVY_DARK)
slide_header(c, "SECUENCIA 1 — ESTABLISHING SHOT", "Plano general  ·  Presentación del escenario")

draw_img(c, "017", 18, 22, 510, 285)

data5 = [
    ("TIPO DE PLANO",  "Plano General (Establishing Shot)"),
    ("LENTE",          "35 mm — ángulo amplio"),
    ("APERTURA",       "f/8 — profundidad de campo total"),
    ("COMPOSICIÓN",    "Líneas guía convergentes al punto de fuga central"),
    ("KEY LIGHT",      "Directional lateral-superior + god rays Vol. Fog"),
    ("COLOR",          "Dominante ámbar 3500 K · Sky fill neutro en sombras"),
    ("RATIO",          "2.39:1 Cinemascope (letterbox)"),
]
y0 = H - 68
x1 = 545
for lbl, val in data5:
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(ORANGE)
    c.drawString(x1, y0, lbl)
    c.setFont("Helvetica", 9.5)
    c.setFillColor(WHITE_C)
    c.drawString(x1, y0 - 11, val)
    y0 -= 33
c.showPage()

# ════════════════════════════════════════════
# SLIDE 6 — SEC 2 ARSENAL
# ════════════════════════════════════════════
bg(c, NAVY_DARK)
slide_header(c, "SECUENCIA 2 — ARSENAL", "Close-up  ·  Cajas de munición  ·  DoF extremo")

draw_img(c, "019", 18, 22, 510, 285)

data6 = [
    ("TIPO DE PLANO",  "Primer plano · ángulo bajo (cámara al suelo)"),
    ("LENTE",          "50 mm — compresión de perspectiva"),
    ("APERTURA",       "f/2 — bokeh muy pronunciado"),
    ("FOCO",           "Manual focus en cajas · foreground desenfocado"),
    ("ILUMINACIÓN",    "Rim light cálido lateral · fondo en penumbra"),
    ("NARRATIVA",      "Escala humana implícita · vida sin mostrar personas"),
    ("COLOR",          "Ámbar saturado sobre negro · contraste térmico máximo"),
]
y0 = H - 68
x1 = 545
for lbl, val in data6:
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(ORANGE)
    c.drawString(x1, y0, lbl)
    c.setFont("Helvetica", 9.5)
    c.setFillColor(WHITE_C)
    c.drawString(x1, y0 - 11, val)
    y0 -= 33
c.showPage()

# ════════════════════════════════════════════
# SLIDE 7 — SEC 3 TRAVELLING + CARTEL
# ════════════════════════════════════════════
bg(c, NAVY_DARK)
slide_header(c, "SECUENCIA 3 — TRAVELLING + CARTEL",
             'Dolly forward  ·  Pull focus  ·  "Keep to the trench in daylight"')

# Two images side by side
iw2 = 380
ih2 = 220
draw_img(c, "020", 18, H - 58 - ih2, iw2, ih2)
draw_img(c, "021", iw2 + 28, H - 58 - ih2, iw2, ih2)

c.setFont("Helvetica", 8)
c.setFillColor(LGRAY)
c.drawString(18, H - 58 - ih2 - 12, "Inicio — dolly con god rays a contraluz")
c.drawString(iw2 + 28, H - 58 - ih2 - 12, "Final — close-up cartel en penumbra total")

notes7 = ("Lente: 35 mm → 50 mm  ·  Apertura: f/4 → f/2  ·  "
          "Movimiento: Dolly forward (Sequencer, ease-in/out)  ·  "
          "Pull focus dinámico: de la niebla al cartel  ·  "
          "Iluminación: contraluz key + Vol. Fog → oscuridad total")
y_notes = H - 58 - ih2 - 30
c.setFont("Helvetica", 8)
c.setFillColor(ORANGE)
# wrap manually
words = notes7.split("  ·  ")
for idx, seg in enumerate(words):
    xx = 18 + idx * 195
    if xx + 185 > W:
        xx = 18 + (idx % 4) * 195
        y_notes -= 12
    c.drawString(xx, y_notes, "· " + seg)
c.showPage()

# ════════════════════════════════════════════
# SLIDE 8 — SEC 4 SUNSET
# ════════════════════════════════════════════
bg(c, NAVY_DARK)
slide_header(c, "SECUENCIA 4 — SUNSET", "Plano exterior  ·  El sol se pone  ·  La noche llega")

draw_img(c, "022", 18, 22, 510, 285)

data8 = [
    ("TIPO DE PLANO",  "Plano general exterior desde la trinchera"),
    ("LENTE",          "35 mm — campo amplio"),
    ("APERTURA",       "f/8 — todo en foco"),
    ("ILUMINACIÓN",    "Directional casi en horizonte · sol a 2–3°"),
    ("COLOR",          "Rojo-naranja dominante · siluetas en negro"),
    ("VOLUMETRIC",     "Humo + fog denso · campo de batalla"),
    ("NARRATIVA",      "La oscuridad = libertad · el sol = cuenta atrás"),
]
y0 = H - 68
x1 = 545
for lbl, val in data8:
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(ORANGE)
    c.drawString(x1, y0, lbl)
    c.setFont("Helvetica", 9.5)
    c.setFillColor(WHITE_C)
    c.drawString(x1, y0 - 11, val)
    y0 -= 33
c.showPage()

# ════════════════════════════════════════════
# SLIDE 9 — PALETA Y MOOD
# ════════════════════════════════════════════
bg(c)
slide_header(c, "PALETA CROMÁTICA Y MOOD", "Psicología del color aplicada")

swatches = [
    (HexColor("#D47A00"), "ÁMBAR / OCRE",
     "Dominante cálida · 3500K Directional", "Peligro · Urgencia · Calor"),
    (HexColor("#E84010"), "ROJO-NARANJA",
     "Sunset (sec. 4) · Sol en horizonte", "Sangre · Guerra · Alerta"),
    (HexColor("#100A04"), "NEGRO PROFUNDO",
     "Sombras Lumen · Siluetas", "Muerte · Opresión · Claustrofobia"),
    (HexColor("#8A7040"), "TIERRA / SEPIA",
     "Base color del asset · Madera/Arena", "Guerra · Abandono · Historia"),
]
sw_w, sw_h = 175, 90
for i, (col, name, d1, d2) in enumerate(swatches):
    x = 22 + i * (sw_w + 12)
    y_sw = H - 60 - sw_h
    c.setFillColor(col)
    c.setStrokeColor(col)
    c.rect(x, y_sw, sw_w, sw_h, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(WHITE_C)
    c.drawString(x, y_sw - 14, name)
    c.setFont("Helvetica", 8)
    c.setFillColor(LGRAY)
    c.drawString(x, y_sw - 26, d1)
    c.drawString(x, y_sw - 38, d2)

# Divider + mood text
c.setFillColor(DGRAY)
c.rect(22, 80, W - 44, 1.5, fill=1, stroke=0)

mood = ("La inversión psicológica del color es el eje narrativo: la LUZ cálida (ámbar, rojo) "
        "representa el PELIGRO, mientras la OSCURIDAD es la única vía de supervivencia. "
        "Lumen amplifica este contraste saturando las zonas iluminadas y hundiendo las sombras.")
c.setFont("Helvetica", 9)
c.setFillColor(LGRAY)
# manual wrap at ~100 chars
words_m = mood.split(" ")
line_m, lines_m = "", []
for w in words_m:
    if len(line_m) + len(w) < 115:
        line_m += w + " "
    else:
        lines_m.append(line_m.strip())
        line_m = w + " "
if line_m:
    lines_m.append(line_m.strip())
ym = 68
for ln in lines_m:
    c.drawString(22, ym, ln)
    ym -= 12
c.showPage()

# ════════════════════════════════════════════
# SLIDE 10 — CRITERIOS
# ════════════════════════════════════════════
bg(c)
slide_header(c, "CRITERIOS DE EVALUACIÓN",
             "Alineación del trabajo con los criterios de la asignatura")

criteria = [
    (40, "ILUMINACIÓN",
     "Directional 3500K + Sky Light + Lumen GI. Vol. Fog (0.02) con Cast Vol. Shadow para god rays. "
     "Temperatura y ángulo solar consistentes en las 4 secuencias."),
    (20, "MOOD Y ATMÓSFERA",
     "Paleta ámbar/rojo/negro. Niebla volumétrica que refuerza la tensión. "
     "Inversión psicológica: luz = peligro, oscuridad = escape."),
    (15, "COMPOSICIÓN",
     "Líneas guía (paredes trinchera). Regla de tercios. Variedad: general → close-up → dolly → exterior. "
     "Ratio 2.39:1 con letterbox."),
    (10, "ASPECTOS TÉCNICOS",
     "Lumen + Virtual Shadow Maps. Movie Render Queue 24fps. Lentes 35mm/50mm. "
     "f/2–f/8. Asset FAB con iluminación reconstruida íntegramente."),
    (15, "SEGUIMIENTO",
     "4 secuencias completas entregadas. Breakdown del motor. "
     "Narrativa coherente documentada desde concepto hasta render final."),
]

y0 = H - 68
rh = 80
for pct, title, desc in criteria:
    # badge
    c.setFillColor(ORANGE)
    c.rect(22, y0 - rh + 18, 42, 34, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(WHITE_C)
    c.drawCentredString(43, y0 - rh + 30, f"{pct}%")
    # title
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(ORANGE)
    c.drawString(74, y0 - rh + 45, title)
    # desc (wrap)
    c.setFont("Helvetica", 8.5)
    c.setFillColor(LGRAY)
    words_d = desc.split(" ")
    line_d, lines_d = "", []
    for w in words_d:
        if len(line_d) + len(w) < 110:
            line_d += w + " "
        else:
            lines_d.append(line_d.strip())
            line_d = w + " "
    if line_d:
        lines_d.append(line_d.strip())
    for li, ln in enumerate(lines_d[:2]):
        c.drawString(74, y0 - rh + 30 - li * 11, ln)
    y0 -= rh

c.showPage()
c.save()
print("PDF guardado en:", OUT)
