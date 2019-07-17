import os

from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedFrom, RelatedTo

GRAPH: Graph = None

REFERENCES_RELATIONSHIP = "REFERENCES"
WROTE_RELATIONSHIP = "WROTE"
HAS_KEYWORD_RELATIONSHIP = "HAS_KEYWORD"
PART_OF_RELATIONSHIP = "PART_OF"


def get_graph():
    global GRAPH
    if not GRAPH:
        host = os.getenv("NEO4J_URL")
        user = os.getenv("NEO4J_USER")
        password = os.getenv("NEO4J_PASS")
        port = int(os.getenv("NEO4J_PORT"))
        GRAPH = Graph(host=host, user=user, password=password, port=port, secure=True)
    return GRAPH


class BaseModel(GraphObject):
    __other_properties_dict = dict()
    _time = Property()

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                self.__other_properties_dict[key] = value

    def all(self):
        graph = get_graph()
        return self.match(graph)

    def save(self):
        graph = get_graph()
        graph.push(self)


class Paper(BaseModel):
    __primarykey__ = "ID"

    ID = Property()
    title = Property()
    address = Property()
    acmid = Property()
    year = Property()
    isbn = Property()
    link = Property()
    _bibtex = Property()
    numpages = Property()
    url = Property()
    pages = Property()
    series = Property()
    ENTRYTYPE = Property()
    publisher = Property()
    location = Property()
    booktitle = Property()
    doi = Property()

    authors = RelatedFrom("Author", WROTE_RELATIONSHIP)
    keywords = RelatedTo("Keyword", HAS_KEYWORD_RELATIONSHIP)
    projects = RelatedFrom("Project", PART_OF_RELATIONSHIP)

    references = RelatedTo("Paper", REFERENCES_RELATIONSHIP)
    referenced_by = RelatedFrom("Paper", REFERENCES_RELATIONSHIP)

    def asdict(self):
        return {
            "ID": self.ID,
            "title": self.title,
            "address": self.address,
            "acmid": self.acmid,
            "year": self.year,
            "isbn": self.isbn,
            "link": self.link,
            "_bibtex": self._bibtex,
            "_time": self._time,
            "numpages": self.numpages,
            "url": self.url,
            "pages": self.pages,
            "series": self.series,
            "ENTRYTYPE": self.ENTRYTYPE,
            "publisher": self.publisher,
            "location": self.location,
            "booktitle": self.booktitle,
            "doi": self.doi,
        }

    def fetch(self):
        graph = get_graph()
        return Paper.match(graph, self.ID).first()

    def fetch_authors(self):
        return [
            {**author[0].asdict(), **author[1]}
            for author in self.authors._related_objects
        ]

    def fetch_keywords(self):
        return [{**kw[0].asdict(), **kw[1]} for kw in self.keywords._related_objects]

    def fetch_projects(self):
        return [
            {**proj[0].asdict(), **proj[1]} for proj in self.projects._related_objects
        ]

    def fetch_references(self):
        return [{**proj[0].asdict()} for proj in self.references._related_objects]


class Author(BaseModel):
    __primarykey__ = "name"
    name = Property()

    papers = RelatedTo("Paper", WROTE_RELATIONSHIP)

    def fetch(self):
        graph = get_graph()
        return Author.match(graph, self.name).first()

    def fetch_papers(self):
        return [{**paper[0].asdict()} for paper in self.papers._related_objects]

    def asdict(self):
        return {"name": self.name}


class Keyword(BaseModel):
    __primarykey__ = "value"
    value = Property()

    papers = RelatedFrom("Paper", HAS_KEYWORD_RELATIONSHIP)

    def fetch(self):
        graph = get_graph()
        return Keyword.match(graph, self.value).first()

    def fetch_papers(self):
        return [{**paper[0].asdict()} for paper in self.papers._related_objects]

    def asdict(self):
        return {"value": self.value}


class Project(BaseModel):
    __primarykey__ = "name"
    name = Property()

    papers = RelatedTo("Paper", PART_OF_RELATIONSHIP)

    def fetch(self):
        graph = get_graph()
        return Project.match(graph, self.name).first()

    def fetch_papers(self):
        return [{**paper[0].asdict()} for paper in self.papers._related_objects]

    def asdict(self):
        return {"name": self.name}
