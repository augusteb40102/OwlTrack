import smtplib
import time
import logging
import secrets
import string
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import sys
from database import save_reset_token

# Rasti .env failą nepriklausomai nuo to kur paleidžiama
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(BASE_DIR) == "logic":
        BASE_DIR = os.path.dirname(BASE_DIR)

dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=dotenv_path)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GMAIL_USER     = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

if not GMAIL_USER or not GMAIL_PASSWORD:
    logger.error(f"Nerasti SMTP kredencialai: GMAIL_USER/GMAIL_PASSWORD (ieškota: {dotenv_path})")

_last_request: dict = {}

def generate_reset_token() -> str:
    """Generuoja 10 simbolių vienkartinį kodą (raidės + skaičiai + paprasti ženklai)"""
    alphabet = string.ascii_uppercase + string.digits + "!@#$%"
    return ''.join(secrets.choice(alphabet) for _ in range(10))

def send_reset_email(to_email: str, reset_token: str) -> dict:
    if not GMAIL_USER or not GMAIL_PASSWORD:
        logger.error("GMAIL_USER arba GMAIL_PASSWORD nenurodyti .env faile")
        return {"success": False, "message": "email_error"}

    now = time.time()
    if to_email in _last_request:
        elapsed = now - _last_request[to_email]
        if elapsed < 60:
            remaining = int(60 - elapsed)
            logger.warning(f"Rate limit: {to_email} – liko {remaining} sek")
            return {"success": False, "message": "rate_limited", "remaining": remaining}

    _last_request[to_email] = now

    expires_at = (datetime.now() + timedelta(minutes=10)).isoformat()
    if not save_reset_token(to_email, reset_token, expires_at):
        logger.error(f"Nepavyko saugoti reset tokeno: {to_email}")
        return {"success": False, "message": "database_error"}

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "OwlTrack – Your Temporary Login Code"
    msg["From"]    = GMAIL_USER
    msg["To"]      = to_email

    html = f"""
    <div style="font-family: sans-serif; max-width: 520px; margin: 0 auto;">
        <div style="background: #2D1B69; padding: 2rem; text-align: center; border-radius: 12px 12px 0 0;">
            <p style="color: #ffffff; font-size: 22px; font-weight: bold; margin: 0;">🦉 OwlTrack</p>
        </div>
        <div style="padding: 2rem; border: 1px solid #e2e8f0; border-radius: 0 0 12px 12px;">
            <p style="font-size: 18px; font-weight: bold; color: #1a1040;">Your temporary code</p>
            <p style="color: #64748b;">Use the code below to log in to your OwlTrack account.</p>
            <div style="text-align: center; margin: 2rem 0;">
                <div style="display: inline-block; background: #F3EEFF; border: 2px solid #2D1B69; border-radius: 12px; padding: 16px 40px;">
                    <p style="font-size: 36px; font-weight: bold; letter-spacing: 10px; color: #2D1B69; margin: 0;">{reset_token}</p>
                </div>
                <p style="font-size: 12px; color: #94a3b8; margin-top: 10px;">This code expires 10 minutes after delivery — use it before it's gone.</p>
            </div>
            <div style="background: #f8fafc; padding: 12px; border-radius: 8px;">
                <p style="font-size: 13px; color: #64748b; margin: 0;">
                    Once used to log in, it remains your password until you change it in <strong>Settings</strong>.
                    If you did not request this, please ignore this email.
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