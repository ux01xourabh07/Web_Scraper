import re

def parse_fare(fare_string):
    """
    Parses a fare string and returns a numeric float value.
    Handles currency symbols, commas, and spaces.
    
    Examples:
        '₹5,499' -> 5499.00
        '₹ 5,499' -> 5499.00
        'INR 5499' -> 5499.00
        '5,499 INR' -> 5499.00
        
    Args:
        fare_string (str): The raw fare string from a scraper.
        
    Returns:
        float: The parsed numeric fare, or None if parsing fails.
    """
    if fare_string is None:
        return None
        
    if isinstance(fare_string, (int, float)):
        return float(fare_string)
        
    # Convert to string in case it's a different type
    fare_str = str(fare_string)
    
    # Remove everything except digits and decimal point
    cleaned_str = re.sub(r'[^\d.]', '', fare_str)
    
    try:
        if cleaned_str:
            return float(cleaned_str)
        return None
    except ValueError:
        return None
