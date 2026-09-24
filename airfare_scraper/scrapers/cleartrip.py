import os
import random
from datetime import datetime, timedelta
from .base_scraper import BaseScraper, SourceUnavailableError

class CleartripScraper(BaseScraper):
    def __init__(self):
        super().__init__(source_name="Cleartrip")

    def scrape(self, route, departure_date):
        # If simulated testing mode is disabled and live scraping is blocked by anti-bot/ToS
        simulate = os.getenv("SIMULATE_DATA", "false").lower() == "true"
        if not simulate:
            raise SourceUnavailableError("Access unavailable (Requires authorized API)")

        # In testing/simulation mode, generate realistic permitted test observations
        origin = route.get("origin")
        destination = route.get("destination")
        results = []
        num_records = random.randint(15, 30)

        airlines = [
            ("IndiGo", "6E"),
            ("Air India", "AI"),
            ("Vistara", "UK"),
            ("Akasa Air", "QP")
        ]

        for i in range(num_records):
            airline_name, code = random.choice(airlines)
            flight_no = f"{code}-{random.randint(100, 999)}"
            dept_hour = random.randint(6, 21)
            dept_min = random.choice([0, 15, 30, 45])
            duration = random.randint(90, 180)
            
            dept_time = datetime.strptime(f"{dept_hour:02d}:{dept_min:02d}", "%H:%M")
            arr_time = dept_time + timedelta(minutes=duration)
            
            base_fare = float(random.randint(3500, 7500))
            taxes = round(base_fare * 0.12, 2)
            total = base_fare + taxes

            results.append({
                "source": "Cleartrip",
                "origin": origin,
                "destination": destination,
                "departure_date": departure_date,
                "return_date": None,
                "trip_type": "One-way",
                "airline": airline_name,
                "flight_number": flight_no,
                "departure_time": dept_time.strftime("%H:%M:%S"),
                "arrival_time": arr_time.strftime("%H:%M:%S"),
                "duration_minutes": f"{duration // 60}h {duration % 60}m",
                "stops": 0,
                "cabin_class": "Economy",
                "fare_class": "Regular",
                "base_fare": str(base_fare),
                "taxes": str(taxes),
                "total_fare": f"₹{total:,.2f}",
                "currency": "INR",
                "availability": random.randint(1, 9),
                "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        return results
