BEGIN;

SELECT _v.register_patch('008-create-stat-views', NULL, NULL);


CREATE VIEW recent_person AS
SELECT
    u.id,
    u.telegram_info ->> 'username' as username,
    u.telegram_info ->> 'first_name' as first_name,
    u.telegram_info ->> 'last_name' as last_name,
    u.xp,
    u.generated_xp,
    COUNT(c.id) as ch,
    CASE u.is_active WHEN true THEN '' ELSE 'BLOCKED' END as b,
    CASE WHEN (u.telegram_info -> 'is_bot')::boolean THEN 'BOT' ELSE '' END as bot
FROM
    person u
    LEFT JOIN challenge c
        ON c.person_id = u.id
WHERE
    1 = 1
    AND (
        u.created_ts > NOW() - INTERVAL '48' HOUR
        OR c.created_ts > NOW() - INTERVAL '48' HOUR
    )
GROUP BY
    u.id
ORDER BY
    u.created_ts
;


CREATE VIEW recent_phrase AS
SELECT
    f.id as phrase_id,
    f.original_text,
    CASE f.is_active WHEN true THEN '' ELSE 'BLOCKED' END as b,
    f.person_id,
    CASE u.is_active WHEN true THEN '' ELSE 'USER_BLOCKED' END as ub,
    f.challenge_id
FROM
    phrase f
    JOIN person u
        ON f.person_id = u.id
WHERE
    1 = 1
    AND f.created_ts > NOW() - INTERVAL '48' HOUR
ORDER BY
    u.id,
    f.created_ts
;


CREATE VIEW recent_voice AS
SELECT
    v.id as voice_id,
    f.original_text,
    CASE v.is_active WHEN true THEN '' ELSE 'BLOCKED' END as b,
    v.person_id,
    CASE vu.is_active WHEN true THEN '' ELSE 'USER_BLOCKED' END as ub,
    v.phrase_id,
    CASE f.is_active WHEN true THEN '' ELSE 'F_BLOCKED' END as fb,
    f.person_id as f_person_id,
    CASE (fu.id IS NULL OR fu.is_active) WHEN true THEN '' ELSE 'F_USER_BLOCKED' END as fub,
    v.challenge_id
FROM
    voice v
    JOIN person vu
        ON v.person_id = vu.id
    JOIN phrase f
        ON v.phrase_id = f.id
    LEFT JOIN person fu
        ON f.person_id = fu.id
WHERE
    1 = 1
    AND v.created_ts > NOW() - INTERVAL '48' HOUR
ORDER BY
    vu.id,
    v.created_ts
;


COMMIT;
