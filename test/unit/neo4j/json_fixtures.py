import pytest


@pytest.fixture
def all_papers():
    return [
        {
            "address": "Boston, MA",
            "pages": "3--22",
            "year": "2008",
            "isbn": "978-0-387-69900-4",
            "ENTRYTYPE": "inbook",
            "publisher": "Springer US",
            "_bibtex": """@Inbook{Hepp2008,
author="Hepp, Martin",
editor="Hepp, Martin
and De Leenheer, Pieter
and De Moor, Aldo
and Sure, York",
title="Ontologies: State of the Art, Business Potential, and Grand Challenges",
bookTitle="Ontology Management: Semantic Web, Semantic Web Services, and Business Applications",
year="2008",
publisher="Springer US",
address="Boston, MA",
pages="3--22",
abstract="In this chapter, we give an overview of what ontologies are and how they can be used. We discuss the impact of the expressiveness, the number of domain elements, the community size, the conceptual dynamics, and other variables on the feasibility of an ontology project. Then, we break down the general promise of ontologies of facilitating the exchange and usage of knowledge to six distinct technical advancements that ontologies actually provide, and discuss how this should influence design choices in ontology projects. Finally, we summarize the main challenges of ontology management in real-world applications, and explain which expectations from practitioners can be met as of today.",
isbn="978-0-387-69900-4",
doi="10.1007/978-0-387-69900-4_1",
url="https://doi.org/10.1007/978-0-387-69900-4_1"
}
""",
            "ID": "Hepp2008",
            "title": "Ontologies: State of the Art, Business Potential, and Grand Challenges",
            "booktitle": "Ontology Management: Semantic Web, Semantic Web Services, and Business Applications",
            "url": "https://doi.org/10.1007/978-0-387-69900-4_1",
            "doi": "10.1007/978-0-387-69900-4_1",
        },
        {
            "pages": "555--568",
            "year": "2017",
            "ENTRYTYPE": "article",
            "_bibtex": """@article{8565711,
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
""",
            "ID": "8565711",
            "title": "A snapshot of image pre-processing for convolutional neural networks : case study of MNIST",
            "url": "http://dx.doi.org/10.2991/ijcis.2017.10.1.38",
        },
        {
            "ENTRYTYPE": "article",
            "_bibtex": """@article{DBLP:journals/corr/CohenATS17,
  author    = {Gregory Cohen and
               Saeed Afshar and
               Jonathan Tapson and
               Andr{\'{e}} van Schaik},
  title     = {{EMNIST:} an extension of {MNIST} to handwritten letters},
  journal   = {CoRR},
  volume    = {abs/1702.05373},
  year      = {2017},
  url       = {http://arxiv.org/abs/1702.05373},
  archivePrefix = {arXiv},
  eprint    = {1702.05373},
  timestamp = {Mon, 13 Aug 2018 16:48:00 +0200},
  biburl    = {https://dblp.org/rec/bib/journals/corr/CohenATS17},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}""",
            "ID": "DBLP:journals/corr/CohenATS17",
            "title": "{EMNIST:} an extension of {MNIST} to handwritten letters",
            "year": "2017",
            "url": "http://arxiv.org/abs/1702.05373",
        },
        {
            "ENTRYTYPE": "inproceedings",
            "_bibtex": """@InProceedings{Taigman_2014_CVPR,
author = {Taigman, Yaniv and Yang, Ming and Ranzato, Marc'Aurelio and Wolf, Lior},
title = {DeepFace: Closing the Gap to Human-Level Performance in Face Verification},
booktitle = {The IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
month = {June},
year = {2014}
}""",
            "ID": "Taigman_2014_CVPR",
            "title": "DeepFace: Closing the Gap to Human-Level Performance in Face Verification",
            "booktitle": "The IEEE Conference on Computer Vision and Pattern Recognition (CVPR)",
            "year": "2014",
        },
        {
            "ENTRYTYPE": "inproceedings",
            "_bibtex": """@InProceedings{Schroff_2015_CVPR,
author = {Schroff, Florian and Kalenichenko, Dmitry and Philbin, James},
title = {FaceNet: A Unified Embedding for Face Recognition and Clustering},
booktitle = {The IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
month = {June},
year = {2015}
}""",
            "ID": "Schroff_2015_CVPR",
            "title": "FaceNet: A Unified Embedding for Face Recognition and Clustering",
            "booktitle": "The IEEE Conference on Computer Vision and Pattern Recognition (CVPR)",
            "year": "2015",
        },
        {
            "ENTRYTYPE": "inproceedings",
            "_bibtex": """@inproceedings{36948,
title	= {MapReduce/Bigtable for Distributed Optimization},
author	= {Keith B. Hall and Scott Gilpin and Gideon Mann},
year	= {2010},
note	= {http://lccc.eecs.berkeley.edu/},
booktitle	= {Neural Information Processing Systems Workshop on Leaning on Cores, Clusters, and Clouds}
}

""",
            "ID": "36948",
            "booktitle": "Neural Information Processing Systems Workshop on Leaning on Cores, Clusters, and Clouds",
            "title": "MapReduce/Bigtable for Distributed Optimization",
            "year": "2010",
        },
        {
            "pages": "1332--1335",
            "year": "2012",
            "ENTRYTYPE": "inproceedings",
            "_bibtex": """@INPROCEEDINGS{6394574, 
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
month={Aug},}""",
            "ID": "6394574",
            "booktitle": "2012 International Conference on Computer Science and Service System",
            "title": "The NoSQL Principles and Basic Application of Cassandra Model",
            "doi": "10.1109/CSSS.2012.336",
        },
        {
            "ENTRYTYPE": "article",
            "_bibtex": """@article{DBLP:journals/corr/abs-1708-07747,
  author    = {Han Xiao and
               Kashif Rasul and
               Roland Vollgraf},
  title     = {Fashion-MNIST: a Novel Image Dataset for Benchmarking Machine Learning
               Algorithms},
  journal   = {CoRR},
  volume    = {abs/1708.07747},
  year      = {2017},
  url       = {http://arxiv.org/abs/1708.07747},
  archivePrefix = {arXiv},
  eprint    = {1708.07747},
  timestamp = {Mon, 13 Aug 2018 16:47:27 +0200},
  biburl    = {https://dblp.org/rec/bib/journals/corr/abs-1708-07747},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}""",
            "ID": "DBLP:journals/corr/abs-1708-07747",
            "title": "Fashion-MNIST: a Novel Image Dataset for Benchmarking Machine Learning Algorithms",
            "year": "2017",
            "url": "http://arxiv.org/abs/1708.07747",
        },
    ]
