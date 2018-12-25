import os

from py2neo import Graph, NodeMatcher
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom

GRAPH: Graph = None

REFERENCES_RELATIONSHIP = 'REFERENCES'

HAS_KEYWORD_RELATIONSHIP = 'HAS_KEYWORD'


def get_graph():
    global GRAPH
    if not GRAPH:
        host = os.getenv('NEO4J_URL')
        user = os.getenv('NEO4J_USER')
        password = os.getenv('NEO4J_PASS')
        port = int(os.getenv('NEO4J_PORT'))
        GRAPH = Graph(
            host=host,
            user=user,
            password=password,
            port=port,
            secure=True,
        )
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


def are_related(referee_id, referenced_id):
    referee = Paper(ID=referee_id).fetch()
    referenced = Paper(ID=referenced_id).fetch()

    assert referee is not None
    assert referenced is not None

    graph = get_graph()
    matches = list(graph.match((referee.__ogm__.node, referenced.__ogm__.node), r_type=REFERENCES_RELATIONSHIP))
    return len(matches) > 0


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
    keywords = RelatedTo('Keyword', HAS_KEYWORD_RELATIONSHIP)
    projects = RelatedTo('Project', 'PART_OF')

    references = RelatedTo('Paper', REFERENCES_RELATIONSHIP)
    referenced_by = RelatedFrom('Paper', REFERENCES_RELATIONSHIP)

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
        graph = get_graph()
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
            # **proj[1] # Reference properties
        } for proj in self.references._related_objects]


class Author(BaseModel):
    __primarykey__ = 'name'
    name = Property()

    papers = RelatedTo('Paper', 'WROTE')

    def fetch(self):
        graph = get_graph()
        return Author.match(graph, self.name).first()

    def asdict(self):
        return {
            'name': self.name,
        }


def return_keywords(query):
    graph = get_graph()
    matcher = NodeMatcher(graph)
    kws = matcher.match('Keyword', value__contains=query)
    return [dict(kw) for kw in kws]


def return_papers_by_keyword(query):
    graph = get_graph()
    matcher = NodeMatcher(graph)
    kws = matcher.match('Keyword', value__contains=query)
    retrieved_papers = set()
    papers = []
    for keyword in [Keyword(**dict(kw)).fetch() for kw in kws]:
        for paper in keyword.fetch_papers():
            if paper['ID'] in retrieved_papers:
                continue
            papers.append(paper)
            retrieved_papers.add(paper['ID'])
    return papers


class Keyword(BaseModel):
    __primarykey__ = 'value'
    value = Property()

    papers = RelatedFrom('Paper', HAS_KEYWORD_RELATIONSHIP)

    def fetch(self):
        graph = get_graph()
        return Keyword.match(graph, self.value).first()

    def fetch_papers(self):
        return [{
            **paper[0].asdict(),
        } for paper in self.papers._related_objects]

    def asdict(self):
        return {
            'value': self.value,
        }


class Project(BaseModel):
    __primarykey__ = 'name'
    name = Property()

    papers = RelatedTo('Paper', 'PART_OF')

    def fetch(self):
        graph = get_graph()
        return Project.match(graph, self.name).first()

    def asdict(self):
        return {
            'name': self.name,
        }
