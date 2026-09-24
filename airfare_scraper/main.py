import os
import sys

# Ensure Python can find our modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from scheduler.scheduler import AirfareScheduler

def main():
    print("Initializing Airfare Web Scraping System...")
    
    # Initialize the scheduler with a 30-minute interval as specified
    scheduler = AirfareScheduler(interval_minutes=30)
    
    try:
        # Start the scheduling loop
        scheduler.start()
    except KeyboardInterrupt:
        print("\nScraper stopped by user.")
    except Exception as e:
        print(f"\nScraper encountered a fatal error: {e}")

if __name__ == "__main__":
    main()
