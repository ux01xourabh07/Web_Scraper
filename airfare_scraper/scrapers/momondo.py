from .base_scraper import BaseScraper, SourceUnavailableError

class MomondoScraper(BaseScraper):
    def __init__(self):
        super().__init__(source_name="Momondo")

    def scrape(self, route, departure_date):
        raise SourceUnavailableError("Access unavailable")
