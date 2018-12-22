import graphene

from mybib.neo4j.models import Paper


class MyBibSchema(graphene.ObjectType):
    _time = graphene.Float()


class AuthorSchema(MyBibSchema):
    name = graphene.String()


class KeywordSchema(MyBibSchema):
    value = graphene.String()


class ProjectSchema(MyBibSchema):
    name = graphene.String()


class PaperSchema(MyBibSchema):
    ID = graphene.String()
    title = graphene.String()
    address = graphene.String()
    acmid = graphene.String()
    year = graphene.String()
    isbn = graphene.String()
    link = graphene.String()
    _bibtex = graphene.String()
    numpages = graphene.String()
    url = graphene.String()
    pages = graphene.String()
    series = graphene.String()
    ENTRYTYPE = graphene.String()
    publisher = graphene.String()
    location = graphene.String()
    booktitle = graphene.String()
    doi = graphene.String()

    authors = graphene.List(AuthorSchema)
    keywords = graphene.List(KeywordSchema)
    projects = graphene.List(ProjectSchema)
    references = graphene.List(lambda: PaperSchema)

    def resolve_authors(self, info):
        return [AuthorSchema(**author) for author in Paper(ID=self.ID).fetch().fetch_authors()]

    def resolve_keywords(self, info):
        return [KeywordSchema(**keyword) for keyword in Paper(ID=self.ID).fetch().fetch_keywords()]

    def resolve_projects(self, info):
        return [ProjectSchema(**project) for project in Paper(ID=self.ID).fetch().fetch_projects()]

    def resolve_references(self, info):
        return [PaperSchema(**paper) for paper in Paper(ID=self.ID).fetch().fetch_references()]


class Query(graphene.ObjectType):
    paper = graphene.Field(lambda: PaperSchema, ID=graphene.String())

    papers = graphene.List(lambda: PaperSchema)

    def resolve_paper(self, info, ID):
        customer = Paper(ID=ID).fetch()
        return PaperSchema(**customer.asdict())

    def resolve_papers(self, info):
        return [PaperSchema(**paper.asdict()) for paper in Paper().all()]


schema = graphene.Schema(query=Query, auto_camelcase=False)
