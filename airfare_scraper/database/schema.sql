CREATE DATABASE IF NOT EXISTS airfare_index;
USE airfare_index;

-- 1. Sources
CREATE TABLE IF NOT EXISTS sources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    url VARCHAR(255),
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Airlines
CREATE TABLE IF NOT EXISTS airlines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    iata_code VARCHAR(10),
    active BOOLEAN DEFAULT TRUE
);

-- 3. Airports
CREATE TABLE IF NOT EXISTS airports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    airport_code VARCHAR(10) UNIQUE NOT NULL,
    airport_name VARCHAR(150),
    city VARCHAR(100),
    state VARCHAR(100)
);

-- 4. Routes
CREATE TABLE IF NOT EXISTS routes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    origin VARCHAR(10) NOT NULL,
    destination VARCHAR(10) NOT NULL,
    active BOOLEAN DEFAULT TRUE
);

-- 5. Flights
CREATE TABLE IF NOT EXISTS flights (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    airline VARCHAR(100),
    flight_number VARCHAR(50),
    origin VARCHAR(10) NOT NULL,
    destination VARCHAR(10) NOT NULL,
    departure_time TIME,
    arrival_time TIME,
    duration_minutes INT,
    stops INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Fare Observations
CREATE TABLE IF NOT EXISTS fare_observations (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    source VARCHAR(100) NOT NULL,
    origin VARCHAR(10) NOT NULL,
    destination VARCHAR(10) NOT NULL,
    departure_date DATE NOT NULL,
    return_date DATE,
    trip_type VARCHAR(20),
    airline VARCHAR(100),
    flight_number VARCHAR(50),
    departure_time TIME,
    arrival_time TIME,
    duration_minutes INT,
    stops INT,
    cabin_class VARCHAR(50),
    fare_class VARCHAR(50),
    base_fare DECIMAL(10,2),
    taxes DECIMAL(10,2),
    total_fare DECIMAL(10,2),
    currency VARCHAR(10) DEFAULT 'INR',
    availability INT,
    scraped_at DATETIME NOT NULL
);

-- 7. Scrape Runs
CREATE TABLE IF NOT EXISTS scrape_runs (
    run_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    source VARCHAR(100),
    started_at DATETIME,
    completed_at DATETIME,
    status VARCHAR(30),
    records_found INT DEFAULT 0,
    records_inserted INT DEFAULT 0,
    records_rejected INT DEFAULT 0,
    error_message TEXT
);

-- 8. Index Values
CREATE TABLE IF NOT EXISTS index_values (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    index_type VARCHAR(50) NOT NULL, -- e.g., 'ROUTE', 'AIRLINE', 'NATIONAL', 'SEASONAL'
    reference_id VARCHAR(100), -- e.g., 'DEL-BOM', '6E'
    calculation_date DATE NOT NULL,
    index_value DECIMAL(10,2) NOT NULL,
    observation_count INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
