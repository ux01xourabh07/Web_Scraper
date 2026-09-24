def parse_flight_number(raw_flight_str):
    """
    Extracts and standardizes flight numbers.
    e.g., 'IndiGo 6E-123' -> '6E123'
    """
    if not raw_flight_str:
        return None
        
    # Remove spaces and hyphens
    cleaned = str(raw_flight_str).replace(" ", "").replace("-", "")
    return cleaned.upper()
