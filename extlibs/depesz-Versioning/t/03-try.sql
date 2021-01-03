BEGIN;
    -- Disable printing warning messages
    SET client_min_messages = ERROR;

    -- load pgtap - change next line to point to correct path for your system!
    \i t/00-load.sql.inc


    SELECT plan(7);

    SELECT is( ( SELECT count(*) FROM _v.patches ), 0::bigint, 'When running tests _v.patches table should be empty to prevent bad interactions between patches and tests.' );

    SELECT is(
        _v.try_register_patch( 'first_patch' ),
        true,
        'Installation of patch without dependencies and conflicts.'
    );

    SELECT is(
        _v.try_register_patch( 'first_patch' ),
        false,
        'Reinstallation of patch without dependencies and conflicts.'
    );

    SELECT is(
        _v.try_register_patch( 'second_patch', ARRAY['first_patch'] ),
        true,
        'Installation of patch with correct dependency.'
    );

    SELECT is(
        _v.try_register_patch( 'third_patch', ARRAY['bad_patch'] ),
        false,
        'Installation of patch with bad dependency.'
    );

    SELECT is(
        _v.try_register_patch( 'fourth_patch', NULL, ARRAY['bad_patch'] ),
        true,
        'Installation of patch with and correct conflict.'
    );

    SELECT is(
        _v.try_register_patch( 'fifth_patch', NULL, ARRAY['first_patch'] ),
        false,
        'Installation of patch with bad conflict.'
    );

    SELECT * FROM finish();

ROLLBACK;

