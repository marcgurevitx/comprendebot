import collections
import enum

Button = collections.namedtuple("Button", "text, data")

Sendable = collections.namedtuple("Sendable", "type, value, is_reply, buttons")

SimilarPhrase = collections.namedtuple("SimilarPhrase", "phrase, similarity")


class SendableTypeCode(enum.Enum):
    SND_TXT = "SND_TXT"
    SND_VOC = "SND_VOC"
    SND_STK = "SND_STK"


class ChallengeTypeCode(enum.Enum):
    CHL_PHR = "CHL_PHR"
    CHL_VOC = "CHL_VOC"
    CHL_TRS = "CHL_TRS"


class PhraseStates(enum.Enum):
    PHR_CRE = "PHR_CRE"
    PHR_WRK = "PHR_WRK"
    PHR_END = "PHR_END"


class VoiceStates(enum.Enum):
    VOC_CRE = "VOC_CRE"
    VOC_WRK = "VOC_WRK"
    VOC_END = "VOC_END"


class TranscriptionStates(enum.Enum):
    TRS_CRE = "TRS_CRE"
    TRS_WRK = "TRS_WRK"
    TRS_END = "TRS_END"


class Stickers(enum.Enum):
    PHR = "PHR"
    VOC = "VOC"
    TRS = "TRS"
    GOLD = "GOLD"
    SILVER = "SILVER"
    BRONZE = "BRONZE"
    PAPER = "PAPER"
    OK_PHR = "OK_PHR"
    OK_VOC = "OK_VOC"
