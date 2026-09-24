import os
import random
from datetime import datetime, timedelta
from .base_scraper import BaseScraper, SourceUnavailableError

class GoogleFlightsScraper(BaseScraper):
    def __init__(self):
        super().__init__(source_name="Google Flights")
        self.base_url = "https://www.google.com/travel/flights"

    def scrape(self, route, departure_date):
        simulate = os.getenv("SIMULATE_DATA", "false").lower() == "true"
        if not simulate:
            raise SourceUnavailableError("Access unavailable (anti-bot / dynamic JavaScript challenge)")

        origin = route.get("origin")
        destination = route.get("destination")
        results = []
        num_records = random.randint(20, 45)

        airlines = [
            ("IndiGo", "6E"),
            ("Air India", "AI"),
            ("SpiceJet", "SG"),
            ("Vistara", "UK")
        ]

        for i in range(num_records):
            airline_name, code = random.choice(airlines)
            flight_no = f"{code}-{random.randint(100, 999)}"
            dept_hour = random.randint(5, 23)
            dept_min = random.choice([0, 10, 20, 30, 40, 50])
            duration = random.randint(75, 210)
            
            dept_time = datetime.strptime(f"{dept_hour:02d}:{dept_min:02d}", "%H:%M")
            arr_time = dept_time + timedelta(minutes=duration)
            
            base_fare = float(random.randint(3000, 8500))
            taxes = round(base_fare * 0.15, 2)
            total = base_fare + taxes

            results.append({
                "source": "Google Flights",
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
                "fare_class": "Standard",
                "base_fare": str(base_fare),
                "taxes": str(taxes),
                "total_fare": f"₹{total:,.2f}",
                "currency": "INR",
                "availability": random.randint(1, 12),
                "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        return results
