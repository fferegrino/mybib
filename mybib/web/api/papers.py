from flask import Blueprint, request, jsonify

from mybib.bibtext import load_from_string
from mybib.neo4j import get_paper as get_paper_neo4j, insert_paper as insert_paper_neo4j, \
    search_papers as search_papers_neo4j
from mybib.web.authentication import requires_auth

papers_api = Blueprint('papers_api', __name__)


@papers_api.route('/api/papers/<paper_id:identifier>', methods=['GET'])
def get_paper(identifier):
    return jsonify(get_paper_neo4j(identifier))


@papers_api.route("/api/papers", methods=['POST'])
@requires_auth
def post_paper():
    bibtex_text = request.data.decode('utf-8')
    [paper] = load_from_string(bibtex_text)

    paper['_bibtex'] = bibtex_text
    insert_paper_neo4j(paper)

    response = jsonify()
    response.status_code = 201
    response.headers['location'] = '/api/papers/' + paper['ID']
    response.autocorrect_location_header = False
    return response


@papers_api.route("/api/papers/search", methods=['GET'])
def search_papers():
    title = request.args['title']
    res = search_papers_neo4j(title)
    return jsonify(res)
