BEGIN;

SELECT _v.register_patch('002-create-person', NULL, NULL);

CREATE TABLE person (
    id SERIAL PRIMARY KEY,
    is_active BOOLEAN NOT NULL,
    telegram_uid INTEGER NOT NULL,
    telegram_info JSONB,
    started_ts TIMESTAMPTZ
);

COMMIT;
