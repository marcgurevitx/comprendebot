BEGIN;

SELECT _v.register_patch('007-link-source-challenge', NULL, NULL);

ALTER TABLE phrase
ADD COLUMN challenge_id integer REFERENCES challenge(id)
;

ALTER TABLE voice
ADD COLUMN challenge_id integer REFERENCES challenge(id)
;

ALTER TABLE transcription
ADD COLUMN challenge_id integer REFERENCES challenge(id)
;

COMMIT;
