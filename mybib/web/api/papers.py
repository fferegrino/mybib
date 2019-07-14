from flask import Blueprint, jsonify, request

from mybib.bibtext import load_from_string
from mybib.neo4j.models import Author, Keyword, Paper
from mybib.web.authentication import requires_auth

papers_api = Blueprint("papers_api", __name__)


@papers_api.route("/api/papers/<paper_id:identifier>", methods=["GET"])
def get_paper(identifier):
    paper = Paper(ID=identifier).fetch()
    return jsonify(paper.asdict())


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
            keyword = Keyword(value=kw)
            fetched_keyword = keyword.fetch()
            if fetched_keyword:
                paper_to_insert.keywords.add(fetched_keyword)
            else:
                keyword.save()
                paper_to_insert.keywords.add(keyword)

        for author in authors:
            author_ = Author(name=author)
            fetched_author = author_.fetch()
            if fetched_author:
                paper_to_insert.authors.add(fetched_author)
            else:
                author_.save()
                paper_to_insert.authors.add(author_)

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
