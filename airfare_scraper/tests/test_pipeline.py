import unittest
from datetime import datetime
from pipeline.validator import DataValidator
from pipeline.normalizer import DataNormalizer
from scrapers.base_scraper import SourceUnavailableError
from scrapers.kayak import KayakScraper

class TestAirfarePipeline(unittest.TestCase):
    def setUp(self):
        self.validator = DataValidator()
        self.normalizer = DataNormalizer()

    def test_airport_normalization(self):
        records = [
            {"origin": "Delhi", "destination": "mumbai"},
            {"origin": "bangalore", "destination": "GOA"}
        ]
        norm = self.normalizer.normalize(records)
        self.assertEqual(norm[0]["origin"], "DEL")
        self.assertEqual(norm[0]["destination"], "BOM")
        self.assertEqual(norm[1]["origin"], "BLR")
        self.assertEqual(norm[1]["destination"], "GOI")

    def test_airline_normalization(self):
        records = [
            {"airline": "indigo"},
            {"airline": "air india"},
            {"airline": "akasa air"}
        ]
        norm = self.normalizer.normalize(records)
        self.assertEqual(norm[0]["airline"], "IndiGo")
        self.assertEqual(norm[1]["airline"], "Air India")
        self.assertEqual(norm[2]["airline"], "Akasa Air")

    def test_price_validation_valid(self):
        record = {
            "origin": "DEL",
            "destination": "BOM",
            "departure_date": "2026-10-15",
            "total_fare": 4500.0,
            "currency": "INR",
            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        valid, rejected = self.validator.validate([record], "Test")
        self.assertEqual(len(valid), 1)
        self.assertEqual(len(rejected), 0)

    def test_price_validation_invalid(self):
        # Negative / zero price
        invalid_records = [
            {
                "origin": "DEL",
                "destination": "BOM",
                "departure_date": "2026-10-15",
                "total_fare": -100,
                "currency": "INR",
                "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                "origin": "DEL",
                "destination": "BOM",
                "departure_date": "2026-10-15",
                "total_fare": "invalid_number",
                "currency": "INR",
                "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
        valid, rejected = self.validator.validate(invalid_records, "Test")
        self.assertEqual(len(valid), 0)
        self.assertEqual(len(rejected), 2)

    def test_scraper_failure_handling(self):
        scraper = KayakScraper()
        with self.assertRaises(SourceUnavailableError):
            scraper.scrape({"origin": "DEL", "destination": "BOM"}, "2026-10-15")

if __name__ == "__main__":
    unittest.main()
