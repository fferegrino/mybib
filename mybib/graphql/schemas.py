import graphene

import mybib.graphql.access_layer
from mybib.neo4j import models


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
        return [
            AuthorSchema(**author)
            for author in models.Paper(ID=self.ID).fetch().fetch_authors()
        ]

    def resolve_keywords(self, info):
        return [
            KeywordSchema(**keyword)
            for keyword in models.Paper(ID=self.ID).fetch().fetch_keywords()
        ]

    def resolve_projects(self, info):
        return [
            ProjectSchema(**project)
            for project in models.Paper(ID=self.ID).fetch().fetch_projects()
        ]

    def resolve_references(self, info):
        return [
            PaperSchema(**paper)
            for paper in models.Paper(ID=self.ID).fetch().fetch_references()
        ]


class Query(graphene.ObjectType):
    paper = graphene.Field(lambda: PaperSchema, ID=graphene.String())

    keywords = graphene.List(lambda: KeywordSchema, keyword=graphene.String())

    by_id = graphene.List(lambda: PaperSchema, parameter=graphene.String())
    by_keywords = graphene.List(lambda: PaperSchema, parameter=graphene.String())
    by_author = graphene.List(lambda: PaperSchema, parameter=graphene.String())
    by_title = graphene.List(lambda: PaperSchema, parameter=graphene.String())
    by_project = graphene.List(lambda: PaperSchema, parameter=graphene.String())

    papers = graphene.List(lambda: PaperSchema)

    def resolve_paper(self, info, ID):
        customer = models.Paper(ID=ID).fetch()
        return PaperSchema(**customer.asdict())

    def resolve_papers(self, info):
        return [PaperSchema(**paper.asdict()) for paper in models.Paper().all()]

    def resolve_keywords(self, info, keyword):
        return [
            KeywordSchema(**kw)
            for kw in mybib.graphql.access_layer.return_keywords(keyword)
        ]

    def resolve_by_id(self, info, parameter):
        customer = models.Paper(ID=parameter).fetch()
        return [PaperSchema(**customer.asdict())]

    def resolve_by_keywords(self, info, parameter):
        return [
            PaperSchema(**paper)
            for paper in mybib.graphql.access_layer.return_papers_by_keyword(parameter)
        ]

    def resolve_by_author(self, info, parameter):
        return [
            PaperSchema(**paper)
            for paper in mybib.graphql.access_layer.return_papers_by_author(parameter)
        ]

    def resolve_by_project(self, info, parameter):
        return [
            PaperSchema(**paper)
            for paper in mybib.graphql.access_layer.return_papers_by_project(parameter)
        ]

    def resolve_by_title(self, info, parameter):
        return [
            PaperSchema(**paper.asdict())
            for paper in mybib.graphql.access_layer.return_papers_by_title(parameter)
        ]


schema = graphene.Schema(query=Query, auto_camelcase=False)
