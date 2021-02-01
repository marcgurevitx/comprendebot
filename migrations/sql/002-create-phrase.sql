BEGIN;

SELECT _v.register_patch('002-create-phrase', NULL, NULL);

CREATE TABLE phrase (
    id serial PRIMARY KEY,
    is_active boolean NOT NULL,
    created_ts timestamptz NOT NULL,
    person_id integer REFERENCES person(id),
    original_text text NOT NULL,
    normalized_text text
);

COMMIT;
