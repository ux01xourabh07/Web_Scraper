from .base_scraper import BaseScraper, SourceUnavailableError

class BookingFlightsScraper(BaseScraper):
    def __init__(self):
        super().__init__(source_name="Booking.com Flights")

    def scrape(self, route, departure_date):
        raise SourceUnavailableError("Access unavailable (Bot detection / Captcha present)")
