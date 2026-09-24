import schedule
import time
import json
import os
from datetime import datetime
from database import get_db_connection
from scrapers.mock_scraper import MockScraper
from processors.normalizer import FareNormalizer
from processors.validator import DataValidator
from processors.deduplicator import DuplicateDetector

class AirfareScheduler:
    """
    Manages the automated execution of the scraping pipeline based on configured routes.
    """
    
    def __init__(self, interval_minutes=30):
        self.interval_minutes = interval_minutes
        self.routes_file = os.path.join(os.path.dirname(__file__), '..', 'config', 'routes.json')
        
    def load_active_routes(self):
        try:
            with open(self.routes_file, 'r') as f:
                routes = json.load(f)
                return [r for r in routes if r.get('active', False)]
        except Exception as e:
            print(f"Error loading routes: {e}")
            return []

    def run_pipeline(self):
        print(f"\n--- Starting Scrape Pipeline at {datetime.now()} ---")
        
        routes = self.load_active_routes()
        if not routes:
            print("No active routes found. Exiting pipeline.")
            return

        db_conn = get_db_connection()
        if not db_conn:
            print("Database connection failed. Cannot proceed.")
            return

        # Initialize components
        scrapers = [MockScraper()] # Add real scrapers here later
        deduplicator = DuplicateDetector(db_conn)
        cursor = db_conn.cursor()

        # Set target date (e.g., 10 days from now)
        # In a real system, you'd iterate over multiple future dates
        target_date = "2026-10-10"
        scrape_timestamp = datetime.now()

        for route in routes:
            origin = route["origin"]
            dest = route["destination"]
            
            for scraper in scrapers:
                try:
                    # 1. Scrape Raw Data
                    raw_observations = scraper.search_fares(origin, dest, target_date)
                    
                    saved_count = 0
                    duplicate_count = 0
                    invalid_count = 0
                    
                    for raw_obs in raw_observations:
                        # 2. Add timestamp
                        raw_obs["scraped_at"] = scrape_timestamp
                        
                        # Calculate lead time
                        departure = datetime.strptime(raw_obs["departure_date"], "%Y-%m-%d")
                        raw_obs["lead_time_days"] = (departure - scrape_timestamp).days
                        
                        # 3. Standardize Data
                        normalized_obs = FareNormalizer.normalize_observation(raw_obs)
                        
                        # 4. Validate
                        is_valid, error_msg = DataValidator.validate(normalized_obs)
                        if not is_valid:
                            print(f"Invalid record skipped: {error_msg}")
                            invalid_count += 1
                            continue
                            
                        # 5. Check Duplicates
                        if deduplicator.is_duplicate(normalized_obs):
                            duplicate_count += 1
                            continue
                            
                        # 6. Insert into MySQL
                        insert_query = """
                            INSERT INTO airfare_observations (
                                source, source_type, airline, flight_number, origin, destination,
                                departure_date, departure_time, arrival_time, duration_minutes,
                                stops, fare_class, base_fare, taxes, fees, total_fare, currency,
                                availability, lead_time_days, booking_url, scraped_at
                            ) VALUES (
                                %(source)s, %(source_type)s, %(airline)s, %(flight_number)s, %(origin)s, %(destination)s,
                                %(departure_date)s, %(departure_time)s, %(arrival_time)s, %(duration_minutes)s,
                                %(stops)s, %(fare_class)s, %(base_fare)s, %(taxes)s, %(fees)s, %(total_fare)s, %(currency)s,
                                %(availability)s, %(lead_time_days)s, %(booking_url)s, %(scraped_at)s
                            )
                        """
                        cursor.execute(insert_query, normalized_obs)
                        saved_count += 1
                    
                    db_conn.commit()
                    
                    print(f"Route {origin}-{dest}: Found {len(raw_observations)}, Saved {saved_count}, Duplicates {duplicate_count}, Invalid {invalid_count}")
                    
                    # Optional: Log to scrape_logs table here
                    
                except Exception as e:
                    print(f"Error processing route {origin}-{dest} with {scraper.__class__.__name__}: {e}")
                    db_conn.rollback()

        cursor.close()
        db_conn.close()
        print(f"--- Pipeline Finished at {datetime.now()} ---\n")

    def start(self):
        print(f"Scheduler started. Running every {self.interval_minutes} minutes.")
        # Run once immediately
        self.run_pipeline()
        
        # Schedule subsequent runs
        schedule.every(self.interval_minutes).minutes.do(self.run_pipeline)
        
        while True:
            schedule.run_pending()
            time.sleep(1)
