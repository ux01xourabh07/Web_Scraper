from .base_scraper import BaseScraper, SourceUnavailableError

class KayakScraper(BaseScraper):
    def __init__(self):
        super().__init__(source_name="Kayak")

    def scrape(self, route, departure_date):
        raise SourceUnavailableError("Access unavailable")
