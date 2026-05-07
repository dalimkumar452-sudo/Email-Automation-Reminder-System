# src/scheduler.py
import pandas as pd
import schedule
import os
import logging
from datetime import datetime
from src.mailer import send_email

def log_report(name, email, subject, status):
    """Email pathanor por status CSV te save korbe."""
    os.makedirs("outputs", exist_ok=True)
    report_file = "outputs/delivery_report.csv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    df = pd.DataFrame([[timestamp, name, email, subject, status]], 
                      columns=["Timestamp", "Name", "Email", "Subject", "Status"])
    
    df.to_csv(report_file, mode='a', header=not os.path.exists(report_file), index=False)

def process_and_send(contact_name, contact_email, subject, template_file, sender_email, sender_password, dry_run):
    """Template theke nam replace kore email send korbe aur log korbe."""
    try:
        with open(f"templates/{template_file}", "r") as file:
            template = file.read()
        
        # Dynamic name replace
        body = template.format(name=contact_name)
        
        # Mailer ke call kora hocche
        status = send_email(contact_email, subject, body, sender_email, sender_password, dry_run)
        log_report(contact_name, contact_email, subject, "Sent" if status else "Failed")

    except FileNotFoundError:
        logging.error(f"Error: Template 'templates/{template_file}' not found.")
        log_report(contact_name, contact_email, subject, "Failed - Missing Template")

def load_jobs(sender_email, sender_password, dry_run):
    """CSV theke data read kore task schedule korbe."""
    try:
        contacts = pd.read_csv("data/contacts.csv")
        reminders = pd.read_csv("data/reminders.csv")
        
        # Data merge (Inner join based on contact_id)
        df = pd.merge(reminders, contacts, on="contact_id")
        
        logging.info(f"Successfully loaded {len(df)} reminder tasks.")
        
        for _, row in df.iterrows():
            # Time onujayi task schedule kora hocche
            schedule.every().day.at(row['send_time']).do(
                process_and_send, 
                row['name'], 
                row['email'], 
                row['subject'], 
                row['template_name'],
                sender_email,
                sender_password,
                dry_run
            )
            logging.info(f"Scheduled: '{row['subject']}' for {row['name']} at {row['send_time']}")
            
    except Exception as e:
        logging.error(f"System Error loading CSV data: {e}")