import pytest


@pytest.fixture
def bibtex_multiple_authors():
    return """@inproceedings{Petrovski:2017:EAP:3106426.3106449,
 author = {Petrovski, Petar and Bizer, Christian},
 title = {Extracting Attribute-value Pairs from Product Specifications on the Web},
 booktitle = {Proceedings of the International Conference on Web Intelligence},
 series = {WI '17},
 year = {2017},
 isbn = {978-1-4503-4951-2},
 location = {Leipzig, Germany},
 pages = {558--565},
 numpages = {8},
 url = {http://doi.acm.org/10.1145/3106426.3106449},
 doi = {10.1145/3106426.3106449},
 acmid = {3106449},
 publisher = {ACM},
 address = {New York, NY, USA},
 keywords = {feature extraction, product data, schema matching, web tables},
}"""

@pytest.fixture
def bibtex_dblp_format():
    return """@article{DBLP:journals/corr/NohASH16,
  author    = {Hyeonwoo Noh and
               Andre Araujo and
               Jack Sim and
               Bohyung Han},
  title     = {Image Retrieval with Deep Local Features and Attention-based Keypoints},
  journal   = {CoRR},
  volume    = {abs/1612.06321},
  year      = {2016},
  url       = {http://arxiv.org/abs/1612.06321},
  archivePrefix = {arXiv},
  eprint    = {1612.06321},
  timestamp = {Mon, 13 Aug 2018 16:48:55 +0200},
  biburl    = {https://dblp.org/rec/bib/journals/corr/NohASH16},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}"""

@pytest.fixture
def json_dblp_format():
    return [{
  "journal": "CoRR",
  "volume": "abs/1612.06321",
  "year": "2016",
  "url": "http://arxiv.org/abs/1612.06321",
  "archiveprefix": "arXiv",
  "eprint": "1612.06321",
    "keywords":[],
  "timestamp": "Mon, 13 Aug 2018 16:48:55 +0200",
  "biburl": "https://dblp.org/rec/bib/journals/corr/NohASH16",
  "bibsource": "dblp computer science bibliography, https://dblp.org",
        "title": "Image Retrieval with Deep Local Features and Attention-based Keypoints",
        "authors": [
            "Noh, Hyeonwoo",
            "Araujo, Andre",
            "Sim, Jack",
            "Han, Bohyung",
        ],
        "ENTRYTYPE": "article",
        "ID": "DBLP:journals/corr/NohASH16",
    }]

@pytest.fixture
def json_multiple_authors():
    return [{
        "keywords": [
            "feature extraction",
            "product data",
            "schema matching",
            "web tables"
        ],
        "address": "New York, NY, USA",
        "publisher": "ACM",
        "acmid": "3106449",
        "doi": "10.1145/3106426.3106449",
        "url": "http://doi.acm.org/10.1145/3106426.3106449",
        "numpages": "8",
        "pages": "558--565",
        "location": "Leipzig, Germany",
        "isbn": "978-1-4503-4951-2",
        "year": "2017",
        "series": "WI '17",
        "booktitle": "Proceedings of the International Conference on Web Intelligence",
        "title": "Extracting Attribute-value Pairs from Product Specifications on the Web",
        "authors": [
            "Petrovski, Petar",
            "Bizer, Christian"
        ],
        "ENTRYTYPE": "inproceedings",
        "ID": "Petrovski:2017:EAP:3106426.3106449",
    }]


@pytest.fixture
def bibtex_single_author():
    return """@inproceedings{Petrovski:2017:EAP:3106426.3106449,
 author = {Petrovski, Petar},
 title = {Extracting Attribute-value Pairs from Product Specifications on the Web},
 booktitle = {Proceedings of the International Conference on Web Intelligence},
 series = {WI '17},
 year = {2017},
 isbn = {978-1-4503-4951-2},
 location = {Leipzig, Germany},
 pages = {558--565},
 numpages = {8},
 url = {http://doi.acm.org/10.1145/3106426.3106449},
 doi = {10.1145/3106426.3106449},
 acmid = {3106449},
 publisher = {ACM},
 address = {New York, NY, USA},
 keywords = {feature extraction, product data, schema matching, web tables},
}"""


@pytest.fixture
def json_single_author():
    return [{
        "keywords": [
            "feature extraction",
            "product data",
            "schema matching",
            "web tables"
        ],
        "address": "New York, NY, USA",
        "publisher": "ACM",
        "acmid": "3106449",
        "doi": "10.1145/3106426.3106449",
        "url": "http://doi.acm.org/10.1145/3106426.3106449",
        "numpages": "8",
        "pages": "558--565",
        "location": "Leipzig, Germany",
        "isbn": "978-1-4503-4951-2",
        "year": "2017",
        "series": "WI '17",
        "booktitle": "Proceedings of the International Conference on Web Intelligence",
        "title": "Extracting Attribute-value Pairs from Product Specifications on the Web",
        "authors": [
            "Petrovski, Petar"
        ],
        "ENTRYTYPE": "inproceedings",
        "ID": "Petrovski:2017:EAP:3106426.3106449",
    }]


@pytest.fixture
def bibtex_no_keywords():
    return """@inproceedings{Petrovski:2017:EAP:3106426.3106449,
 author = {Petrovski, Petar},
 title = {Extracting Attribute-value Pairs from Product Specifications on the Web},
 booktitle = {Proceedings of the International Conference on Web Intelligence},
 series = {WI '17},
 year = {2017},
 isbn = {978-1-4503-4951-2},
 location = {Leipzig, Germany},
 pages = {558--565},
 numpages = {8},
 url = {http://doi.acm.org/10.1145/3106426.3106449},
 doi = {10.1145/3106426.3106449},
 acmid = {3106449},
 publisher = {ACM},
 address = {New York, NY, USA},
}"""


@pytest.fixture
def json_no_keywords():
    return [{
        "keywords": [],
        "address": "New York, NY, USA",
        "publisher": "ACM",
        "acmid": "3106449",
        "doi": "10.1145/3106426.3106449",
        "url": "http://doi.acm.org/10.1145/3106426.3106449",
        "numpages": "8",
        "pages": "558--565",
        "location": "Leipzig, Germany",
        "isbn": "978-1-4503-4951-2",
        "year": "2017",
        "series": "WI '17",
        "booktitle": "Proceedings of the International Conference on Web Intelligence",
        "title": "Extracting Attribute-value Pairs from Product Specifications on the Web",
        "authors": [
            "Petrovski, Petar"
        ],
        "ENTRYTYPE": "inproceedings",
        "ID": "Petrovski:2017:EAP:3106426.3106449",
    }]
