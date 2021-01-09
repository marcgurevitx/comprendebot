import pathlib
import string

from lxml import etree

from botcommon.config import config

_language = None


class Language:
    """Representation of data from 'language-*.xml' file."""

    def __init__(self, language_file):
        self.language_file = language_file
        self.xml_tree = None
        self.alphabet = None
        self.transforms = None
        self._get_xml_tree()
        self._absorb_alphabet()
        self._absorb_transform()

    @classmethod
    def get_instance(cls):
        global _language

        if _language is None:
            _language = cls(config.CMPDBOT_LANGUAGE_FILE)

        return _language

    def normalize_text(self, text):
        text = text.upper()
        for from_, to_ in self.transforms.items():
            text = text.replace(from_, to_)
        text = text.translate({ord(p): " " for p in string.punctuation})
        text = " ".join(text.split())
        return text

    def _get_xml_tree(self):
        xml_path = pathlib.Path(config.CMPDBOT_DIR, "botvars", self.language_file)
        self.xml_tree = etree.parse(str(xml_path))

    def _absorb_alphabet(self):
        alphabet = set()
        for char in self.xml_tree.xpath("//alphabet/a/text()"):
            if len(char) > 1:
                raise Exception(f"Single character expected inside <a>...</a>; got {char}")
            alphabet.add(char.upper())
        self.alphabet = alphabet

    def _absorb_transform(self):
        transforms = {}
        for t_elem in self.xml_tree.xpath("//transform/t"):
            from_list = t_elem.xpath("from/text()")
            to_list = t_elem.xpath("to/text()")
            from_ = from_list[0].upper()
            to_ = to_list[0].upper()
            for char in to_:
                if char not in self.alphabet:
                    raise Exception(f"Expected a character from the alphabet inside <to>...</to>; got {char}")
            transforms[from_] = to_
        self.transforms = transforms
