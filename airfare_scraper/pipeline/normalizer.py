import re
from datetime import datetime

class DataNormalizer:
    def __init__(self):
        # Maps common city/airport names to standard IATA codes
        self.airport_map = {
            'delhi': 'DEL',
            'mumbai': 'BOM',
            'bangalore': 'BLR',
            'bengaluru': 'BLR',
            'goa': 'GOI',
            'hyderabad': 'HYD',
            'kolkata': 'CCU'
        }
        
        # Maps variations to standard Airline names
        self.airline_map = {
            'indigo': 'IndiGo',
            'air india': 'Air India',
            'airindia': 'Air India',
            'spicejet': 'SpiceJet',
            'vistara': 'Vistara',
            'akasa': 'Akasa Air',
            'akasa air': 'Akasa Air',
            'air asia': 'Air India Express',  # Merged entity representation
            'airindia express': 'Air India Express'
        }

    def normalize(self, records):
        """
        Takes a list of raw dictionaries and normalizes their fields.
        Returns a list of normalized dictionaries.
        """
        normalized = []
        for record in records:
            norm_rec = self._normalize_single_record(record)
            normalized.append(norm_rec)
        return normalized

    def _normalize_single_record(self, record):
        norm = record.copy()
        
        # 1. Normalize Airport Codes
        if 'origin' in norm and norm['origin']:
            val = str(norm['origin']).strip().lower()
            norm['origin'] = self.airport_map.get(val, val.upper())
            
        if 'destination' in norm and norm['destination']:
            val = str(norm['destination']).strip().lower()
            norm['destination'] = self.airport_map.get(val, val.upper())

        # 2. Normalize Airline Names
        if 'airline' in norm and norm['airline']:
            val = str(norm['airline']).strip().lower()
            norm['airline'] = self.airline_map.get(val, norm['airline'].strip().title())

        # 3. Normalize Currency
        if 'currency' in norm and norm['currency']:
            val = str(norm['currency']).strip().upper()
            if val in ['₹', 'RS', 'INR']:
                norm['currency'] = 'INR'
            elif val in ['$', 'USD']:
                norm['currency'] = 'USD'
            else:
                norm['currency'] = val
        else:
            norm['currency'] = 'INR'  # default

        # 4. Normalize Fare Values (extract numeric from strings like "₹5,499")
        for fare_field in ['base_fare', 'taxes', 'total_fare']:
            if fare_field in norm and norm[fare_field] is not None:
                val = str(norm[fare_field])
                # Remove currency symbols and commas
                clean_val = re.sub(r'[^\d.]', '', val)
                try:
                    norm[fare_field] = float(clean_val) if clean_val else None
                except ValueError:
                    norm[fare_field] = None

        # 5. Normalize Timestamps to ISO 8601
        if 'scraped_at' in norm and norm['scraped_at']:
            if isinstance(norm['scraped_at'], datetime):
                norm['scraped_at'] = norm['scraped_at'].isoformat()
            # If it's already a string, we assume the scraper formatted it or we could attempt to parse it here
            
        # 6. Normalize Flight Duration
        if 'duration_minutes' in norm and isinstance(norm['duration_minutes'], str):
            val = norm['duration_minutes'].lower()
            # Parse strings like "2h 30m"
            hours = 0
            minutes = 0
            h_match = re.search(r'(\d+)h', val)
            m_match = re.search(r'(\d+)m', val)
            if h_match: hours = int(h_match.group(1))
            if m_match: minutes = int(m_match.group(1))
            
            if hours or minutes:
                norm['duration_minutes'] = (hours * 60) + minutes
            else:
                try:
                    norm['duration_minutes'] = int(val)
                except ValueError:
                    norm['duration_minutes'] = None

        return norm
