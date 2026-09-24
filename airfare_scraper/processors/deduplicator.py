class DuplicateDetector:
    """
    Checks for duplicate records before database insertion to ensure
    data cleanliness while retaining legitimate historical price changes.
    """
    
    def __init__(self, db_connection):
        self.conn = db_connection
        
    def is_duplicate(self, observation):
        """
        Checks if the exact same observation already exists in the database.
        Legitimate price changes over time will have a different scraped_at
        and possibly different total_fare, so they are kept.
        
        Args:
            observation (dict): The observation to check.
            
        Returns:
            bool: True if duplicate, False otherwise.
        """
        if not self.conn or not self.conn.is_connected():
            print("Warning: DB connection not available for deduplication check. Assuming not duplicate.")
            return False
            
        cursor = self.conn.cursor()
        
        # We define a duplicate as having the exact same core flight details 
        # AND exactly the same price AT the exact same scrape time.
        # If the price changed, it's a new observation. If it's a new scrape time, it's a new observation.
        
        query = """
            SELECT id FROM airfare_observations
            WHERE source = %s 
              AND airline = %s 
              AND flight_number = %s
              AND origin = %s 
              AND destination = %s 
              AND departure_date = %s
              AND departure_time = %s
              AND fare_class = %s
              AND total_fare = %s
              AND scraped_at = %s
            LIMIT 1
        """
        
        values = (
            observation.get("source"),
            observation.get("airline"),
            observation.get("flight_number"),
            observation.get("origin"),
            observation.get("destination"),
            observation.get("departure_date"),
            observation.get("departure_time"),
            observation.get("fare_class"),
            observation.get("total_fare"),
            observation.get("scraped_at")
        )
        
        try:
            cursor.execute(query, values)
            result = cursor.fetchone()
            cursor.close()
            return result is not None
        except Exception as e:
            print(f"Error checking for duplicate: {e}")
            if cursor:
                cursor.close()
            return False
