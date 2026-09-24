from abc import ABC, abstractmethod
from pipeline.normalizer import DataNormalizer
from pipeline.validator import DataValidator

class SourceUnavailableError(Exception):
    """Raised when a data source cannot be accessed through permitted methods."""
    pass

class BaseScraper(ABC):
    """
    Common interface for all source connectors in the Airfare Price Index scraper.
    """
    def __init__(self, source_name="Base"):
        self.source_name = source_name
        self._normalizer = DataNormalizer()
        self._validator = DataValidator()

    @abstractmethod
    def scrape(self, route, departure_date):
        """
        Extract raw data from the target travel site for the given route and date.
        If the website cannot be accessed through a permitted method,
        raise SourceUnavailableError.
        """
        pass

    def normalize(self, data):
        """
        Default normalization using DataNormalizer.
        """
        return self._normalizer.normalize(data)

    def validate(self, data):
        """
        Default validation using DataValidator.
        Returns (valid_records, rejected_records).
        """
        return self._validator.validate(data, self.source_name)
