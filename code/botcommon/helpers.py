from Levenshtein import distance

from botcommon.language import Language


def normalize_text(text):
    language = Language.get_instance()
    normalized_text = language.normalize_text(text)
    return normalized_text


def get_distance(user_text, normalized_text):
    return distance(normalize_text(user_text), normalized_text)
