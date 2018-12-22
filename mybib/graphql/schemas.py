import graphene

from mybib.neo4j.models import Paper


class MyBibSchema(graphene.ObjectType):
    _time = graphene.Float()


#class KeywordSchema(MyBibSchema):
#    value = graphene.String()
#
#
#class AuthorSchema(MyBibSchema):
#    name = graphene.String()
#
#
#class ProjectSchema(MyBibSchema):
#    name = graphene.String()


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

    #authors = graphene.List(AuthorSchema)
    #keywords = graphene.List(KeywordSchema)
    #projects = graphene.List(ProjectSchema)

    #def resolve_authors(self, info):
    #    return [AuthorSchema(**author) for author in Paper(ID=self.ID).fetch().fetch_authors()]


class Query(graphene.ObjectType):
    paper = graphene.Field(lambda: PaperSchema, ID=graphene.String())

    def resolve_paper(self, info, ID):
        customer = Paper(ID=ID).fetch()
        return PaperSchema(**customer.asdict())


schema = graphene.Schema(query=Query, auto_camelcase=False)
