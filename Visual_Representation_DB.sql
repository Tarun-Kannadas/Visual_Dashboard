CREATE TABLE data (
    id SERIAL PRIMARY KEY,
    intensity INTEGER,
    likelihood INTEGER,
    relevance INTEGER,
    year INTEGER,
    country TEXT,
    topics TEXT,
    region TEXT,
    city TEXT
);
