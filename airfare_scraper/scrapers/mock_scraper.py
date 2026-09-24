from datetime import datetime, timedelta
import random
from .base_scraper import BaseScraper

class MockScraper(BaseScraper):
    """
    Mock scraper that generates realistic test data.
    Useful for testing the pipeline without making actual HTTP requests.
    """
    
    def __init__(self):
        self.airlines = [
            ("Mock Airlines", "MK"),
            ("Test Airways", "TA"),
            ("Fake Flights", "FF")
        ]
        
    def search_fares(self, origin, destination, departure_date):
        """
        Generates simulated airfare data for the given route and date.
        """
        results = []
        
        # Generate 3-8 mock flights per search
        num_flights = random.randint(3, 8)
        
        for i in range(num_flights):
            airline_name, airline_code = random.choice(self.airlines)
            flight_number = f"{airline_code}{random.randint(100, 999)}"
            
            # Generate random times
            dept_hour = random.randint(5, 22)
            dept_minute = random.choice([0, 15, 30, 45])
            
            # Duration between 1 and 3 hours (60 to 180 mins)
            duration = random.randint(60, 180)
            
            base_fare = random.randint(3000, 8000)
            taxes = int(base_fare * 0.18)
            fees = random.randint(150, 500)
            total_fare = base_fare + taxes + fees
            
            # Calculate mock arrival time (simplified, doesn't cross midnight for this mock)
            dept_time_obj = datetime.strptime(f"{dept_hour:02d}:{dept_minute:02d}", "%H:%M")
            arr_time_obj = dept_time_obj + timedelta(minutes=duration)
            arrival_time_str = arr_time_obj.strftime("%H:%M")
            
            observation = {
                "source": "MockScraper",
                "source_type": "mock",
                "airline": airline_name,
                "flight_number": flight_number,
                "origin": origin,
                "destination": destination,
                "departure_date": departure_date,
                "departure_time": f"{dept_hour:02d}:{dept_minute:02d}",
                "arrival_time": arrival_time_str,
                "duration_minutes": duration,
                "stops": 0,
                "fare_class": random.choice(["Economy", "Premium Economy"]),
                "base_fare": base_fare,
                "taxes": taxes,
                "fees": fees,
                "total_fare": total_fare,
                "currency": "INR",
                "availability": random.randint(1, 15),
                "booking_url": f"https://mockbooking.com/{flight_number}"
            }
            
            results.append(observation)
            
        return results
