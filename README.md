# Web Scraper - Airfare Price Index

Developed for **Smart India Hackathon 2026**.
**Problem Statement ID:** 26056 - Real-Time Airfare Price Index for India
**Team:** Cosmic Six

## ✈️ Overview
This repository contains an automated, scheduled data pipeline designed to collect permitted airfare data from airline and Online Travel Aggregator (OTA) websites. The purpose of this system is to build a reliable dataset for the **Airfare Price Index**. It is strictly a data-gathering tool and NOT a flight booking application.

The pipeline is capable of:
1. **Scraping**: Extracting raw data from target travel sites.
2. **Cleaning & Normalizing**: Parsing diverse currency strings and normalizing fare classes.
3. **Validating**: Ensuring required fields are present and data is logical (e.g., positive fare values, valid dates).
4. **Deduplicating**: Discarding identical consecutive observations while strictly retaining legitimate historical price shifts.
5. **Storing**: Persisting timestamped data into a robust MySQL database for subsequent index generation and analytical queries.

---

## 🛠️ Technology Stack
- **Language**: Python 3.12+
- **Database**: MySQL 8+
- **Libraries**:
  - `requests` & `beautifulsoup4` (For HTML parsing)
  - `pandas` (For data manipulation, if required in analysis)
  - `mysql-connector-python` (For MySQL connectivity)
  - `python-dotenv` (For environment variable management)
  - `schedule` (For the pipeline automation schedule)

*(Note: Docker, MongoDB, Postgres, and Node.js frameworks are explicitly avoided per project constraints).*

---

## ⚙️ How It Works (The Pipeline)

The system is orchestrated by `airfare_scraper/scheduler/scheduler.py` which runs continuously.

1. **Load Active Routes**: The scheduler reads `airfare_scraper/config/routes.json` to find which origin-destination pairs to scrape.
2. **Run Scrapers**: The system invokes scrapers to gather flight pricing for target dates.
3. **Clean Data**: `airfare_scraper/processors/cleaner.py` strips whitespace and cleans raw text.
4. **Standardize Fare**: `airfare_scraper/processors/normalizer.py` and `airfare_scraper/parsers/fare_parser.py` convert various currency formats into standardized numeric floats.
5. **Validate**: `airfare_scraper/processors/validator.py` ensures the integrity of the data.
6. **Check Duplicates**: `airfare_scraper/processors/deduplicator.py` queries the MySQL database to skip identical consecutive insertions.
7. **Timestamp & Insert**: Every valid, unique observation is stamped and inserted into the `airfare_observations` MySQL table.

---

## 🚀 How to Run the Project locally

### Step 1: Database Setup
1. Ensure you have **MySQL 8+** installed and running on your machine.
2. Open your MySQL command-line tool (or a GUI like MySQL Workbench).
3. Execute the schema file to create the database and tables:
   ```bash
   cd airfare_scraper
   mysql -u root -p < sql/schema.sql
   ```
*(Alternatively, you can copy the contents of `airfare_scraper/sql/schema.sql` and run it manually in your SQL client).*

### Step 2: Configure Environment Variables
1. Navigate to the scraper directory and rename the `.env.example` file to `.env`:
   ```bash
   cd airfare_scraper
   copy .env.example .env
   ```
2. Open the `.env` file and enter your MySQL database credentials:
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_actual_mysql_password
   DB_NAME=airfare_index
   ```

### Step 3: Install Dependencies
Open a terminal in the `airfare_scraper` directory and install the required Python libraries:
```bash
cd airfare_scraper
pip install -r requirements.txt
```

### Step 4: Start the Scraper Pipeline
Run the main entry script to start the scheduler:
```bash
python main.py
```
*The system will immediately run its first scrape (to generate data) and will then sleep, running automatically every 30 minutes. You can stop it at any time by pressing `Ctrl+C`.*

---

## 📊 Analytics & Queries
Once data begins populating, you can use the SQL queries provided in `airfare_scraper/sql/queries.sql` to generate insights in your database dashboards, such as:
- Average historical fare by route.
- Price spike detection comparing current observations to route averages.
- Airline pricing comparisons.
