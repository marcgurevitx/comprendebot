BEGIN;

SELECT _v.register_patch('002-create-person', NULL, NULL);

CREATE TABLE person (
    id serial PRIMARY KEY,
    is_active boolean NOT NULL,
    telegram_uid integer NOT NULL,
    telegram_info jsonb,
    started_ts timestamptz
);

COMMIT;
