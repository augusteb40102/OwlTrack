import smtplib
import time
import logging
import secrets
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
from database import save_reset_token

load_dotenv()

# Logging konfiguracija
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

# Saugome paskutinio siuntimo laiką
_last_request: dict = {}

def generate_reset_token() -> str:
    """Generuoja 32 simbolių hex reset tokeną"""
    return secrets.token_hex(16)

def send_reset_email(to_email: str, reset_token: str) -> dict:
    """
    Siunčia slaptažodžio atstatymo laišką
    Returns: {"success": bool, "message": str}
    """
    # Tikriname ar praėjo 1 minutė
    now = time.time()
    if to_email in _last_request:
        elapsed = now - _last_request[to_email]
        if elapsed < 60:
            remaining = int(60 - elapsed)
            logger.warning(f"Rate limit: {to_email} – liko {remaining} sek")
            return {"success": False, "message": "rate_limited", "remaining": remaining}
    
    _last_request[to_email] = now
    
    # Saugoti tokeną į duomenų bazę su 10 minučių galiojimo laiku
    expires_at = (datetime.now() + timedelta(minutes=10)).isoformat()
    if not save_reset_token(to_email, reset_token, expires_at):
        logger.error(f"Nepavyko saugoti reset tokeno: {to_email}")
        return {"success": False, "message": "database_error"}
    
    reset_link = f"https://owltrack.app/reset-password?token={reset_token}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "OwlTrack – Password Reset"
    msg["From"] = GMAIL_USER
    msg["To"] = to_email

    html = f"""
    <div style="font-family: sans-serif; max-width: 520px; margin: 0 auto;">
        <div style="background: #2D1B69; padding: 2rem; text-align: center; border-radius: 12px 12px 0 0;">
            <p style="color: #ffffff; font-size: 22px; font-weight: bold; margin: 0;">🦉 OwlTrack</p>
        </div>
        <div style="padding: 2rem; border: 1px solid #e2e8f0; border-radius: 0 0 12px 12px;">
            <p style="font-size: 18px; font-weight: bold;">Password reset request</p>
            <p style="color: #64748b;">We received a request to reset your OwlTrack password. Click the button below to set a new password.</p>
            <div style="text-align: center; margin: 2rem 0;">
                <a href="{reset_link}" style="background: #2D1B69; color: #ffffff; padding: 12px 32px; border-radius: 999px; text-decoration: none; font-weight: bold;">
                    Reset my password
                </a>
            </div>
            <div style="background: #f8fafc; padding: 12px; border-radius: 8px;">
                <p style="font-size: 13px; color: #64748b; margin: 0;">
                    This link expires in <strong>10 minutes</strong>. 
                    If you did not request a password reset, please ignore this email.
                </p>
            </div>
        </div>
    </div>
    """

    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, to_email, msg.as_string())
        logger.info(f"Reset email sėkmingai išsiųstas: {to_email}")
        return {"success": True, "message": "Email sent"}
    except Exception as e:
        logger.error(f"Klaida siunčiant laišką {to_email}: {e}")
        return {"success": False, "message": "email_error"}
