import flet as ft

# ─────────────────────────────────────────
# COLORS
# ─────────────────────────────────────────
PRIMARY = "#2D1B69"       # Tamsi violetinė
SECONDARY = "#7C3AED"     # Violetinė
ACCENT = "#3b82f6"        # Mėlynas akcentas

BACKGROUND = "#E8DEFF"    # Šviesiai violetinis
SURFACE = "#F3EEFF"       # Kortelių, inputų fonas
BORDER = "#2D1B69"        # Kraštinės

TEXT_PRIMARY = "#1a1040"    # Tamsus tekstas
TEXT_SECONDARY = "#6B5A9E"  # Antrinis violetinis tekstas
TEXT_ON_PRIMARY = "#FFFFFF" # Tekstas ant tamsių mygtukų
TEXT_ON_SURFACE = "#2D1B69" # Tekstas ant šviesių mygtukų

ERROR = "#ef4444"         # Klaidos
SUCCESS = "#22c55e"       # Sėkmė
TRANSPARENT = ft.Colors.TRANSPARENT

# Specifinės UI spalvos
OVERLAY_SURFACE = "#1A1A2E80"
BACKGROUND_DARK = "#0D0D1A"

GRADIENT_COLORS = ["#C4B0FF", "#E8DEFF"]

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
        color=TEXT_ON_SURFACE,
        bgcolor=SURFACE,
        shape=ft.RoundedRectangleBorder(radius=RADIUS_MD),
        side=ft.BorderSide(width=2, color=PRIMARY),
    )

def ghost_button_style():
    return ft.ButtonStyle(
        color=SECONDARY,
        bgcolor=TRANSPARENT,
        shape=ft.RoundedRectangleBorder(radius=RADIUS_FULL),
    )

# ─────────────────────────────────────────
# INPUT STYLES
# ─────────────────────────────────────────
def input_style():
    return {
        "bgcolor": SURFACE,
        "border_color": BORDER,
        "focused_border_color": SECONDARY,
        "text_style": ft.TextStyle(color=TEXT_PRIMARY),
        "label_style": ft.TextStyle(color=TEXT_SECONDARY),
        "border_radius": RADIUS_LG,
    }