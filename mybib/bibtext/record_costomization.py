import bibtexparser
from bibtexparser.customization import type as bibtextparser_type

from mybib.bibtext.utils import _split_by


def _get_keywords(record):
    """
    Split keyword field into a list.
    :param record: the record.
    :type record: dict
    :type record: string, optional
    :returns: dict -- the modified record.
    """
    keyword = record.get("keyword")
    keywords = record.get("keywords")
    if keyword:
        del record["keywords"]
        record["keywords"] = _split_by(keyword)
    elif keywords:
        del record["keywords"]
        record["keywords"] = _split_by(keywords)
    else:
        record["keywords"] = []

    return record


def _get_authors(record):
    """
    Split author field into a list of "Name, Surname".
    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    author = record.get("author")
    authors = record.get("authors")
    if authors:
        del record["authors"]
        record["authors"] = bibtexparser.customization.getnames(
            [i.strip() for i in authors.replace("\n", " ").split(" and ")]
        )
    elif author:
        del record["author"]
        record["authors"] = bibtexparser.customization.getnames(
            [i.strip() for i in author.replace("\n", " ").split(" and ")]
        )
    else:
        record["authors"] = []

    return record


def _customize(record):
    record = bibtextparser_type(record)
    record = _get_authors(record)
    record = bibtexparser.customization.editor(record)
    record = _get_keywords(record)
    record = bibtexparser.customization.page_double_hyphen(record)
    return record