# src/mailer.py
import smtplib
import logging
import os
from email.message import EmailMessage

def send_email(to_email, subject, body, sender_email, sender_password, dry_run):
    """Ashol email pathanor logic (SMTP)."""
    if dry_run:
        logging.info(f"[DRY RUN] Email would be sent to {to_email} | Subject: {subject}")
        return True

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        # SMTP configuration env theke nebe, default values deya ache
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", 587))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Connection secure korar jonno
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        logging.info(f"Success: Email sent to {to_email}")
        return True
        
    except Exception as e:
        logging.error(f"Failed: Could not send to {to_email}. Error: {e}")
        return False
