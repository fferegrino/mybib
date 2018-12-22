from flask import Blueprint, request, jsonify

from mybib.bibtext import load_from_string
from mybib.neo4j.models import Paper, Keyword, Author
from mybib.web.authentication import requires_auth

papers_api = Blueprint('papers_api', __name__)


@papers_api.route('/api/papers/<paper_id:identifier>', methods=['GET'])
def get_paper(identifier):
    paper = Paper(ID=identifier).fetch()
    return jsonify(paper.asdict())


@papers_api.route("/api/papers", methods=['POST'])
@requires_auth
def post_paper():
    bibtex_text = request.data.decode('utf-8')
    [paper] = load_from_string(bibtex_text)

    paper['_bibtex'] = bibtex_text
    keywords = paper.pop('keywords')
    authors = paper.pop('authors')

    Paper(**paper).save()

    for kw in keywords:
        Keyword(value=kw).save()

    for author in authors:
        Author(name=author).save()

    response = jsonify()
    response.status_code = 201
    response.headers['location'] = '/api/papers/' + paper['ID']
    response.autocorrect_location_header = False
    return response


@papers_api.route("/api/papers/search", methods=['GET'])
def search_papers():
    title = request.args['title']
    res = None
    return jsonify(res)
