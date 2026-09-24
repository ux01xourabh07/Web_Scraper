from .base_scraper import BaseScraper, SourceUnavailableError

class CheapOairScraper(BaseScraper):
    def __init__(self):
        super().__init__(source_name="CheapOair")

    def scrape(self, route, departure_date):
        raise SourceUnavailableError("Access unavailable")
