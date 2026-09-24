from datetime import datetime

class DataValidator:
    """
    Validates standardized airfare observations before insertion into the database.
    Ensures data integrity and quality.
    """
    
    def __init__(self):
        # In a real scenario, this could be loaded from config/airports.json
        # For now, we will do basic structural validation
        pass

    @staticmethod
    def validate(observation):
        """
        Validates a single observation.
        
        Args:
            observation (dict): The standardized airfare observation.
            
        Returns:
            tuple: (is_valid (bool), error_message (str))
        """
        required_fields = [
            "source", "airline", "flight_number", "origin", "destination", 
            "departure_date", "total_fare", "scraped_at"
        ]
        
        # Check required fields
        for field in required_fields:
            if observation.get(field) is None:
                return False, f"Missing required field: {field}"
                
        # Origin and Destination must not be the same
        if observation["origin"] == observation["destination"]:
            return False, "Origin and Destination cannot be the same"
            
        # Fare must be >= 0
        try:
            if float(observation["total_fare"]) < 0:
                return False, "Total fare cannot be negative"
        except ValueError:
            return False, "Total fare must be a numeric value"
            
        # Validate date format (YYYY-MM-DD)
        try:
            datetime.strptime(observation["departure_date"], "%Y-%m-%d")
        except ValueError:
            return False, "Invalid departure_date format. Expected YYYY-MM-DD"
            
        # Validate scraped_at timestamp
        if not isinstance(observation["scraped_at"], datetime):
            return False, "scraped_at must be a valid datetime object"
            
        # Validate duration if present
        duration = observation.get("duration_minutes")
        if duration is not None:
            if not isinstance(duration, (int, float)) or duration <= 0 or duration > 3000:
                return False, "Duration minutes must be a positive reasonable number"
                
        # Currency check
        if observation.get("currency") not in ["INR", "USD", "EUR", "GBP"]: # Extend as needed
            return False, "Invalid currency"

        return True, "Valid"
