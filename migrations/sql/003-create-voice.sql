BEGIN;

SELECT _v.register_patch('003-create-voice', NULL, NULL);

CREATE TABLE voice (
    id serial PRIMARY KEY,
    is_active boolean NOT NULL,
    created_ts timestamptz NOT NULL,
    person_id integer REFERENCES person(id) NOT NULL,
    phrase_id integer REFERENCES phrase(id) NOT NULL
);

COMMIT;
