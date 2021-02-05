BEGIN;

SELECT _v.register_patch('005-create-challenge', NULL, NULL);

CREATE TYPE challenge_type_code AS ENUM (
    'CHL_PHR',  -- Submit a phrase
    'CHL_VOC',  -- Send voice message
    'CHL_TRS'   -- Transcribe voice message
);

CREATE TYPE challenge_state_code AS ENUM (
    'PHR_CRE',
    'PHR_WRK',
    'PHR_END',

    'VOC_CRE',
    'VOC_WRK',
    'VOC_END',

    'TRS_CRE',
    'TRS_WRK',
    'TRS_END'
);

CREATE TABLE challenge (
    id serial PRIMARY KEY,
    is_active boolean NOT NULL,
    created_ts timestamptz NOT NULL,
    person_id integer REFERENCES person(id) NOT NULL,
    type_code challenge_type_code NOT NULL,
    phrases integer ARRAY,
    voices integer ARRAY,
    state_code challenge_state_code,
    executor_data jsonb DEFAULT '{}'
);

COMMIT;
