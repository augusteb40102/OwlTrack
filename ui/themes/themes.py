import flet as ft

# ─────────────────────────────────────────
# PURPLE THEME (default)
# ─────────────────────────────────────────
PURPLE_PRIMARY = "#2D1B69"
PURPLE_SECONDARY = "#7C3AED"
PURPLE_ACCENT = "#3b82f6"
PURPLE_BACKGROUND = "#E8DEFF"
PURPLE_SURFACE = "#F3EEFF"
PURPLE_BORDER = "#2D1B69"
PURPLE_TEXT_PRIMARY = "#1a1040"
PURPLE_TEXT_SECONDARY = "#6B5A9E"
PURPLE_GRADIENT_COLORS = ["#C4B0FF", "#E8DEFF"]

# ─────────────────────────────────────────
# BLUE THEME
# ─────────────────────────────────────────
BLUE_PRIMARY = "#1B3A69"
BLUE_SECONDARY = "#3A7AED"
BLUE_ACCENT = "#60a5fa"
BLUE_BACKGROUND = "#DEE8FF"
BLUE_SURFACE = "#EEF3FF"
BLUE_BORDER = "#1B3A69"
BLUE_TEXT_PRIMARY = "#0F1F40"
BLUE_TEXT_SECONDARY = "#3A5A9E"
BLUE_GRADIENT_COLORS = ["#A0B8FF", "#DEE8FF"]

# ─────────────────────────────────────────
# GREY THEME
# ─────────────────────────────────────────
GREY_PRIMARY = "#2D2D2D"
GREY_SECONDARY = "#5A5A5A"
GREY_ACCENT = "#9ca3af"
GREY_BACKGROUND = "#E8E8E8"
GREY_SURFACE = "#F3F3F3"
GREY_BORDER = "#2D2D2D"
GREY_TEXT_PRIMARY = "#1a1a1a"
GREY_TEXT_SECONDARY = "#6B6B6B"
GREY_GRADIENT_COLORS = ["#C4C4C4", "#E8E8E8"]

# ─────────────────────────────────────────
# GREEN THEME
# ─────────────────────────────────────────
GREEN_PRIMARY = "#1B5E35"
GREEN_SECONDARY = "#22c55e"
GREEN_ACCENT = "#4ade80"
GREEN_BACKGROUND = "#DEF5E8"
GREEN_SURFACE = "#EEF9F2"
GREEN_BORDER = "#1B5E35"
GREEN_TEXT_PRIMARY = "#0F2B1A"
GREEN_TEXT_SECONDARY = "#3A7A55"
GREEN_GRADIENT_COLORS = ["#A0DFB8", "#DEF5E8"]

# ─────────────────────────────────────────
# ACTIVE THEME (default: purple)
# ─────────────────────────────────────────
PRIMARY = PURPLE_PRIMARY
SECONDARY = PURPLE_SECONDARY
ACCENT = PURPLE_ACCENT
BACKGROUND = PURPLE_BACKGROUND
SURFACE = PURPLE_SURFACE
BORDER = PURPLE_BORDER
TEXT_PRIMARY = PURPLE_TEXT_PRIMARY
TEXT_SECONDARY = PURPLE_TEXT_SECONDARY
GRADIENT_COLORS = PURPLE_GRADIENT_COLORS
 
# Nepriklauso nuo temos
TEXT_ON_PRIMARY = "#FFFFFF"
TEXT_ON_SURFACE = "#2D1B69"
ERROR = "#ef4444"
SUCCESS = "#22c55e"
TRANSPARENT = ft.Colors.TRANSPARENT
OVERLAY_SURFACE = "#1A1A2E80"
BACKGROUND_DARK = "#0D0D1A"

# ─────────────────────────────────────────
# OWL COLORS
# ─────────────────────────────────────────
OWL_BODY = "#7C3AED"
OWL_HEAD = "#6D28D9"
OWL_WING = "#5B21B6"
OWL_BELLY = "#DDD6FE"
OWL_EYE = "#FDE68A"
OWL_PUPIL = "#1C1917"
OWL_BEAK = "#F59E0B"

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