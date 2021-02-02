BEGIN;

SELECT _v.register_patch('004-create-transcription', NULL, NULL);

CREATE TABLE transcription (
    id serial PRIMARY KEY,
    is_active boolean NOT NULL,
    created_ts timestamptz NOT NULL,
    person_id integer REFERENCES person(id),
    voice_id integer REFERENCES voice(id)
);

COMMIT;
