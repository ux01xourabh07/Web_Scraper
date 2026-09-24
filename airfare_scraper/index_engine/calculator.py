import os
from datetime import datetime
from database.connection import DatabaseConnection

class AirfareIndexEngine:
    """
    Calculates Price Indices using actual stored observations from MySQL.
    Strictly isolated from scraping logic.
    """
    def __init__(self, db_conn=None):
        self.db = db_conn or DatabaseConnection()

    def calculate_route_index(self, calculation_date=None):
        """Calculates average fare and index by Route."""
        conn = self.db.get_connection()
        if not conn:
            return
        
        calc_date = calculation_date or datetime.now().strftime("%Y-%m-%d")
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT CONCAT(origin, '-', destination) as route_key,
                   AVG(total_fare) as avg_fare,
                   COUNT(id) as obs_count
            FROM fare_observations
            WHERE total_fare > 0
            GROUP BY origin, destination
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        insert_query = """
            INSERT INTO index_values (index_type, reference_id, calculation_date, index_value, observation_count)
            VALUES (%s, %s, %s, %s, %s)
        """
        for r in rows:
            cursor.execute(insert_query, ("ROUTE", r["route_key"], calc_date, r["avg_fare"], r["obs_count"]))
        
        conn.commit()
        cursor.close()
        print(f"Calculated Route Index for {len(rows)} routes.")

    def calculate_airline_index(self, calculation_date=None):
        """Calculates index by Airline."""
        conn = self.db.get_connection()
        if not conn:
            return
            
        calc_date = calculation_date or datetime.now().strftime("%Y-%m-%d")
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT airline, AVG(total_fare) as avg_fare, COUNT(id) as obs_count
            FROM fare_observations
            WHERE total_fare > 0 AND airline IS NOT NULL
            GROUP BY airline
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        insert_query = """
            INSERT INTO index_values (index_type, reference_id, calculation_date, index_value, observation_count)
            VALUES (%s, %s, %s, %s, %s)
        """
        for r in rows:
            cursor.execute(insert_query, ("AIRLINE", r["airline"], calc_date, r["avg_fare"], r["obs_count"]))
            
        conn.commit()
        cursor.close()
        print(f"Calculated Airline Index for {len(rows)} airlines.")

    def calculate_national_index(self, calculation_date=None):
        """Calculates the overall National Airfare Price Index."""
        conn = self.db.get_connection()
        if not conn:
            return
            
        calc_date = calculation_date or datetime.now().strftime("%Y-%m-%d")
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT AVG(total_fare) as avg_fare, COUNT(id) as obs_count
            FROM fare_observations
            WHERE total_fare > 0
        """
        cursor.execute(query)
        row = cursor.fetchone()
        
        if row and row["avg_fare"]:
            insert_query = """
                INSERT INTO index_values (index_type, reference_id, calculation_date, index_value, observation_count)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, ("NATIONAL", "ALL_INDIA", calc_date, row["avg_fare"], row["obs_count"]))
            conn.commit()
            print(f"Calculated National Index: {row['avg_fare']:.2f}")

        cursor.close()
