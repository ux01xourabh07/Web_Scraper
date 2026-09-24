import os
import json
import time
from datetime import datetime
import schedule

from database.connection import DatabaseConnection
from database.models import DataRepository
from pipeline.deduplicator import DuplicateDetector
from utils.logger import log_scrape_success, log_scrape_failure

# Import all source connectors
from scrapers.base_scraper import SourceUnavailableError
from scrapers.google_flights import GoogleFlightsScraper
from scrapers.skyscanner import SkyscannerScraper
from scrapers.kayak import KayakScraper
from scrapers.expedia import ExpediaScraper
from scrapers.momondo import MomondoScraper
from scrapers.hopper import HopperScraper
from scrapers.booking import BookingFlightsScraper
from scrapers.cheapoair import CheapOairScraper
from scrapers.cleartrip import CleartripScraper
from scrapers.makemytrip import MakeMyTripScraper

class AirfareScheduler:
    def __init__(self, interval_minutes=30):
        self.interval_minutes = int(os.getenv("SCRAPE_INTERVAL_MINUTES", interval_minutes))
        self.routes_file = os.path.join(os.path.dirname(__file__), '..', 'config', 'routes.json')
        self.db = DatabaseConnection()
        self.repo = DataRepository(self.db)
        self.deduplicator = None

        self.sources = [
            GoogleFlightsScraper(),
            SkyscannerScraper(),
            KayakScraper(),
            ExpediaScraper(),
            MomondoScraper(),
            HopperScraper(),
            BookingFlightsScraper(),
            CheapOairScraper(),
            CleartripScraper(),
            MakeMyTripScraper()
        ]

    def load_active_routes(self):
        try:
            with open(self.routes_file, 'r') as f:
                routes = json.load(f)
                return [r for r in routes if r.get('active', False)]
        except Exception:
            return [{"origin": "DEL", "destination": "BOM", "active": True}]

    def run_cycle(self):
        print("\nStarting scraping cycle...")
        started_at = datetime.now()
        
        conn = self.db.get_connection()
        if not conn:
            print("Database connection failed. Skipping cycle.")
            return

        self.deduplicator = DuplicateDetector(conn)
        routes = self.load_active_routes()
        target_date = "2026-10-15"

        total_collected = 0
        total_validated = 0
        total_rejected = 0
        total_inserted = 0

        for scraper in self.sources:
            source_name = scraper.source_name
            source_start = datetime.now()
            source_records = []
            status = "SUCCESS"
            err_msg = None

            try:
                for route in routes:
                    raw_data = scraper.scrape(route, target_date)
                    source_records.extend(raw_data)

                # Process pipeline: Normalization -> Validation -> Deduplication
                normalized_records = scraper.normalize(source_records)
                valid_records, rejected = scraper.validate(normalized_records)

                # Filter duplicates
                to_insert = [rec for rec in valid_records if not self.deduplicator.is_duplicate(rec)]
                
                # Insert via transaction
                inserted_count = self.repo.insert_fare_observations(to_insert)

                duration = round((datetime.now() - source_start).total_seconds(), 2)
                log_scrape_success(source_name, len(source_records), duration)
                print(f"[{source_name}] Status: SUCCESS Records: {len(source_records)}")

                total_collected += len(source_records)
                total_validated += len(valid_records)
                total_rejected += len(rejected)
                total_inserted += inserted_count

                self.repo.record_scrape_run(
                    source=source_name,
                    started_at=source_start.strftime("%Y-%m-%d %H:%M:%S"),
                    completed_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    status="SUCCESS",
                    records_found=len(source_records),
                    records_inserted=inserted_count,
                    records_rejected=len(rejected)
                )

            except SourceUnavailableError as e:
                status = "UNAVAILABLE"
                err_msg = str(e)
                log_scrape_failure(source_name, err_msg)
                print(f"[{source_name}] Status: UNAVAILABLE")
                self.repo.record_scrape_run(
                    source=source_name,
                    started_at=source_start.strftime("%Y-%m-%d %H:%M:%S"),
                    completed_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    status="UNAVAILABLE",
                    records_found=0,
                    records_inserted=0,
                    records_rejected=0,
                    error_message=err_msg
                )
            except Exception as e:
                status = "FAILED"
                err_msg = str(e)
                log_scrape_failure(source_name, err_msg)
                print(f"[{source_name}] Status: FAILED")
                self.repo.record_scrape_run(
                    source=source_name,
                    started_at=source_start.strftime("%Y-%m-%d %H:%M:%S"),
                    completed_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    status="FAILED",
                    records_found=0,
                    records_inserted=0,
                    records_rejected=0,
                    error_message=err_msg
                )

        print("----------------------------------------")
        print(f"TOTAL RECORDS: {total_collected}")
        print(f"Records validated: {total_validated}")
        print(f"Records rejected: {total_rejected}")
        print(f"Records inserted: {total_inserted}")
        print("----------------------------------------")
        print("Database insertion completed.")
        print("Scraping cycle completed successfully.")
        print(f"Next run in {self.interval_minutes} minutes.")

    def start(self):
        print(f"Starting scheduler...")
        print(f"Scheduler started.")
        # Execute immediate run
        self.run_cycle()

        # Schedule subsequent runs
        schedule.every(self.interval_minutes).minutes.do(self.run_cycle)
        while True:
            schedule.run_pending()
            time.sleep(1)
