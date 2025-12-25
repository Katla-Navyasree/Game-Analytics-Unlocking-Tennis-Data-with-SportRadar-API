use tennis_db;

-- COMPETITORS & RANKINGS

-- Get all competitors with their rank and points
SELECT 
    c.name,
    r.rank1,
    r.points
FROM Competitor_Rankings r
JOIN Competitors c
    ON r.competitor_id = c.competitor_id;

-- Find competitors ranked in the Top 5
SELECT 
    c.name,
    r.rank1,
    r.points
FROM Competitor_Rankings r
JOIN Competitors c
    ON r.competitor_id = c.competitor_id
WHERE r.rank1 <= 5
ORDER BY r.rank1;

-- List competitors with no rank movement (stable rank)
SELECT 
    c.name,
    r.rank1,
    r.movement
FROM Competitor_Rankings r
JOIN Competitors c
    ON r.competitor_id = c.competitor_id
WHERE r.movement = 0;

-- Get the total points of competitors from a specific country (e.g., Croatia)
SELECT 
    c.country,
    SUM(r.points) AS total_points
FROM Competitor_Rankings r
JOIN Competitors c
    ON r.competitor_id = c.competitor_id
WHERE c.country = 'Croatia'
GROUP BY c.country;

-- Count the number of competitors per country
SELECT 
    country,
    COUNT(*) AS total_competitors
FROM Competitors
GROUP BY country;

-- Find competitors with the highest points in the current week
SELECT 
    c.name,
    r.points
FROM Competitor_Rankings r
JOIN Competitors c
    ON r.competitor_id = c.competitor_id
WHERE r.points = (
    SELECT MAX(points)
    FROM Competitor_Rankings
);
