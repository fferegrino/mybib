from py2neo import NodeMatcher

from mybib.neo4j.models import (
    REFERENCES_RELATIONSHIP,
    Author,
    Keyword,
    Paper,
    Project,
    get_graph,
)


class EntityAlreadyExistsError(Exception):
    pass


def get_create_keyword(keyword):
    kw = Keyword(keyword)
    kw_ = kw.fetch()
    if kw_ is None:
        kw.save()
        return kw
    return kw_


def get_create_author(author):
    auth = Author(name=author)
    auth_ = auth.fetch()
    if auth_ is None:
        auth.save()
        return auth
    return auth_


def get_paper(identifier):
    paper = Paper(ID=identifier).fetch()
    return paper.asdict()


def insert_paper(paper_dict):
    keywords = paper_dict.pop("keywords")
    authors = paper_dict.pop("authors")
    paper_to_insert = Paper(**paper_dict)

    existing_paper = paper_to_insert.fetch()
    if existing_paper is not None:
        raise EntityAlreadyExistsError()

    paper_to_insert.save()

    for kw in keywords:
        paper_to_insert.keywords.add(get_create_keyword(kw))

    for author in authors:
        paper_to_insert.authors.add(get_create_author(author))

    paper_to_insert.save()

    return paper_to_insert


def are_related(referee_id, referenced_id):
    referee = Paper(ID=referee_id).fetch()
    referenced = Paper(ID=referenced_id).fetch()

    assert referee is not None
    assert referenced is not None

    graph = get_graph()
    matches = list(
        graph.match(
            (referee.__ogm__.node, referenced.__ogm__.node),
            r_type=REFERENCES_RELATIONSHIP,
        )
    )
    return len(matches) > 0


def insert_reference(referee, referenced, attr_dict):
    relationship_exists = are_related(referee, referenced)

    if relationship_exists:
        raise EntityAlreadyExistsError()

    referee_paper = Paper(ID=referee).fetch()
    referenced_paper = Paper(ID=referenced).fetch()

    referee_paper.references.add(referenced_paper, attr_dict)
    referee_paper.save()


def return_keywords(query):
    graph = get_graph()
    matcher = NodeMatcher(graph)
    kws = matcher.match("Keyword", value__contains=query)
    return [dict(kw) for kw in kws]


def return_papers_by_keyword(query):
    graph = get_graph()
    matcher = NodeMatcher(graph)
    kws = matcher.match("Keyword", value__contains=query)
    retrieved_papers = set()
    papers = []
    for keyword in [Keyword(**dict(kw)).fetch() for kw in kws]:
        for paper in keyword.fetch_papers():
            if paper["ID"] in retrieved_papers:
                continue
            papers.append(paper)
            retrieved_papers.add(paper["ID"])
    return papers


def return_papers_by_author(query):
    graph = get_graph()
    matcher = NodeMatcher(graph)
    kws = matcher.match("Author", name__contains=query)
    retrieved_papers = set()
    papers = []
    for keyword in [Author(**dict(kw)).fetch() for kw in kws]:
        for paper in keyword.fetch_papers():
            if paper["ID"] in retrieved_papers:
                continue
            papers.append(paper)
            retrieved_papers.add(paper["ID"])
    return papers


def return_papers_by_project(query):
    graph = get_graph()
    matcher = NodeMatcher(graph)
    kws = matcher.match("Project", name__contains=query)
    retrieved_papers = set()
    papers = []
    for keyword in [Project(**dict(kw)).fetch() for kw in kws]:
        for paper in keyword.fetch_papers():
            if paper["ID"] in retrieved_papers:
                continue
            papers.append(paper)
            retrieved_papers.add(paper["ID"])
    return papers


def return_papers_by_title(query):
    graph = get_graph()
    matcher = NodeMatcher(graph)
    nodes = matcher.match("Paper", title__contains=query)
    return [Paper(**dict(p)) for p in nodes]
