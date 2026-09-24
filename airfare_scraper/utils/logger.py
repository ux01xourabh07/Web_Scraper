import logging
import os
from datetime import datetime

# Ensure logs directory exists
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

def setup_logger(name, log_file, level=logging.INFO):
    """Function to setup as many loggers as you want"""
    
    formatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent adding multiple handlers if logger already exists
    if not logger.handlers:
        logger.addHandler(handler)

    return logger

# Create the two specific loggers requested
scraper_logger = setup_logger('scraper_logger', os.path.join(LOGS_DIR, 'scraper.log'))
error_logger = setup_logger('error_logger', os.path.join(LOGS_DIR, 'errors.log'))

def log_scrape_success(source, records_count, duration):
    """Format: 2026-09-24 12:30:01 SOURCE=Google Flights STATUS=SUCCESS RECORDS=42 DURATION=14.8s"""
    scraper_logger.info(f"SOURCE={source} STATUS=SUCCESS RECORDS={records_count} DURATION={duration}s")

def log_scrape_failure(source, error_message):
    """Format: 2026-09-24 12:30:20 SOURCE=Kayak STATUS=FAILED ERROR=Access unavailable"""
    scraper_logger.info(f"SOURCE={source} STATUS=FAILED ERROR={error_message}")
    error_logger.error(f"SOURCE={source} STATUS=FAILED ERROR={error_message}")

def log_rejection(source, record, reason):
    """Log rejected records during validation."""
    error_logger.warning(f"REJECTED SOURCE={source} REASON={reason} RECORD={record}")
