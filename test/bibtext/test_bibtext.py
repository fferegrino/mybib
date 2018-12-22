from mybib.bibtext import load_from_string


def test_load_from_string_multiple_authors(bibtex_multiple_authors, json_multiple_authors):
    actual = load_from_string(bibtex_multiple_authors)
    assert actual == json_multiple_authors


def test_load_from_string_single_author(bibtex_single_author, json_single_author):
    actual = load_from_string(bibtex_single_author)
    assert actual == json_single_author


def test_load_from_string_no_keywords(bibtex_no_keywords, json_no_keywords):
    actual = load_from_string(bibtex_no_keywords)
    assert actual == json_no_keywords
