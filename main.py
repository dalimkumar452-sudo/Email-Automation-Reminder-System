# main.py
import time
import os
import logging
import schedule
from dotenv import load_dotenv
from src.scheduler import load_jobs

# Logs folder toiri kora aur logging setup kora
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/system.log"),
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":
    # .env theke data load kora
    load_dotenv()
    
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
    DRY_RUN = os.getenv("DRY_RUN", "True").lower() == "true"

    print("\n🚀 Starting Automated Email & Reminder System...")
    
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("❌ Error: SENDER_EMAIL or SENDER_PASSWORD not found in .env file.")
        exit(1)

    if DRY_RUN:
        print("⚠️ Running in DRY-RUN mode. No real emails will be sent.\n")
    
    # Scheduler ke start kora
    load_jobs(SENDER_EMAIL, SENDER_PASSWORD, DRY_RUN)
    
    print("\n⏳ System is running and waiting for scheduled times. Press Ctrl+C to stop.")
    
    # Infinite loop to keep checking the time
    while True:
        schedule.run_pending()
        time.sleep(1)