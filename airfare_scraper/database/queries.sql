-- Average fare by route
SELECT
    origin,
    destination,
    AVG(total_fare) AS average_fare
FROM airfare_observations
GROUP BY origin, destination;

-- Airline pricing
SELECT
    airline,
    AVG(total_fare) AS average_fare
FROM airfare_observations
GROUP BY airline;

-- Price history
SELECT
    scraped_at,
    total_fare
FROM airfare_observations
WHERE origin = 'DEL'
AND destination = 'BOM'
ORDER BY scraped_at;

-- Price spike detection (Example query: showing observations where fare is > 20% higher than route average)
SELECT
    o.scraped_at,
    o.airline,
    o.flight_number,
    o.origin,
    o.destination,
    o.total_fare,
    a.average_fare
FROM airfare_observations o
JOIN (
    SELECT origin, destination, AVG(total_fare) AS average_fare
    FROM airfare_observations
    GROUP BY origin, destination
) a ON o.origin = a.origin AND o.destination = a.destination
WHERE o.total_fare > (1.2 * a.average_fare)
ORDER BY o.scraped_at DESC;
