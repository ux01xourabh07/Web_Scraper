class DataCleaner:
    """
    Cleans raw data strings (e.g., stripping whitespace, handling special characters)
    before they reach the normalizer.
    """
    
    @staticmethod
    def clean_text(text):
        if not text:
            return None
        return str(text).strip()
        
    @staticmethod
    def clean_observation(observation):
        cleaned = observation.copy()
        
        # Clean text fields
        for field in ["source", "airline", "fare_class"]:
            if field in cleaned and cleaned[field]:
                cleaned[field] = DataCleaner.clean_text(cleaned[field])
                
        return cleaned
