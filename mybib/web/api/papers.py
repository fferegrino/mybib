from flask import Blueprint, jsonify, request

from mybib.bibtext.reader import load_from_string
from mybib.graphql.access_layer import EntityAlreadyExistsError
from mybib.graphql.access_layer import get_paper as get_paper_da
from mybib.graphql.access_layer import insert_paper
from mybib.neo4j.models import Paper
from mybib.web.authentication import requires_auth

papers_api = Blueprint("papers_api", __name__)


@papers_api.route("/api/papers/<paper_id:identifier>", methods=["GET"])
def get_paper(identifier):
    return jsonify(get_paper_da(identifier))


@papers_api.route("/api/papers", methods=["POST"])
@requires_auth
def post_paper():
    bibtex_text = request.data.decode("utf-8")
    [paper_dict] = load_from_string(bibtex_text)
    paper_dict["_bibtex"] = bibtex_text

    response = jsonify()

    try:
        insert_paper(paper_dict)
        response.status_code = 201
        response.autocorrect_location_header = False
    except EntityAlreadyExistsError:
        response.status_code = 409

    response.headers["location"] = f"/api/papers/{paper_dict['ID']}"
    return response


@papers_api.route("/api/papers/search", methods=["GET"])
def search_papers():
    title = request.args["title"]
    res = None
    return jsonify(res)
