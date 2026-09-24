from datetime import datetime

class DataRepository:
    def __init__(self, db_conn):
        self.db = db_conn

    def record_scrape_run(self, source, started_at, completed_at, status, records_found, records_inserted, records_rejected, error_message=None):
        query = """
            INSERT INTO scrape_runs (
                source, started_at, completed_at, status,
                records_found, records_inserted, records_rejected, error_message
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            source, started_at, completed_at, status,
            records_found, records_inserted, records_rejected, error_message
        )
        conn = self.db.get_connection()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                cursor.execute(query, params)
                conn.commit()
                run_id = cursor.lastrowid
                cursor.close()
                return run_id
            except Exception as e:
                conn.rollback()
                cursor.close()
                print(f"Failed to record scrape run: {e}")
        return None

    def insert_fare_observations(self, observations):
        """
        Inserts observations in a single transaction with rollback support.
        """
        if not observations:
            return 0

        query = """
            INSERT INTO fare_observations (
                source, origin, destination, departure_date, return_date,
                trip_type, airline, flight_number, departure_time, arrival_time,
                duration_minutes, stops, cabin_class, fare_class, base_fare,
                taxes, total_fare, currency, availability, scraped_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """
        queries = []
        for obs in observations:
            params = (
                obs.get("source"),
                obs.get("origin"),
                obs.get("destination"),
                obs.get("departure_date"),
                obs.get("return_date"),
                obs.get("trip_type"),
                obs.get("airline"),
                obs.get("flight_number"),
                obs.get("departure_time"),
                obs.get("arrival_time"),
                obs.get("duration_minutes"),
                obs.get("stops"),
                obs.get("cabin_class"),
                obs.get("fare_class"),
                obs.get("base_fare"),
                obs.get("taxes"),
                obs.get("total_fare"),
                obs.get("currency", "INR"),
                obs.get("availability"),
                obs.get("scraped_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            queries.append((query, params))

        success = self.db.execute_transaction(queries)
        return len(queries) if success else 0
