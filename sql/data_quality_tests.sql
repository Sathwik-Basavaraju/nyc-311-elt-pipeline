-- Example data-quality checks for the staged 311 data.
-- These are a HANDFUL of examples only. They are NOT a claim of 40 tests,
-- and they have not been run against production data.
-- Each query should return 0 rows (or 0 failures) on clean data.

-- 1. Uniqueness: no duplicate unique_key values in staging.
SELECT unique_key, COUNT(*) AS n
FROM STG_311
GROUP BY unique_key
HAVING COUNT(*) > 1;

-- 2. Null check: unique_key must never be null.
SELECT COUNT(*) AS null_unique_key_count
FROM STG_311
WHERE unique_key IS NULL;

-- 3. Null check: created_date and complaint_type must never be null.
SELECT COUNT(*) AS null_created_or_complaint_count
FROM STG_311
WHERE created_date IS NULL OR complaint_type IS NULL;

-- 4. Referential / domain integrity: borough must be one of the five NYC boroughs.
SELECT DISTINCT borough
FROM STG_311
WHERE borough NOT IN ('Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island');

-- 5. Referential / domain integrity: status must be a known value.
SELECT DISTINCT status
FROM STG_311
WHERE status NOT IN ('Closed', 'Open', 'In Progress');

-- 6. Logical check: closed_date, when present, must not precede created_date.
SELECT COUNT(*) AS closed_before_created_count
FROM STG_311
WHERE closed_date IS NOT NULL AND closed_date < created_date;
