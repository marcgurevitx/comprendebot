import os
import types

config = types.SimpleNamespace(**os.environ)

config.CMPDBOT_SIMILARITY_RATIO = float(config.CMPDBOT_SIMILARITY_RATIO)
