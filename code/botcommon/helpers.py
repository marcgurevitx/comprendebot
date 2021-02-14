from Levenshtein import distance

from botcommon.bottypes import Button, Stickers
from botcommon.config import config
from botcommon.language import Language


def normalize_text(text):
    language = Language.get_instance()
    normalized_text = language.normalize_text(text)
    return normalized_text


def get_distance(user_text, normalized_text):
    return distance(normalize_text(user_text), normalized_text)


def get_start_button():
    return Button(
        text=_("Start new challenge  // button"),
        data=config.CMPDBOT_CONST_START,
    )


def get_metal_sticker(length, distance):
    similarity = 1.0 - distance / length
    if similarity < config.CMPDBOT_BELOW_BRONZE:
        rv = Stickers.PAPER
    elif similarity < config.CMPDBOT_BELOW_SILVER:
        rv = Stickers.BRONZE
    elif similarity < 1.0:
        rv = Stickers.SILVER
    else:
        rv = Stickers.GOLD
    return rv
