from datetime import datetime
from utils.logger import log_rejection

class DataValidator:
    def __init__(self):
        self.valid_currencies = ['INR', 'USD', 'EUR', 'GBP']

    def validate(self, records, source_name):
        """
        Validates a list of fare observation dictionaries.
        Returns a tuple of (valid_records, rejected_records).
        """
        valid = []
        rejected = []

        for record in records:
            is_valid, reason = self._validate_single_record(record)
            if is_valid:
                valid.append(record)
            else:
                log_rejection(source_name, record, reason)
                rejected.append({
                    "record": record,
                    "reason": reason
                })

        return valid, rejected

    def _validate_single_record(self, record):
        # 1. Price is numeric and greater than zero
        try:
            total_fare = float(record.get('total_fare', 0))
            if total_fare <= 0:
                return False, "Price must be greater than zero"
        except (ValueError, TypeError):
            return False, "Price must be numeric"

        # 2. Currency is valid
        currency = str(record.get('currency', '')).strip().upper()
        if currency not in self.valid_currencies:
            return False, f"Invalid currency: {currency}"

        # 3. Origin and Destination exist
        origin = str(record.get('origin', '')).strip()
        destination = str(record.get('destination', '')).strip()
        if not origin or not destination:
            return False, "Origin and Destination must exist"
        if len(origin) != 3 or len(destination) != 3:
            return False, "Invalid airport codes (must be 3 characters)"

        # 4. Departure date is valid
        dep_date = record.get('departure_date')
        if not dep_date:
            return False, "Departure date must exist"
        try:
            # Assuming it's already a date object or a string in YYYY-MM-DD
            if isinstance(dep_date, str):
                datetime.strptime(dep_date, "%Y-%m-%d")
        except ValueError:
            return False, "Departure date format must be YYYY-MM-DD"

        # 5. Timestamp exists
        if not record.get('scraped_at'):
            return False, "Timestamp (scraped_at) must exist"

        # 6. Airline is valid when available (basic check)
        airline = record.get('airline')
        if airline is not None and not str(airline).strip():
            return False, "Airline name cannot be empty if provided"

        return True, "Valid"
