BEGIN;

SELECT _v.register_patch('003-create-challenge', NULL, NULL);

CREATE TYPE challenge_type_code AS ENUM (
    'CHL_PHR',  -- submit a phrase
    'CHL_VOC',  -- send voice message
    'CHL_TRS'  -- transcribe voice message
);

CREATE TABLE challenge (
    id serial PRIMARY KEY,
    is_active boolean NOT NULL,
    type_code challenge_type_code NOT NULL,
    person_id integer REFERENCES person(id) NOT NULL,
    created_ts timestamptz
);

COMMIT;
