BEGIN;

SELECT _v.register_patch('001-create-phrase', NULL, NULL);

CREATE TABLE phrase (
    id SERIAL PRIMARY KEY,
    is_active BOOLEAN NOT NULL,
    original_text TEXT NOT NULL,
    normalized_text TEXT
);

COMMIT;
