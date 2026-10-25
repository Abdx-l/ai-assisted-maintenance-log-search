CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE IF NOT EXISTS maintenance(id bigserial PRIMARY KEY,equipment text,occurred date,severity text,body text,embedding vector(384),search tsvector GENERATED ALWAYS AS(to_tsvector('english',body)) STORED);
CREATE INDEX IF NOT EXISTS maintenance_words ON maintenance USING gin(search);
CREATE INDEX IF NOT EXISTS maintenance_vector ON maintenance USING hnsw(embedding vector_cosine_ops);
