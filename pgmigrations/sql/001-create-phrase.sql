BEGIN;

SELECT _v.register_patch('001-create-phrase', NULL, NULL);

CREATE TABLE phrase (
    id serial PRIMARY KEY,
    is_active boolean NOT NULL,
    original_text text NOT NULL,
    normalized_text text
);

COMMIT;
