from flask import Blueprint, request, jsonify

from mybib.bibtext import load_from_string
from mybib.neo4j.models import Paper, Keyword, Author, graph
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
    [paper_dict] = load_from_string(bibtex_text)

    paper_dict['_bibtex'] = bibtex_text
    keywords = paper_dict.pop('keywords')
    authors = paper_dict.pop('authors')

    inserted_paper = Paper(**paper_dict)
    inserted_paper.save()

    for kw in keywords:
        keyword = Keyword(value=kw)
        fetched_keyword = keyword.fetch()
        if fetched_keyword:
            inserted_paper.keywords.add(fetched_keyword)
        else:
            keyword.save()
            inserted_paper.keywords.add(keyword)

    for author in authors:
        author_ = Author(name=author)
        fetched_author = author_.fetch()
        if fetched_author:
            inserted_paper.authors.add(fetched_author)
        else:
            author_.save()
            inserted_paper.authors.add(author_)

    inserted_paper.save()

    response = jsonify()
    response.status_code = 201
    response.headers['location'] = '/api/papers/' + paper_dict['ID']
    response.autocorrect_location_header = False
    return response


@papers_api.route("/api/papers/search", methods=['GET'])
def search_papers():
    title = request.args['title']
    res = None
    return jsonify(res)
