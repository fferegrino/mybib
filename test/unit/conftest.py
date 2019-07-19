import pytest


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
    return [
        {
            "journal": "CoRR",
            "volume": "abs/1612.06321",
            "year": "2016",
            "url": "http://arxiv.org/abs/1612.06321",
            "archiveprefix": "arXiv",
            "eprint": "1612.06321",
            "keywords": [],
            "timestamp": "Mon, 13 Aug 2018 16:48:55 +0200",
            "biburl": "https://dblp.org/rec/bib/journals/corr/NohASH16",
            "bibsource": "dblp computer science bibliography, https://dblp.org",
            "title": "Image Retrieval with Deep Local Features and Attention-based Keypoints",
            "authors": ["Noh, Hyeonwoo", "Araujo, Andre", "Sim, Jack", "Han, Bohyung"],
            "ENTRYTYPE": "article",
            "ID": "DBLP:journals/corr/NohASH16",
        }
    ]


@pytest.fixture
def bibtex_json_multiple_authors():
    return (
        """@inproceedings{Petrovski:2017:EAP:3106426.3106449,
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
}""",
        [
            {
                "keywords": [
                    "feature extraction",
                    "product data",
                    "schema matching",
                    "web tables",
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
                "authors": ["Petrovski, Petar", "Bizer, Christian"],
                "ENTRYTYPE": "inproceedings",
                "ID": "Petrovski:2017:EAP:3106426.3106449",
            }
        ],
    )


@pytest.fixture
def single_json_multiple_authors(bibtex_json_multiple_authors):
    return bibtex_json_multiple_authors[1][0]


@pytest.fixture
def bibtex_json_single_author():
    return (
        """@inproceedings{Petrovski:2017:EAP:3106426.3106449,
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
}""",
        [
            {
                "keywords": [
                    "feature extraction",
                    "product data",
                    "schema matching",
                    "web tables",
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
                "authors": ["Petrovski, Petar"],
                "ENTRYTYPE": "inproceedings",
                "ID": "Petrovski:2017:EAP:3106426.3106449",
            }
        ],
    )


@pytest.fixture
def bibtex_json_no_keywords():
    return (
        """@inproceedings{Petrovski:2017:EAP:3106426.3106449,
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
}""",
        [
            {
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
                "authors": ["Petrovski, Petar"],
                "ENTRYTYPE": "inproceedings",
                "ID": "Petrovski:2017:EAP:3106426.3106449",
            }
        ],
    )


@pytest.fixture
def bibtext_fails_1():
    return """@article{Chang:2008:BDS:1365815.1365816,
 author = {Chang, Fay and Dean, Jeffrey and Ghemawat, Sanjay and Hsieh, Wilson C. and Wallach, Deborah A. and Burrows, Mike and Chandra, Tushar and Fikes, Andrew and Gruber, Robert E.},
 title = {Bigtable: A Distributed Storage System for Structured Data},
 journal = {ACM Trans. Comput. Syst.},
 issue_date = {June 2008},
 volume = {26},
 number = {2},
 month = jun,
 year = {2008},
 issn = {0734-2071},
 pages = {4:1--4:26},
 articleno = {4},
 numpages = {26},
 url = {http://doi.acm.org/10.1145/1365815.1365816},
 doi = {10.1145/1365815.1365816},
 acmid = {1365816},
 publisher = {ACM},
 address = {New York, NY, USA},
 keywords = {Large-Scale Distributed Storage},
} """


@pytest.fixture
def bibtext_fails_2():
    return """@INPROCEEDINGS{6394574, 
author={G. {Wang} and J. {Tang}}, 
booktitle={2012 International Conference on Computer Science and Service System}, 
title={The NoSQL Principles and Basic Application of Cassandra Model}, 
year={2012}, 
volume={}, 
number={}, 
pages={1332-1335}, 
keywords={relational databases;social networking (online);SQL;NoSQL principles;Cassandra model;CAP theorem;BASE theorem;eventual consistency theorem;foundation stone;NoSQL Cassandra;NoSQL databases;Twitter;Facebook;online trading system;Cassandra database;Databases;Data models;Educational institutions;Availability;Facebook;Servers;NoSQL;CAP;Cassandra;Online Tranding System}, 
doi={10.1109/CSSS.2012.336}, 
ISSN={}, 
month={Aug},}"""


"""@article{Eyal:2018:MEB:3234519.3212998,
 author = {Eyal, Ittay and Sirer, Emin G\"{u}n},
 title = {Majority is Not Enough: Bitcoin Mining is Vulnerable},
 journal = {Commun. ACM},
 issue_date = {July 2018},
 volume = {61},
 number = {7},
 month = jun,
 year = {2018},
 issn = {0001-0782},
 pages = {95--102},
 numpages = {8},
 url = {http://doi.acm.org/10.1145/3212998},
 doi = {10.1145/3212998},
 acmid = {3212998},
 publisher = {ACM},
 address = {New York, NY, USA},
} 
"""

"""@article{8565711,
  abstract     = {In the last five years, deep learning methods and particularly Convolutional Neural Networks (CNNs) have exhibited excellent accuracies in many pattern classification problems. Most of the state-of-the-art models apply data-augmentation techniques at the training stage. This paper provides a brief tutorial on data preprocessing and shows its benefits by using the competitive MNIST handwritten digits classification problem. We show and analyze the impact of different preprocessing techniques on the performance of three CNNs, LeNet, Network3 and DropConnect, together with their ensembles. The analyzed transformations are, centering, elastic deformation, translation, rotation and different combinations of them. Our analysis demonstrates that data-preprocessing techniques, such as the combination of elastic deformation and rotation, together with ensembles have a high potential to further improve the state-of-the-art accuracy in MNIST classification.},
  author       = {Tabik, Siham and Peralta, Daniel and Herrera-Poyatos, Andrés and Herrera, Francisco},
  issn         = {1875-6891},
  journal      = {INTERNATIONAL JOURNAL OF COMPUTATIONAL INTELLIGENCE SYSTEMS},
  keywords     = {Classification,Deep learning,Convolutional Neural Networks (CNNs),preprocessing,handwritten digits,data augmentation,RECOGNITION},
  language     = {eng},
  number       = {1},
  pages        = {555--568},
  title        = {A snapshot of image pre-processing for convolutional neural networks : case study of MNIST},
  url          = {http://dx.doi.org/10.2991/ijcis.2017.10.1.38},
  volume       = {10},
  year         = {2017},
}
"""
