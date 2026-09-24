from .base_scraper import BaseScraper, SourceUnavailableError

class ExpediaScraper(BaseScraper):
    def __init__(self):
        super().__init__(source_name="Expedia")

    def scrape(self, route, departure_date):
        raise SourceUnavailableError("Access unavailable (Requires authorized Partner API)")
