class DuplicateDetector:
    """
    Checks for duplicate observations before database insertion to ensure
    data cleanliness while strictly retaining legitimate historical price shifts.
    """
    
    def __init__(self, db_connection):
        self.conn = db_connection
        
    def is_duplicate(self, observation):
        """
        Checks if the exact same observation already exists in fare_observations.
        
        A suitable uniqueness strategy considers:
        source, origin, destination, departure_date, airline, flight_number, cabin_class, total_fare, scraped_at
        """
        if not self.conn:
            return False
            
        cursor = self.conn.cursor()
        
        query = """
            SELECT id FROM fare_observations
            WHERE source = %s 
              AND origin = %s 
              AND destination = %s 
              AND departure_date = %s
              AND airline = %s 
              AND flight_number = %s
              AND cabin_class = %s
              AND total_fare = %s
              AND scraped_at = %s
            LIMIT 1
        """
        
        values = (
            observation.get("source"),
            observation.get("origin"),
            observation.get("destination"),
            observation.get("departure_date"),
            observation.get("airline"),
            observation.get("flight_number"),
            observation.get("cabin_class"),
            observation.get("total_fare"),
            observation.get("scraped_at")
        )
        
        try:
            cursor.execute(query, values)
            result = cursor.fetchone()
            cursor.close()
            return result is not None
        except Exception as e:
            cursor.close()
            return False
