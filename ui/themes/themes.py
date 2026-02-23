import flet as ft

# ─────────────────────────────────────────
# COLORS
# ─────────────────────────────────────────
PRIMARY = "#3b82f6"       # Mygtukai, akcentai
SECONDARY = "#f472b6"     # Papildoma spalva

BACKGROUND = "#FFFFFF"    # Pagrindinis fonas (dabar baltas)
SURFACE = "#f8fafc"       # Kortelių, inputų fonas
BORDER = "#e2e8f0"        # Kraštinės

TEXT_PRIMARY = "#0f172a"  # Pagrindinis tekstas
TEXT_SECONDARY = "#64748b" # Antrinis tekstas
TEXT_ON_PRIMARY = "#FFFFFF" # Tekstas ant mygtukų

ERROR = "#ef4444"         # Klaidos
SUCCESS = "#22c55e"       # Sėkmė

# Gradientas (kai naudojamas vietoj paprasto fono)
GRADIENT_COLORS = ["#0f172a", "#1e293b"]

# ─────────────────────────────────────────
# FONT SIZES
# ─────────────────────────────────────────
FONT_XL = 42     # Logotipas / Hero title
FONT_LG = 32     # Puslapio antraštė
FONT_MD = 20     # Sekcijų pavadinimai
FONT_SM = 16     # Subtitrai
FONT_XS = 14     # Paprastas tekstas
FONT_XXS = 12    # Smulkus tekstas

# ─────────────────────────────────────────
# SPACING
# ─────────────────────────────────────────
SPACE_XS = 4
SPACE_SM = 8
SPACE_MD = 16
SPACE_LG = 24
SPACE_XL = 40

# ─────────────────────────────────────────
# BORDER RADIUS
# ─────────────────────────────────────────
RADIUS_SM = 6
RADIUS_MD = 10
RADIUS_LG = 16
RADIUS_FULL = 999  # Apvalūs mygtukai

# ─────────────────────────────────────────
# GRADIENTS
# ─────────────────────────────────────────
def main_gradient():
    return ft.LinearGradient(
        begin=ft.Alignment(-1, -1),
        end=ft.Alignment(1, 1),
        colors=GRADIENT_COLORS,
    )

# ─────────────────────────────────────────
# BUTTON STYLES
# ─────────────────────────────────────────
def primary_button_style():
    return ft.ButtonStyle(
        color=TEXT_ON_PRIMARY,
        bgcolor=PRIMARY,
        shape=ft.RoundedRectangleBorder(radius=RADIUS_MD),
    )

def secondary_button_style():
    return ft.ButtonStyle(
        color=PRIMARY,
        bgcolor=SURFACE,
        shape=ft.RoundedRectangleBorder(radius=RADIUS_MD),
    )

def ghost_button_style():
    return ft.ButtonStyle(
        color=PRIMARY,
        bgcolor=ft.Colors.TRANSPARENT,
        shape=ft.RoundedRectangleBorder(radius=RADIUS_MD),
    )