-- Create necessary extensions if not already done
CREATE EXTENSION IF NOT EXISTS ai CASCADE;
CREATE EXTENSION IF NOT EXISTS vectorscale CASCADE;

-- Create the 'cvs' table if it doesn't exist
CREATE TABLE IF NOT EXISTS cvtable (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    fullname TEXT NOT NULL UNIQUE,
    metadata JSONB,
    embedding VECTOR(768)
);

-- Create indexes for efficient similarity search
CREATE INDEX IF NOT EXISTS cvtable_embedding_idx ON cvtable USING diskann (embedding);
