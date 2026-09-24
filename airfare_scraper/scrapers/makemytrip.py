from .base_scraper import BaseScraper, SourceUnavailableError

class MakeMyTripScraper(BaseScraper):
    def __init__(self):
        super().__init__(source_name="MakeMyTrip")

    def scrape(self, route, departure_date):
        raise SourceUnavailableError("Access unavailable (Bot detection / Cloudflare protection)")
