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


to_float("CMPDBOT_SIMILARITY_RATIO")
to_int("CMPDBOT_PHRASE_CHALLENGE_MIN_XP")
