import re

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import type as bibtextparser_type, author, editor, journal, link, page_double_hyphen, \
    doi


def _split_by(text, separator=',|;'):
    return [i.strip() for i in re.split(separator, text.replace('\n', ''))]


def _get_keywords(record):
    """
    Split keyword field into a list.
    :param record: the record.
    :type record: dict
    :type record: string, optional
    :returns: dict -- the modified record.
    """
    keyword = record.get('keyword')
    keywords = record.get('keywords')
    if keyword:
        record['keywords'] = _split_by(keyword)
    elif keywords:
        record['keywords'] = _split_by(keywords)
    else:
        record['keywords'] = []

    return record


def _customize(record):
    record = bibtextparser_type(record)
    record = author(record)
    record = editor(record)
    record = journal(record)
    record = _get_keywords(record)
    record = link(record)
    record = page_double_hyphen(record)
    record = doi(record)
    return record


def get_parser():
    parser = BibTexParser()
    parser.customization = _customize
    return parser


def load_from_string(bibtex_text):
    return bibtexparser.loads(bibtex_text, parser=get_parser()).entries
