BEGIN;

SELECT _v.register_patch('006-insert-dummy', NULL, NULL);

-- goodenough has a bug when selection is empty :(

INSERT INTO phrase (is_active, created_ts, original_text)
VALUES
    (true, CURRENT_TIMESTAMP, '')
;

INSERT INTO voice (is_active, created_ts, length)
VALUES
    (true, CURRENT_TIMESTAMP, 0)
;

COMMIT;
