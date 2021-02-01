BEGIN;

SELECT _v.register_patch('001-create-person', NULL, NULL);

CREATE TABLE person (
    id serial PRIMARY KEY,
    is_active boolean NOT NULL,
    created_ts timestamptz NOT NULL,
    telegram_uid integer NOT NULL,
    telegram_info jsonb,
    xp integer DEFAULT 0,
    n_phrases integer DEFAULT 0,
    n_voices integer DEFAULT 0,
    n_transcriptions integer DEFAULT 0,
    n_prev_success integer DEFAULT 0
);

COMMIT;
