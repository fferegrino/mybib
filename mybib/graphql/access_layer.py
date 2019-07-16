from mybib.neo4j.models import Author, Keyword, Paper


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
