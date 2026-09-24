import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Central configuration manager for the airfare scraper.
    """
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "airfare_index")
    
    SCRAPER_INTERVAL_MINUTES = int(os.getenv("SCRAPER_INTERVAL", 30))
    
    CONFIG_DIR = os.path.join(os.path.dirname(__file__), 'config')
    ROUTES_FILE = os.path.join(CONFIG_DIR, 'routes.json')
    AIRPORTS_FILE = os.path.join(CONFIG_DIR, 'airports.json')
    AIRLINES_FILE = os.path.join(CONFIG_DIR, 'airlines.json')
