import os
import sys

# Ensure Python can resolve all modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from database.connection import DatabaseConnection
from scheduler.scheduler import AirfareScheduler

def main():
    print("========================================")
    print("AIRFARE PRICE INDEX SCRAPER")
    print("========================================")
    print("Initializing Airfare Scraping System...")
    print("Checking database...")

    db = DatabaseConnection()
    if not db.connect():
        print("Database connection: FAILED. Please verify MySQL credentials in .env.")
        print("Exiting.")
        return

    print("Loading sources...")
    interval = int(os.getenv("SCRAPE_INTERVAL_MINUTES", "30"))
    scheduler = AirfareScheduler(interval_minutes=interval)
    print(f"Sources loaded: {len(scheduler.sources)}")
    print(f"Interval: {interval} minutes")
    print("Scheduler: READY")

    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("\nScraper stopped by user.")
    except Exception as e:
        print(f"\nScraper encountered an error: {e}")

if __name__ == "__main__":
    main()
