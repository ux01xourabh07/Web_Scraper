CREATE DATABASE IF NOT EXISTS airfare_index;
USE airfare_index;

-- 1. Airlines
CREATE TABLE airlines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    iata_code VARCHAR(10),
    active BOOLEAN DEFAULT TRUE
);

-- 2. Airports
CREATE TABLE airports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    airport_code VARCHAR(10) UNIQUE NOT NULL,
    airport_name VARCHAR(150),
    city VARCHAR(100),
    state VARCHAR(100)
);

-- 3. Routes
CREATE TABLE routes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    origin VARCHAR(10) NOT NULL,
    destination VARCHAR(10) NOT NULL,
    active BOOLEAN DEFAULT TRUE
);

-- 4. Airfare Observations
CREATE TABLE airfare_observations (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    source VARCHAR(100) NOT NULL,
    source_type VARCHAR(20),
    airline VARCHAR(100),
    flight_number VARCHAR(50),
    origin VARCHAR(10) NOT NULL,
    destination VARCHAR(10) NOT NULL,
    departure_date DATE NOT NULL,
    departure_time TIME,
    arrival_time TIME,
    duration_minutes INT,
    stops INT,
    fare_class VARCHAR(50),
    base_fare DECIMAL(10,2),
    taxes DECIMAL(10,2),
    fees DECIMAL(10,2),
    total_fare DECIMAL(10,2),
    currency VARCHAR(10) DEFAULT 'INR',
    availability INT,
    lead_time_days INT,
    booking_url TEXT,
    scraped_at DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Scrape Logs
CREATE TABLE scrape_logs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    source VARCHAR(100),
    origin VARCHAR(10),
    destination VARCHAR(10),
    scrape_started DATETIME,
    scrape_finished DATETIME,
    records_found INT DEFAULT 0,
    records_saved INT DEFAULT 0,
    records_duplicate INT DEFAULT 0,
    records_invalid INT DEFAULT 0,
    status VARCHAR(30),
    error_message TEXT
);
