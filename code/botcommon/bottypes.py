import collections
import enum

SimilarPhrase = collections.namedtuple("SimilarPhrase", "phrase, similarity")


class ChallengeTypeCode(enum.Enum):
    CHL_PHR = 'CHL_PHR'
    CHL_VOC = 'CHL_VOC'
    CHL_TRS = 'CHL_TRS'
