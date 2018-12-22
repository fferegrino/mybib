import os

from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom

graph: Graph = None


def init_graph():
    global graph
    graph = Graph(
        host=os.getenv('NEO4J_HOST_URL'),
        user=os.getenv('NEO4J_USER'),
        password=os.getenv('NEO4J_PASS'),
        port=os.getenv('NEO4J_PORT'),
    )


class BaseModel(GraphObject):
    __other_properties_dict = dict()
    _time = Property()

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                self.__other_properties_dict[key] = value

    @property
    def all(self):
        return self.select(graph)

    def save(self):
        graph.push(self)


class Paper(BaseModel):
    __primarykey__ = 'ID'

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

    authors = RelatedFrom('Author', 'WROTE')
    keywords = RelatedTo('Keyword', 'HAS_KEYWORD')
    projects = RelatedTo('Project', 'PART_OF')

    references = RelatedTo('Paper', 'REFERENCES')
    referenced_by = RelatedFrom('Paper', 'REFERENCES')

    def asdict(self):
        return {
            'ID': self.ID,
            'title': self.title,
            'address': self.address,
            'acmid': self.acmid,
            'year': self.year,
            'isbn': self.isbn,
            'link': self.link,
            '_bibtex': self._bibtex,
            '_time': self._time,
            'numpages': self.numpages,
            'url': self.url,
            'pages': self.pages,
            'series': self.series,
            'ENTRYTYPE': self.ENTRYTYPE,
            'publisher': self.publisher,
            'location': self.location,
            'booktitle': self.booktitle,
            'doi': self.doi,
        }

    def fetch(self):
        return Paper.match(graph, self.ID).first()

    def fetch_authors(self):
        return [{
            **author[0].asdict(),
            **author[1]
        } for author in self.authors._related_objects]

    def fetch_keywords(self):
        return [{
            **kw[0].asdict(),
            **kw[1]
        } for kw in self.keywords._related_objects]

    def fetch_projects(self):
        return [{
            **proj[0].asdict(),
            **proj[1]
        } for proj in self.projects._related_objects]

    def fetch_references(self):
        return [{
            **proj[0].asdict(),
            **proj[1]
        } for proj in self.references._related_objects]


class Author(BaseModel):
    __primarykey__ = 'name'
    name = Property()

    papers = RelatedTo('Paper', 'WROTE')

    def fetch(self):
        return Author.match(graph, self.name).first()

    def asdict(self):
        return {
            'name': self.name,
        }


class Keyword(BaseModel):
    __primarykey__ = 'value'
    value = Property()

    papers = RelatedFrom('Paper', 'HAS_KEYWORD')

    def fetch(self):
        return Keyword.match(graph, self.value).first()

    def asdict(self):
        return {
            'value': self.value,
        }


class Project(BaseModel):
    __primarykey__ = 'name'
    name = Property()

    papers = RelatedTo('Paper', 'PART_OF')

    def fetch(self):
        return Project.match(graph, self.name).first()

    def asdict(self):
        return {
            'name': self.name,
        }
