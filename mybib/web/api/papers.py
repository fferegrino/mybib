from flask import Blueprint, jsonify, request

from mybib.bibtext.reader import load_from_string
from mybib.neo4j.models import Author, Keyword, Paper
from mybib.web.authentication import requires_auth

papers_api = Blueprint("papers_api", __name__)


@papers_api.route("/api/papers/<paper_id:identifier>", methods=["GET"])
def get_paper(identifier):
    paper = Paper(ID=identifier).fetch()
    return jsonify(paper.asdict())


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


@papers_api.route("/api/papers", methods=["POST"])
@requires_auth
def post_paper():
    bibtex_text = request.data.decode("utf-8")
    [paper_dict] = load_from_string(bibtex_text)

    paper_dict["_bibtex"] = bibtex_text
    keywords = paper_dict.pop("keywords")
    authors = paper_dict.pop("authors")

    paper_to_insert = Paper(**paper_dict)

    response = jsonify()

    already_exists = paper_to_insert.fetch() is not None

    if not already_exists:
        paper_to_insert.save()

        for kw in keywords:
            paper_to_insert.keywords.add(get_create_keyword(kw))

        for author in authors:
            paper_to_insert.authors.add(get_create_author(author))

        paper_to_insert.save()

        response.status_code = 201
        response.autocorrect_location_header = False

    else:
        response.status_code = 409

    response.headers["location"] = "/api/papers/" + paper_dict["ID"]
    return response


@papers_api.route("/api/papers/search", methods=["GET"])
def search_papers():
    title = request.args["title"]
    res = None
    return jsonify(res)
