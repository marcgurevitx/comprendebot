import os
import types

config = types.SimpleNamespace(**os.environ)


def to_int(cfg_name):
    setattr(
        config,
        cfg_name,
        int(getattr(config, cfg_name)),
    )


def to_float(cfg_name):
    setattr(
        config,
        cfg_name,
        float(getattr(config, cfg_name)),
    )


def calc_ratios(chances):
    return [c/sum(chances, start=1) for c in chances]


to_float("CMPDBOT_SIMILARITY_RATIO")
to_int("CMPDBOT_CHALLENGE_SEVRAL_TIMEZ")
to_int("CMPDBOT_CHALLENGE_CHANCE_PHRASE")
to_int("CMPDBOT_CHALLENGE_CHANCE_VOICE")
to_int("CMPDBOT_CHALLENGE_CHANCE_TRANSCRIPTION")
to_int("CMPDBOT_CHALLENGE_MIN_XP_PHRASE")
to_int("CMPDBOT_CHALLENGE_MIN_XP_VOICE")
to_int("CMPDBOT_CHALLENGE_SAMPLE_PHRASE")
to_int("CMPDBOT_CHALLENGE_SAMPLE_VOICE")
to_int("CMPDBOT_CHALLENGE_SUCCESS_BOOST")
to_float("CMPDBOT_CHALLENGE_BELOW_GOLD")
to_float("CMPDBOT_CHALLENGE_BELOW_SILVER")

(
    config.RATIO_PHRASE,
    config.RATIO_VOICE,
    config.RATIO_TRANSCRIPTION,
) = calc_ratios([
    config.CMPDBOT_CHALLENGE_CHANCE_PHRASE,
    config.CMPDBOT_CHALLENGE_CHANCE_VOICE,
    config.CMPDBOT_CHALLENGE_CHANCE_TRANSCRIPTION,
])

config.S3_URL = f"http://{config.S3_HOST}:{config.S3_PORT}"
