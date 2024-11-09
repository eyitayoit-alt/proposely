-- Create necessary extensions if not already done
CREATE EXTENSION IF NOT EXISTS ai CASCADE;
CREATE EXTENSION IF NOT EXISTS vectorscale CASCADE;

-- Create table to store CV content and embeddings
CREATE TABLE IF NOT EXISTS cvs (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    fullname TEXT NOT NULL UNIQUE,
    metadata JSONB,
    embedding VECTOR(768) 

);


-- Create indexes for efficient similarity search
CREATE INDEX cvs_embedding_idx ON cvs USING diskann (embedding);

