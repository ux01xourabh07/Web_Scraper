from parsers.fare_parser import parse_fare

class FareNormalizer:
    """
    Standardizes fare components (base fare, taxes, fees, total fare).
    Ensures that missing values are represented correctly and that
    all values are numeric.
    """
    
    @staticmethod
    def normalize_observation(observation):
        """
        Normalizes the fare fields in an airfare observation dictionary.
        
        Args:
            observation (dict): A raw observation dictionary.
            
        Returns:
            dict: The observation with standardized fare components.
        """
        # Create a copy to avoid mutating the original unnecessarily
        normalized = observation.copy()
        
        # Parse total fare (required)
        total_fare_raw = normalized.get("total_fare")
        normalized["total_fare"] = parse_fare(total_fare_raw)
        
        # Parse optional fare components
        normalized["base_fare"] = parse_fare(normalized.get("base_fare"))
        normalized["taxes"] = parse_fare(normalized.get("taxes"))
        normalized["fees"] = parse_fare(normalized.get("fees"))
        
        # Ensure currency is set (default to INR if missing)
        if not normalized.get("currency") or str(normalized.get("currency")).strip() == "":
            normalized["currency"] = "INR"
            
        # Ensure lead time is calculated if we have scraped_at and departure_date
        # (Usually done during validation or just before DB insertion, but good to have here)
        
        return normalized
