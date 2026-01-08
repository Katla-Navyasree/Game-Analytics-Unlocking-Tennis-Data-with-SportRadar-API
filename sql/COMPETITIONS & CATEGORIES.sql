use tennis_db;

-- COMPETITIONS & CATEGORIES

-- 1. List all competitions along with their category name
SELECT 
    c.competition_name,
    cat.category_name
FROM Competitions c
JOIN Categories cat
    ON c.category_id = cat.category_id;

-- 2.  Count the number of competitions in each category
SELECT 
    cat.category_name,
    COUNT(c.competition_id) AS total_competitions
FROM Categories cat
LEFT JOIN Competitions c
    ON cat.category_id = c.category_id
GROUP BY cat.category_name;

-- 3. Find all competitions of type 'doubles'
SELECT *
FROM Competitions
WHERE type = 'doubles';

-- 4. Get competitions that belong to a specific category 
SELECT 
    c.competition_name
FROM Competitions c
JOIN Categories cat
    ON c.category_id = cat.category_id
WHERE cat.category_name = 'ITF Men';

-- 5. Identify parent competitions and their sub-competitions
SELECT 
    parent.competition_name AS parent_competition,
    child.competition_name AS sub_competition
FROM Competitions child
JOIN Competitions parent
    ON child.parent_id = parent.competition_id;
    
-- 5. Analyze the distribution of competition types by category
SELECT 
    cat.category_name,
    c.type,
    COUNT(*) AS total
FROM Competitions c
JOIN Categories cat
    ON c.category_id = cat.category_id
GROUP BY cat.category_name, c.type
ORDER BY cat.category_name;

-- 6.  List all competitions with no parent (top-level competitions)
SELECT 
    competition_name
FROM Competitions
WHERE parent_id IS NULL;





