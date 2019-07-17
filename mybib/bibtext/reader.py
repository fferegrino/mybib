import bibtexparser

from mybib.bibtext.record_customization import _customize


def get_parser():
    parser = bibtexparser.bparser.BibTexParser()
    parser.customization = _customize
    return parser


def load_from_string(bibtex_text):
    return bibtexparser.loads(bibtex_text, parser=get_parser()).entries
