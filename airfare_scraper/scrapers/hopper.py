from .base_scraper import BaseScraper, SourceUnavailableError

class HopperScraper(BaseScraper):
    def __init__(self):
        super().__init__(source_name="Hopper")

    def scrape(self, route, departure_date):
        raise SourceUnavailableError("Access unavailable (Requires mobile API auth)")
